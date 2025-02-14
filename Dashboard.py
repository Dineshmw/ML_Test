import re
import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import bcrypt
from streamlit_cookies_manager import EncryptedCookieManager
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(
    layout="wide",
    page_title="AudioHitAnalyzer",
    page_icon="🎧"
)

cookies = EncryptedCookieManager(
    prefix="my_app",
    password="111"
)

if not cookies.ready():
    st.stop()

def set_login_cookies(username):
    cookies["logged_in"] = "True"
    cookies["username"] = username
    cookies.save()

def clear_login_cookies():
    cookies["logged_in"] = "False"
    cookies["username"] = ""
    cookies.save()

def hash_passwords(passwords):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(input_password, stored_hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))

def load_config():
    with open('config.yaml') as file:
        return yaml.load(file, Loader=SafeLoader)

def save_config(config):
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

def is_strong_password(password):
    if (len(password) < 8 or
            not re.search(r'[A-Z]', password) or
            not re.search(r'[a-z]', password) or
            not re.search(r'\d', password) or
            not re.search(r'[@$!%*?&#]', password)):
        return False
    return True

if 'login_state' not in st.session_state:
    st.session_state.login_state = {
        'logged_in': cookies.get("logged_in") == "True",
        'username': cookies.get("username") if cookies.get("username") else None
    }
    

def appName():
        st.markdown("""
            <style>
                [data-testid="stSidebarNav"]::before {
                    content: "🎧 AudioHitAnalyzer";
                    margin-left: 25px;
                    font-size: 22px;
                    position: relative;
                    top: -20px;
                    font-weight: 600;
                }
            </style>
        """, unsafe_allow_html=True)

config = load_config()

# ***********************************************************************
if 'login_state' not in st.session_state:
    st.session_state.login_state = {
        'logged_in': cookies.get("logged_in") == "True",
        'username': cookies.get("username") if cookies.get("username") else None
    }

if st.session_state.login_state['logged_in']:
    logout_button = st.sidebar.button("Logout", key="logout_button")
    if logout_button:
        st.session_state.login_state['logged_in'] = False
        st.session_state.login_state['username'] = None
        clear_login_cookies()
        st.experimental_rerun()

    st.subheader(f'Welcome {st.session_state.login_state["username"]}! :wave:')
    # authenticator.logout('Logout', 'sidebar')
    
    appName()

    custom_html = """
    <div style="position: relative; padding: 15px; border: 1px solid #4CAF50; background-color: #e7f3ea; color: #4CAF50; border-radius: 5px; display: flex; align-items: center;">
        <div style="flex: 1;">
            <span style="font-size: 18px; font-weight: bold;">✅ AudioHitAnalyzer</span><br>
            AudioHitAnalyzer predicts the popularity of songs based on user-input details such as tempo, danceability, and time signature. The app analyzes these factors to provide insights into the potential popularity of a song, helping users understand its projected impact in the music landscape.
        </div>
    </div>
    """
    st.markdown(custom_html, unsafe_allow_html=True)

    st.write("")

    if st.button("Get Started!", type="primary"):
        st.switch_page("pages/Predictions.py")

    st.title("⚙ Dashboard")
    st.divider()
    
    data = pd.read_csv("dataset/dataset.csv")
    bar_chart_data = data['key'].value_counts().reset_index()
    bar_chart_data = bar_chart_data.sort_values(by='count', ascending=False)
    scatter_chart_data = data[['tempo', 'danceability', 'time_signature']].head(100)

    col1, col2 = st.columns([2, 1])
    col1.bar_chart(bar_chart_data)
    col2.scatter_chart(scatter_chart_data)

    st.dataframe(data, use_container_width=True)

else:
    hide_sidebar_style = """
    <style>
        .ea3mdgi5 {
            padding-bottom: 0;
            padding-top: 50px !important;
            padding-left: auto;
        }
        .eczjsme18 {
            display: none !important;
        }
        .main{
            margin-right: 15rem;
            margin-left: 15rem;
        }
    </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    st.subheader("Welcome to 🎧 AudioHitAnalyzer")

    login, signup = st.tabs(["Log in", "Sign Up",])

    with login:
        
        st.header("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")

            
        if submit_button:
            if username and password:
                existing_usernames = config['credentials']['usernames'].keys()

                if username in existing_usernames:
                    stored_hashed_password = config['credentials']['usernames'].get(username, {}).get('password')

                    if stored_hashed_password:
                        if verify_password(password, stored_hashed_password):
                            st.session_state.login_state['logged_in'] = True
                            st.session_state.login_state['username'] = username 
                            set_login_cookies(username)
                            st.experimental_rerun()
                        else:
                            st.error("Invalid password")
                else:
                    st.error("Username not found")
            else:
                st.error("Please fill out all fields.")


    with signup:
        st.header("Sign Up")
        with st.form("signup_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Sign Up")

        if submit_button:
            if new_username and new_email and new_password:
                if not is_strong_password(new_password):
                    st.error("Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a number, and a special character.")
                else:
                    existing_usernames = config['credentials']['usernames'].keys()
                    existing_emails = [user['email'] for user in config['credentials']['usernames'].values()]

                    if new_username in existing_usernames:
                        st.error("Username already exists. Please choose a different username.")
                    elif new_email in existing_emails:
                        st.error("Email already exists.")
                    else:
                        hashed_new_password = hash_passwords([new_password])[0]
                        new_user_credentials = {
                            'email': new_email,
                            'name': new_username,
                            'password': hashed_new_password
                        }

                        config['credentials']['usernames'][new_username] = new_user_credentials
                        config['preauthorized']['emails'].append(new_email)

                        save_config(config)
                        st.success("User signed up successfully! Please log in.")
            else:
                st.error("Please fill out all fields.")

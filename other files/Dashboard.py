import re
import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from streamlit_authenticator.utilities.hasher import Hasher

st.set_page_config(
    layout="wide",
    page_title="AudioHitAnalyzer",
    page_icon="🎧"
)

def hash_passwords(passwords):
    return Hasher(passwords).generate()

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

config = load_config()

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('main')

if authentication_status:
    st.subheader(f'Welcome {name}! :wave:')
    authenticator.logout('Logout', 'sidebar')

    def appName():
        st.markdown("""
            <style>
                [data-testid="stSidebarNav"]::before {
                    content: "🎧 AudioHitAnalyzer";
                    margin-left: 25px;
                    font-size: 22px;
                    position: relative;
                    top: 50px;
                    font-weight: 600;
                }
            </style>
        """, unsafe_allow_html=True)
    
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
        .eczjsme11 {
            display: none !important;
        }
        .main{
            margin-right: 15rem;
            margin-left: 15rem;
        }
    </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    if authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

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
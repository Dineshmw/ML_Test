import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from streamlit_authenticator.utilities.hasher import Hasher

st.set_page_config(
    layout="wide",
    page_title ="Songs hit Predictions Application"
    )

def hash_passwords(passwords):
    return Hasher(passwords).generate()

passwords_to_hash = ['admin@123', 'user@123']
hashed_passwords = hash_passwords(passwords_to_hash)
print(hashed_passwords)

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('main')

if authentication_status:
    st.subheader(f'Welcome {name}!')
    authenticator.logout('Logout', 'sidebar')

    def add_logo():
        st.markdown("""
            <style>
                [data-testid="stSidebarNav"]::before {
                    content: "Song Hit Prediction";
                    margin-left: 25px;
                    font-size: 25px;
                    position: relative;
                    top: 50px;
                    font-weight: 600;
                }
            </style>
        """, unsafe_allow_html=True)

    data = pd.read_csv("dataset/dataset.csv")
    bar_chart_data = data['key'].value_counts().reset_index()
    bar_chart_data = bar_chart_data.sort_values(by = 'count', ascending = False)
    scatter_chart_data = data[['tempo', 'danceability', 'time_signature']].head(100)

    st.title("Dashboard")
    
    add_logo()
    col1, col2 = st.columns([2, 1])
    col1.bar_chart(bar_chart_data)
    col2.scatter_chart(scatter_chart_data)

    st.dataframe(data, use_container_width=True)

else:
    # Hide the sidebar completely on the login page
    hide_sidebar_style = """
        <style>
            [data-testid="stSidebarNav"], [data-testid="collapsedControl"], .css-1lcbmhc, .css-qri22k {
                display: none;
            }
        </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)


    if authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

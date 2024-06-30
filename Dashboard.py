import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from streamlit_authenticator.utilities.hasher import Hasher


st.set_page_config(
    layout="wide",
    page_title ="AudioHitAnalyzer",
    page_icon="🎧"
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
    st.subheader('Welcome! :wave:')
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

        

    data = pd.read_csv("dataset/dataset.csv")
    bar_chart_data = data['key'].value_counts().reset_index()
    bar_chart_data = bar_chart_data.sort_values(by = 'count', ascending = False)
    scatter_chart_data = data[['tempo', 'danceability', 'time_signature']].head(100)

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

    if st.button("Get Start!", type="primary"):
        st.switch_page("pages/Predictions.py")

    st.title("⚙ Dashboard")

    st.divider()
    
    appName()
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

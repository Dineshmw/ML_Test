import streamlit as st
import pandas as pd
import numpy as np

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

st.set_page_config(
    layout="wide",
    page_title ="Songs hit Predictions Application"
    )
st.title("Dashboard")
   
add_logo()
col1, col2 = st.columns([2, 1])

col1.bar_chart(bar_chart_data)
col2.scatter_chart(scatter_chart_data)

st.dataframe(data, use_container_width=True)

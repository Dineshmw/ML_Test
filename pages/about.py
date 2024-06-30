import streamlit as st
import pandas as pd     
from streamlit_authenticator import Authenticate
from streamlit_authenticator.utilities.hasher import Hasher
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    layout="wide",
    page_title ="About - AudioHitAnalyzer",
    page_icon="🎧"
    )

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

st.title("🔗 About")

st.divider()

st.subheader("🖥️ About App")
st.write("**AudioHitAnalyzer** predicts the popularity of songs based on user-input details such as tempo, danceability, and time signature. The app analyzes these factors to provide insights into the potential popularity of a song, helping users understand its projected impact in the music landscape.")

st.divider()

st.subheader("📊 About Dataset")

appName()
st.write("This is a dataset of Spotify tracks over a range of 125 different genres. Each track has some audio features associated with it. The data is in CSV format which is tabular and can be loaded quickly.")

st.link_button("More", "https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset")

st.divider()

st.subheader("Column Description")

st.write("**Key**: Integers map to pitches using standard Pitch Class notation. For example, E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.")
st.write("**Danceability**: Indicates how suitable a track is for dancing, based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is the least danceable, and 1.0 is the most danceable.")

st.write("**Duration**: The track length in milliseconds.")

st.write("""
**Energy**: Measures the intensity and activity of a track. Energetic tracks feel fast, loud, and noisy. This is measured from 0.0 to 1.0.
""")

st.write("""
**Mode**: Indicates the modality (major or minor) of a track. Major is represented by 1, and minor by 0.
""")

st.write("""
**Loudness**: The overall loudness of a track in decibels (dB).
""")

st.write("""
**Speechiness**: Measures the presence of spoken words in a track. A value closer to 1.0 indicates more speech-like content. Values above 0.66 likely represent tracks made entirely of spoken words. Values between 0.33 and 0.66 may contain both music and speech, either in sections or layered, such as in rap music. Values below 0.33 likely represent music and other non-speech-like tracks.
""")

st.write("""
**Acousticness**: A confidence measure from 0.0 to 1.0 indicates whether the track is acoustic. A value of 1.0 represents high confidence that the track is acoustic.
""")

st.write("**Duration**: The track length in milliseconds.")

st.write("""
**Energy**: Measures the intensity and activity of a track. Energetic tracks feel fast, loud, and noisy. This is measured from 0.0 to 1.0.
""")

st.write("""
**Mode**: Indicates the modality (major or minor) of a track. Major is represented by 1, and minor by 0.
""")

st.write("""
**Loudness**: The overall loudness of a track in decibels (dB).
""")

st.write("""
**Speechiness**: Measures the presence of spoken words in a track. A value closer to 1.0 indicates more speech-like content. Values above 0.66 likely represent tracks made entirely of spoken words. Values between 0.33 and 0.66 may contain both music and speech, either in sections or layered, such as in rap music. Values below 0.33 likely represent music and other non-speech-like tracks.
""")

st.write("""
**Acousticness**: A confidence measure from 0.0 to 1.0 indicates whether the track is acoustic. A value of 1.0 represents high confidence that the track is acoustic.
""")

st.write("""
**Instrumentalness**: Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are considered instrumental. Rap or spoken word tracks are classified as "vocal." The closer the instrumentalness value is to 1.0, the greater the likelihood that the track contains no vocal content.
""")

st.write("""
**Liveness**: Detects the presence of an audience in the recording. Higher liveness values indicate an increased probability that the track was performed live. A value above 0.8 strongly suggests the track is live.
""")

st.write("""
**Valence**: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g., happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g., sad, depressed, angry).
""")

st.write("""
**Tempo**: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo refers to the speed or pace of a piece and is derived from the average beat duration.
""")

st.write("""
**Time Signature**: An estimated time signature of the track. The time signature (meter) specifies how many beats are in each bar (or measure). The time signature ranges from 3 to 7, indicating time signatures of 3/4 to 7/4.
""")

st.write("""
**Track Genre**: The genre to which the track belongs.
""")

st.divider()

st.subheader('**Python version - 3.10**')

st.divider()

st.subheader('**Packages**')

data_df = pd.DataFrame(
    {
        "Packages": [
            ['jupyter', 'pandas', 'numpy', 'seaborn', 'matplotlib', 'statsmodels'], ['scikit-learn', 'openpyxl', 'pycaret', 'streamlit'],
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "Packages": st.column_config.ListColumn(),
    },
    hide_index=True,
)

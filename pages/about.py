import streamlit as st
import pandas as pd
from home import add_logo

st.set_page_config(
    layout="wide",
    page_title ="Songs hit Predictions Application"
    )
 
st.title("About Dataset")

add_logo()
st.write("This is a dataset of Spotify tracks over a range of 125 different genres. Each track has some audio features associated with it. The data is in CSV format which is tabular and can be loaded quickly.")

st.link_button("More", "https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset")

st.divider()

st.subheader("Column Description")

st.write("**track_id**: The Spotify ID for the track.")
st.write("**artists**: The artists' names who performed the track. If there is more than one artist, they are separated by a ;")
st.write("**album_name**: The album name in which the track appears")
st.write("**track_name**: Name of the track")
st.write("**popularity: The popularity of a track is a value between 0 and 100, with 100 being the most popular.** The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are. Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated independently. Artist and album popularity is derived mathematically from track popularity.")
st.write("**duration_ms**: The track length in milliseconds")
st.write("**explicit:** Whether or not the track has explicit lyrics (true = yes it does; false = no it does not OR unknown)")
st.write("**danceability:** Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable")
st.write("**energy:** Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale")
st.write("**key:** The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1")
st.write("**loudness:** The overall loudness of a track in decibels (dB)")
st.write("**mode:** Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0")
st.write("**speechiness:** Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks")
st.write("**acousticness:** A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic")
st.write("**instrumentalness:** Predicts whether a track contains no vocals. 'Ooh' and 'aah' sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly 'vocal'. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content")
st.write("**liveness:** Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live")
st.write("**valence:** A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)")
st.write("**tempo:** The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration")
st.write("**time_signature:** An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of 3/4, to 7/4.")
st.write("**track_genre:** The genre in which the track belongs")

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

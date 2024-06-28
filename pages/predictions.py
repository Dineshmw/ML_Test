import streamlit as st
from pycaret.classification import *
import pandas as pd
from home import add_logo


# session variables
# st.session_state.prediction_state = "";
st.session_state.fd_submit = False
st.session_state.submit = False

st.set_page_config(
    layout="wide",
    page_title ="Songs hit Predictions Application"
    )
st.title("Predictions")
add_logo()
notes_dict = {'A': 9, 'A#/Bb': 10, 'B': 11, 'C': 0, 'C#/Db': 1, 'D': 2, 'D#/Eb': 3, 'E': 4, 'F': 5, 'F#/Gb': 6, 'G': 7, 'G#/Ab': 8}

time_signatures_dict = {"3/4": 3,  "4/4": 4, "5/4": 5, "6/4": 6, "7/4": 7}

track_genre_dict = {
    'acoustic': 0, 'afrobeat': 1, 'alt-rock': 2, 'alternative': 3, 'ambient': 4,
    'anime': 5, 'black-metal': 6, 'bluegrass': 7, 'blues': 8, 'brazil': 9,
    'breakbeat': 10, 'british': 11, 'cantopop': 12, 'chicago-house': 13, 'children': 14,
    'chill': 15, 'classical': 16, 'club': 17, 'comedy': 18, 'country': 19, 'dance': 20,
    'dancehall': 21, 'death-metal': 22, 'deep-house': 23, 'detroit-techno': 24,
    'disco': 25, 'disney': 26, 'drum-and-bass': 27, 'dub': 28,
'dubstep': 29, 'edm': 30,
    'electro': 31, 'electronic': 32, 'emo': 33, 'folk': 34, 'forro': 35, 'french': 36,
    'funk': 37, 'garage': 38, 'german': 39, 'gospel': 40, 'goth': 41, 'grindcore': 42,
    'groove': 43, 'grunge': 44, 'guitar': 45, 'happy': 46, 'hard-rock': 47, 'hardcore': 48,
    'hardstyle': 49, 'heavy-metal': 50, 'hip-hop': 51, 'honky-tonk': 52, 'house': 53,
    'idm': 54, 'indian': 55, 'indie-pop': 56,
'indie': 57, 'industrial': 58, 'iranian': 59,
    'j-dance': 60, 'j-idol': 61, 'j-pop': 62, 'j-rock': 63, 'jazz': 64, 'k-pop': 65, 'kids': 66,
    'latin': 67, 'latino': 68, 'malay': 69, 'mandopop': 70, 'metal': 71, 'metalcore': 72,
    'minimal-techno': 73, 'mpb': 74, 'new-age': 75, 'opera': 76, 'pagode': 77, 'party': 78,
    'piano': 79, 'pop-film': 80, 'pop': 81, 'power-pop': 82, 'progressive-house': 83,
    'psych-rock': 84, 'punk-rock': 85, 'punk': 86, 'r-n-b': 87, 'reggae': 88, 'reggaeton': 89,
    'rock-n-roll': 90, 'rock': 91, 'rockabilly': 92, 'romance': 93, 'sad': 94, 'salsa': 95,
    'samba': 96, 'sertanejo': 97, 'show-tunes': 98, 'singer-songwriter': 99, 'ska': 100,
    'sleep': 101, 'songwriter': 102, 'soul': 103, 'spanish': 104, 'study': 105, 'swedish': 106,
    'synth-pop': 107, 'tango': 108, 'techno': 109, 'trance': 110, 'trip-hop': 111, 'turkish': 112,
    'world-music': 113}



# Function to get value from dictionary by key
def get_note_value(note):
    return notes_dict.get(note)

# Function to get value from dictionary by key
def get_time_signature_value(signature):
    return time_signatures_dict.get(signature)

# Function to get value from dictionary by key
def get_genre_value(genre):
    return track_genre_dict.get(genre)




with st.form("my_form"):
    col1, col2 = st.columns([1, 1])
    key = col1.selectbox(
    "Key",
    ('A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab'))
    danceability = col2.slider("Danceability", 0.00,1.00,0.00)

    explicit = st.toggle("Explicit")

    col1, col2 = st.columns([1, 1])
    duration = col1.number_input("Duration (Seconds)")
    enargy = col2.slider("Enargy", 0.00,1.00,0.00)

    col1, col2 = st.columns([1, 1])
    mode = col1.selectbox(
    "mode",
    ('Minor', 'Major'))
    loudness = col2.slider("Loudness", -50.00,50.00,0.00)

    col1, col2 = st.columns([1, 1])
    speechiness = col1.slider("Speechiness", 0.00,1.00,0.00)
    acousticness = col2.slider("Acousticness", 0.00,1.00,0.00)

    col1, col2 = st.columns([1, 1])
    instrumentalness = col1.slider("Instrumentalness", 0.00,1.00,0.00)
    liveness = col2.slider("Liveness", 0.00,1.00,0.00)

    col1, col2 = st.columns([1, 1])
    valence = col1.slider("Valence", 0.00,1.00,0.00)
    tempo = col2.slider("Tempo", 0.00,250.00,0.00)

    col1, col2 = st.columns([1, 1])
    time_signature = col1.selectbox(
    "Time signature",
    ('3/4', '4/4', '5/4', '6/4', '7/4'))
    track_genre = col2.selectbox(
    "Track genre",
    ('acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient',
       'anime', 'black-metal', 'bluegrass', 'blues', 'brazil',
       'breakbeat', 'british', 'cantopop', 'chicago-house', 'children',
       'chill', 'classical', 'club', 'comedy', 'country', 'dance',
       'dancehall', 'death-metal', 'deep-house', 'detroit-techno',
       'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm',
       'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk',
       'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove',
       'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle',
       'heavy-metal', 'hip-hop', 'honky-tonk', 'house', 'idm', 'indian',
       'indie-pop', 'indie', 'industrial', 'iranian', 'j-dance', 'j-idol',
       'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino',
       'malay', 'mandopop', 'metal', 'metalcore', 'minimal-techno', 'mpb',
       'new-age', 'opera', 'pagode', 'party', 'piano', 'pop-film', 'pop',
       'power-pop', 'progressive-house', 'psych-rock', 'punk-rock',
       'punk', 'r-n-b', 'reggae', 'reggaeton', 'rock-n-roll', 'rock',
       'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo',
       'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter',
       'soul', 'spanish', 'study', 'swedish', 'synth-pop', 'tango',
       'techno', 'trance', 'trip-hop', 'turkish', 'world-music'))


    submitted = st.form_submit_button("Submit")
   
if submitted:
    st.session_state.submit = True

    input_key = get_note_value(key)
    input_danceability = danceability
    if explicit == True: 
        input_explicit = 1
    else:
        input_explicit = 0
    input_duration = duration*1000
    input_enargy = enargy
    if mode == 'Minor':
        input_mode = 0
    else:
        input_mode = 1
    input_loudness = loudness
    input_speechiness = speechiness
    input_acousticness = acousticness
    input_instrumentalness = instrumentalness
    input_liveness = liveness
    input_valence = valence
    input_tempo = tempo
    input_time_signature = get_time_signature_value(time_signature)
    input_track_genre = get_genre_value(track_genre)

    #load model
    prediction_model=load_model("./Hit_song_Prediction");

    input_dict = {'duration_ms': input_duration,
'explicit': input_explicit,
'danceability': input_danceability,
'energy': input_enargy,
'key': input_key,
'loudness': input_loudness,
'mode': input_mode,
'speechiness': input_speechiness,
'acousticness': input_acousticness,
'instrumentalness': input_instrumentalness,
'liveness': input_liveness,
'valence': input_valence,
'tempo': input_tempo,
'time_signature': input_time_signature,
'track_genre': input_track_genre}
    st.session_state.input_duration = input_duration
    st.session_state.input_explicit= input_explicit
    st.session_state.input_danceability = input_danceability
    st.session_state.input_enargy = input_enargy
    st.session_state.input_key = input_key
    st.session_state.input_loudness = input_loudness
    st.session_state.input_mode = input_mode
    st.session_state.input_speechiness = input_speechiness
    st.session_state.input_acousticness = input_acousticness
    st.session_state.input_liveness = input_liveness
    st.session_state.input_instrumentalness= input_instrumentalness
    st.session_state.input_liveness= input_liveness
    st.session_state.input_valence = input_valence
    st.session_state.input_tempo = input_tempo
    st.session_state.input_time_signature = input_time_signature
    st.session_state.input_track_genre = input_track_genre

    input_df = pd.DataFrame(input_dict, index = [0])

    prediction = predict_model(prediction_model, data = input_df)
    prediction_value = round(float(prediction['prediction_label']),0)
    
    st.session_state.prediction_state = prediction_value;
    st.subheader(f"The Predicted Popularity : {st.session_state.prediction_state} %")

     

st.title("Feedback")
with st.form("feedback_form"):
    col1, col2 = st.columns([1, 1])
    
    st.session_state.feedback = col1.selectbox(
    "Are you happy with the prediction?",
    ('Yes', 'No'))
    st.session_state.comment=col1.text_input("Comment")
    
    feedback_submitted = col1.form_submit_button("Submit")

if feedback_submitted:
    st.session_state.fd_submit = True
    st.session_state.submit = True
        

if st.session_state.submit:
    if st.session_state.fd_submit:
        fd_dict = {'duration_ms': st.session_state.input_duration,
'explicit': st.session_state.input_explicit,
'danceability': st.session_state.input_danceability,
'energy': st.session_state.input_enargy,
'key': st.session_state.input_key,
'loudness': st.session_state.input_loudness,
'mode': st.session_state.input_mode,
'speechiness': st.session_state.input_speechiness,
'acousticness': st.session_state.input_acousticness,
'instrumentalness': st.session_state.input_instrumentalness,
'liveness': st.session_state.input_liveness,
'valence': st.session_state.input_valence,
'tempo': st.session_state.input_tempo,
'time_signature': st.session_state.input_time_signature,
'track_genre': st.session_state.input_track_genre,
'Prediction':st.session_state.prediction_state,
'Feedback':st.session_state.feedback,
'Feedback_Comment':st.session_state.comment}
        st.subheader("Feedback submitted");
        fd_df = pd.DataFrame(fd_dict,index=[0])
        fd_df.to_csv('dataset/feedback.csv',mode='a', header=False, index=False)

            
       
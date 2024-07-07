import streamlit as st
from pycaret.classification import *
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from streamlit_cookies_manager import EncryptedCookieManager

st.session_state.fd_submit = False
st.session_state.submit = False

st.set_page_config(
    layout="wide",
    page_title ="Predictions - AudioHitAnalyzer",
    page_icon="🎧"
    )

cookies = EncryptedCookieManager(
    prefix="my_app",
    password="111"
)

if not cookies.ready():
    st.stop()

def clear_login_cookies():
    cookies["logged_in"] = "False"
    cookies["username"] = ""
    cookies.save()

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


if st.session_state.login_state['logged_in']:
    logout_button = st.sidebar.button("Logout", key="logout_button")
    if logout_button:
        st.session_state.login_state['logged_in'] = False
        st.session_state.login_state['username'] = None
        clear_login_cookies()
        st.experimental_rerun()

    st.title("🎶 Predictions")
    appName()
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
        ('A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab'),  help="Integers map to pitches using standard Pitch Class notation. For example, E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.")
        danceability = col2.slider("Danceability", 0.00,1.00,0.00, help="Indicates how suitable a track is for dancing, based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is the least danceable, and 1.0 is the most danceable.")

        explicit = st.toggle("Explicit", help="Explicit")

        col1, col2 = st.columns([1, 1])
        duration = col1.number_input("Duration (Seconds)", help="The track length in seconds.")
        enargy = col2.slider("Energy", 0.00, 1.00, 0.00, help="Measures the intensity and activity of a track. Energetic tracks feel fast, loud, and noisy. This is measured from 0.0 to 1.0.")

        col1, col2 = st.columns([1, 1])
        mode = col1.selectbox("Mode", ('Minor', 'Major'), help="Indicates the modality (major or minor) of a track. Major is represented by 1, and minor by 0.")
        loudness = col2.slider("Loudness", -50.00, 50.00, 0.00, help="The overall loudness of a track in decibels (dB).")

        col1, col2 = st.columns([1, 1])
        speechiness = col1.slider("Speechiness", 0.00, 1.00, 0.00, help="Measures the presence of spoken words in a track. A value closer to 1.0 indicates more speech-like content. Values above 0.66 likely represent tracks made entirely of spoken words. Values between 0.33 and 0.66 may contain both music and speech, either in sections or layered, such as in rap music. Values below 0.33 likely represent music and other non-speech-like tracks.")
        acousticness = col2.slider("Acousticness", 0.00, 1.00, 0.00, help="A confidence measure from 0.0 to 1.0 indicates whether the track is acoustic. A value of 1.0 represents high confidence that the track is acoustic.")

        col1, col2 = st.columns([1, 1])
        instrumentalness = col1.slider("Instrumentalness", 0.00, 1.00, 0.00, help="Predicts whether a track contains no vocals. 'Ooh' and 'aah' sounds are considered instrumental. Rap or spoken word tracks are classified as 'vocal.' The closer the instrumentalness value is to 1.0, the greater the likelihood that the track contains no vocal content.")
        liveness = col2.slider("Liveness", 0.00, 1.00, 0.00, help="Detects the presence of an audience in the recording. Higher liveness values indicate an increased probability that the track was performed live. A value above 0.8 strongly suggests the track is live.")

        col1, col2 = st.columns([1, 1])
        valence = col1.slider("Valence", 0.00, 1.00, 0.00, help="A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g., happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g., sad, depressed, angry).")
        tempo = col2.slider("Tempo", 0.00, 250.00, 0.00, help="The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo refers to the speed or pace of a piece and is derived from the average beat duration.")

        col1, col2 = st.columns([1, 1])
        time_signature = col1.selectbox("Time Signature", ('3/4', '4/4', '5/4', '6/4', '7/4'), help="An estimated time signature of the track. The time signature (meter) specifies how many beats are in each bar (or measure). The time signature ranges from 3 to 7, indicating time signatures of 3/4 to 7/4.")
        track_genre = col2.selectbox("Track Genre", (
            'acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'brazil',
            'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 
            'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 
            'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 
            'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 
            'hip-hop', 'honky-tonk', 'house', 'idm', 'indian', 'indie-pop', 'indie', 'industrial', 'iranian', 'j-dance', 
            'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metalcore', 
            'minimal-techno', 'mpb', 'new-age', 'opera', 'pagode', 'party', 'piano', 'pop-film', 'pop', 'power-pop', 
            'progressive-house', 'psych-rock', 'punk-rock', 'punk', 'r-n-b', 'reggae', 'reggaeton', 'rock-n-roll', 'rock', 
            'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 
            'songwriter', 'soul', 'spanish', 'study', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 
            'turkish', 'world-music'), help="The genre to which the track belongs.")


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

else:
    st.switch_page("./Dashboard.py")
                

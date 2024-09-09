import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse

# Spotify API credentials
CLIENT_ID = "a477f3cc36024d5ba07065fc7543f252"
CLIENT_SECRET = "56f58122bce1425d96010beda24c0dda"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get the album cover URL of a song
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Function to recommend similar songs
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# Streamlit app header
st.header('Music Recommender System')

# Load the pre-trained models
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown for song selection
music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

# Display recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        col.text(recommended_music_names[idx])
        col.image(recommended_music_posters[idx])
        # Encode the song name for the URL
        song_url_encoded = urllib.parse.quote(recommended_music_names[idx])
        col.markdown(f"[Open in Spotify](https://open.spotify.com/search/{song_url_encoded})")

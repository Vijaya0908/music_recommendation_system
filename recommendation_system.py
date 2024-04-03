import streamlit as st
import joblib
import pandas as pd
from sklearn.cluster import KMeans

# Load the K-Means clustering model and data
clusters_new = joblib.load("D:\Recommendation System for songs\Streamlit\kmeans_model.pkl")
df = joblib.load("D:\Recommendation System for songs\Streamlit\songs_data.pkl")
data = joblib.load("D:\Recommendation System for songs\Streamlit\songs_dataset.pkl")


# Set the title and logo
st.set_page_config(
    page_title="GetaR Music Recommendation",
    page_icon="🎵",
)


st.markdown(
    f"""
    <h1 style='color: orange;'>GetaR Music Recommendation</h1>  
    """,
    unsafe_allow_html=True
)



st.markdown(
    """
    <p style='color: white;'>Welcome to the GetaR Music Recommendation system! This system helps you discover new songs similar to your favorites.</p>
    """,
    unsafe_allow_html=True
)

st.subheader("Similiar Tracks for Your Song :headphones:")

# User input for song selection
input_song = st.text_input("Enter a song name:", "")


if st.button("Get Recommendations"):
    # Function to recommend songs
    def recommend_songs(input_song, num_recommendations=10):
        input_song_cluster = df.loc[df['name'] == input_song, 'clusterid_new'].values[0]
        recommended_songs = df[df['clusterid_new'] == input_song_cluster]
        recommended_songs = recommended_songs[recommended_songs['name'] != input_song]
        recommended_songs = recommended_songs.sort_values(by='popularity', ascending=False)
        return recommended_songs[['name', 'artist']].head(num_recommendations)

    # Get recommendations
    recommendations = recommend_songs(input_song)
    st.subheader(f"Recommendations for '{input_song}':")
    st.write(recommendations)
    
  
def find_song_by_artist(artist_name):
    a = 0
    b = 0
    found_songs = []  # Create an empty list to store the found songs
    for i in data["artist_name"]:
        if artist_name.lower() in i.lower():
            found_songs.append((data["track_name"][a], data["artist_name"][a]))
            b += 1
        a += 1
    if b == 0:
        st.warning("Nothing found. Please try something else.")
    else:
        # Convert the list of found songs to a DataFrame
        found_songs_df = pd.DataFrame(found_songs, columns=["Song Name", "Artist"])

        # Display the top 10 found songs
        st.write("Songs found:")
        st.dataframe(found_songs_df.head(10))


st.subheader("Search by Artist :microphone:")

# Input for the artist's name
artist_name = st.text_input("Enter the artist's name:")

if st.button("Search"):
    if artist_name:
        find_song_by_artist(artist_name)
    else:
        st.warning("Please enter the artist's name to search for songs.")


st.subheader("Search by Genre :guitar:")
genre_input = st.text_input("Enter a genre:", "")

if st.button("Find Songs"):
    # Function to find songs by genre
    def find_songs_by_genre(genre):
        songs_in_genre = df[df[genre] == 1]
        return songs_in_genre[["name", "artist"]].head(10)

    # Find songs in the specified genre
    songs = find_songs_by_genre(genre_input)

    if songs.empty:
        st.write(f"No songs found in the genre: {genre_input}")
    else:
        st.subheader(f"Songs in the genre: {genre_input}")
        st.write(songs)
        

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #008080, #1976D2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)    
st.text("Copyright © 2023 GetaR")
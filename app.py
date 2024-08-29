import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
from dotenv import load_dotenv
import os
import pandas as pd

# Load the environment variables from the .env file
load_dotenv()

# Get the Spotify API credentials from the environment variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Initialize the Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to scrape songs from a Spotify playlist
def scrape_playlist(playlist_url):
    # Get the playlist ID from the URL
    playlist_id = playlist_url.split('/')[-1].split('?')[0]

    # Get the playlist tracks
    results = sp.playlist_tracks(playlist_id)

    # Create a CSV file to save the songs
    with open('playlist.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Song', 'Artist'])

        # Iterate over the tracks and save the song and artist names in the CSV file
        for track in results['items']:
            song_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            writer.writerow([song_name, artist_name])

        # Check if there are more tracks to retrieve
        while results['next']:
            results = sp.next(results)
            for track in results['items']:
                song_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                writer.writerow([song_name, artist_name])

    st.success('Playlist scraped and saved to playlist.csv')

    # Read the CSV file and display the playlist as a table
    with open('playlist.csv', 'r', encoding='utf-8') as csvfile:
        playlist_data = list(csv.reader(csvfile))
        header = playlist_data[0]  # Get the header row
        data = playlist_data[1:]  # Get the data rows
        df = pd.DataFrame(data, columns=header)
        st.dataframe(df)

# Streamlit app
def main():
    st.title('Spotify Playlist Scraper')

    # Input field for playlist URL
    playlist_url = st.text_input('Enter the Spotify playlist URL')

    # Scrape button
    if st.button('Scrape Playlist'):
        if playlist_url:
            scrape_playlist(playlist_url)
        else:
            st.warning('Please enter a playlist URL')

if __name__ == '__main__':
    main()

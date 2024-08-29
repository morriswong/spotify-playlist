import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Get the Spotify API credentials from the environment variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Initialize the Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to scrape songs from a Spotify playlist
def scrape_playlist(playlist_id):
    # Create a CSV file to save the songs
    with open('playlist.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Song', 'Artist'])

        # Initialize variables for pagination
        offset = 0
        limit = 100
        total = limit  # Set an initial value greater than the limit

        # Iterate until all tracks are retrieved
        while offset < total:
            # Get the playlist tracks with pagination
            results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)

            # Update the total number of tracks in the playlist
            total = results['total']

            # Iterate over the tracks and save the song and artist names in the CSV file
            for track in results['items']:
                song_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                writer.writerow([song_name, artist_name])

            # Increment the offset for the next pagination request
            offset += limit

    print('Playlist scraped and saved to playlist.csv')

# Example usage
playlist_url = input('Enter the Spotify playlist URL: ')
playlist_id = playlist_url.split('/')[-1].split('?')[0]
scrape_playlist(playlist_id)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Authenticate Spotify API
spotify_client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                              client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)


import logging
import time

def get_audio_features(title, artist):
    # Search for the song
    results = spotify.search(q=f"track:{title} artist:{artist}", limit=1, type='track')
    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        logging.info(f"Found track ID for {title} by {artist}: {track_id}")
        try:
            # Get audio features
            audio_features = spotify.audio_features([track_id])[0]
            return audio_features
        except Exception as e:
            logging.error(f"Error fetching audio features for {title} by {artist}: {e}")
            return None
    else:
        logging.warning(f"Track not found: {title} by {artist}")
        return None

# Function to handle retries with backoff to prevent 429 timeout errors
def retry_with_backoff(func, max_retries=3, initial_backoff=1, max_backoff=10):
    retries = 0
    backoff = initial_backoff
    
    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            logging.error(f"Error: {e}. Retrying in {backoff} seconds...")
            time.sleep(backoff)
            retries += 1
            backoff = min(backoff * 2, max_backoff)
    
    logging.error("Max retries reached. Unable to complete operation.")
    return None

# Open original CSV file and create a new CSV file
with open('data/train_dataset2.csv', 'r', newline='', encoding='utf-8') as csvfile, \
        open('train_spotify_dataset.csv', 'w', newline='', encoding='utf-8') as outputfile:

    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ['tempo', 'energy', 'loudness', 'danceability', 'acousticness',
                                      'instrumentalness', 'key', 'liveness', 'mode', 'speechiness',
                                      'duration_ms', 'valence']

    writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through each row in the original CSV
    for row in reader:
        # Get audio features for the song
        audio_features = get_audio_features(row['title'], row['artist'])
        if audio_features:
            # Update the row with audio features
            row.update({
                'tempo': audio_features['tempo'],
                'energy': audio_features['energy'],
                'loudness': audio_features['loudness'],
                'danceability': audio_features['danceability'],
                'acousticness': audio_features['acousticness'],
                'instrumentalness': audio_features['instrumentalness'],
                'key': audio_features['key'],
                'liveness': audio_features['liveness'],
                'mode': audio_features['mode'],
                'speechiness': audio_features['speechiness'],
                'duration_ms': audio_features['duration_ms'],
                'valence': audio_features['valence']
            })
        else:
            # If audio features are not found, fill with None values
            row.update({
                'tempo': 'no audio features found',
                'energy': None,
                'loudness': None,
                'danceability': None,
                'acousticness': None,
                'instrumentalness': None,
                'key': None,
                'liveness': None,
                'mode': None,
                'speechiness': None,
                'duration_ms': None,
                'valence': None
            })
        # Write the updated row to the new CSV file
        writer.writerow(row)

print("Data has been successfully written to spotify_data.csv")
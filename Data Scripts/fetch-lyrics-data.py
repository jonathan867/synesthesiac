import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import csv
from dotenv import load_dotenv
import os
import time

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Genius API credentials
GENIUS_API_TOKEN = os.getenv('GENIUS_API_TOKEN')

# Authenticate Spotify API
spotify_client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                              client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)

# Authenticate Genius API
genius = lyricsgenius.Genius(GENIUS_API_TOKEN)

# Playlist URI (found in the Spotify's playlist share link)
playlist_uri = '0fvS9GSbXcGqiqgvdTCDVM' 

# Open CSV file to write data
with open('song_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['song_name', 'artist_name', 'tempo', 'energy', 'loudness', 'danceability', 'lyrics',
              'acousticness', 'instrumentalness', 'key', 'liveness', 'mode', 'speechiness',
              'duration_ms', 'valence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Get tracks from the playlist
    results = spotify.playlist_tracks(playlist_uri)
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])

    # Iterate through each track
    start_time = time.time()

    start_index = 223 # input the one that the last one ended on
    count = start_index

    for track in tracks[start_index:]:

        print(count)
        count += 1

        song_name = track['track']['name']

        # Get list of artists for the track
        artists = [artist['name'] for artist in track['track']['artists']]
        artist_name = ', '.join(artists)

        # Get audio features
        audio_features = spotify.audio_features(track['track']['uri'])[0]
        tempo = audio_features['tempo']
        energy = audio_features['energy']
        loudness = audio_features['loudness']
        danceability = audio_features['danceability']
        
        acousticness = audio_features['acousticness']
        instrumentalness = audio_features['instrumentalness']
        key = audio_features['key'] # key of the song
        liveness = audio_features['liveness']
        mode = audio_features['mode'] # major: 1, minor: 0
        speechiness = audio_features['speechiness']
        duration_ms = audio_features['duration_ms']
        valence = audio_features['valence']
        
        # Get lyrics from Genius
        song = genius.search_song(song_name, artist_name)
        if song:
            lyrics = song.lyrics
        else:
            lyrics = "Lyrics not found"
        # print(lyrics)

        # Write data to CSV
        writer.writerow({'song_name': song_name,
                         'artist_name': artist_name,
                         'tempo': tempo,
                         'energy': energy,
                         'loudness': loudness,
                         'danceability': danceability,

                         'acousticness': acousticness,
                         'instrumentalness': instrumentalness,
                         'key': key,
                         'liveness': liveness,
                         'mode': mode,
                         'speechiness': speechiness,

                         'duration_ms': duration_ms,
                         'valence': valence,

                         'lyrics': lyrics,
                         })

print("Data has been successfully written to song_data.csv")
end_time = time.time()
execution_time = end_time - start_time
print("Time taken for API call:", execution_time, "seconds")

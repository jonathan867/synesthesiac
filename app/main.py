from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.Models.model import predict_emotion

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import re

app = FastAPI()

class SongInput(BaseModel): # Define request body model
    lyrics_text: str
    tempo: float
    energy: float
    loudness: float
    danceability: float
    liveness: float
    mode: int
    speechiness: float
    valence: float

class SongPredictionOut(BaseModel):
    emotion: str

class PlaylistInput(BaseModel):
    playlistURI: str
    spotifyClientId: str
    spotifyClientSecret: str
    geniusAPIToken: str

class PlaylistAnalyzeOut(BaseModel):
    percentAngry: float
    percentHappy: float
    percentRelaxed: float
    percentSad: float
    

# Endpoints

@app.get("/")
def home():
    return {"health_check": "OK"}

@app.post("/predict-song-emotion/", response_model=SongPredictionOut)
async def predict_emotion_endpoint(song_info: SongInput):
    try:
        emotion = predict_emotion(song_info.lyrics_text, song_info.tempo, song_info.energy,
                                  song_info.loudness, song_info.danceability, song_info.liveness,
                                  song_info.mode, song_info.speechiness, song_info.valence)
        return {"emotion": emotion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def extractPlaylist(clientId, clientSecret, geniusToken, playlistURI):

    spotify_client_credentials_manager = SpotifyClientCredentials(client_id = clientId,
                                                              client_secret = clientSecret)
    spotify = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)
    genius = lyricsgenius.Genius(geniusToken)

    results = spotify.playlist_tracks(playlistURI) # Get tracks from the playlist
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])

    emotionCount = {"angry": 0, "happy": 0, "relaxed": 0, "sad": 0}

    for track in tracks:
        song_name = track['track']['name']
        artists = [artist['name'] for artist in track['track']['artists']]
        artist_name = ', '.join(artists) # Get list of artists for the track

        audio_features = spotify.audio_features(track['track']['uri'])[0] # Get audio features
        tempo = audio_features['tempo']
        energy = audio_features['energy']
        loudness = audio_features['loudness']
        danceability = audio_features['danceability']
        liveness = audio_features['liveness']
        mode = audio_features['mode']
        speechiness = audio_features['speechiness']
        valence = audio_features['valence']
        
        song = genius.search_song(song_name, artist_name) # Get lyrics from Genius
        if song:
            lyrics = song.lyrics
            lyrics = re.sub(r'.*?\[.*?\].*?(\n|$)', '', lyrics) # removes all lines with [] in them, like ads
            lyrics = lyrics[:-5] # removes "Embed"
            # print(lyrics)

        if (audio_features and lyrics):
            emotion = predict_emotion(lyrics, tempo, energy, loudness, danceability, liveness, mode, speechiness, valence)
            print("          ", song_name, ": ", emotion)
            if (emotion in emotionCount):
                emotionCount[emotion] += 1
        else:
            print(song_name, " could not be found")

    print(emotionCount)
    return emotionCount

        

        
    
@app.post("/analyze-playlist/", response_model=PlaylistAnalyzeOut)
async def predict_emotion_endpoint(playlist_info: PlaylistInput):

    emotionCount = extractPlaylist(playlist_info.spotifyClientId, playlist_info.spotifyClientSecret, playlist_info.geniusAPIToken, playlist_info.playlistURI)
    print("done")
    songCount = emotionCount["angry"] + emotionCount["sad"] + emotionCount["happy"] + emotionCount["relaxed"]
    pAngry = emotionCount["angry"] /songCount
    pHappy = emotionCount["happy"] /songCount
    pRelaxed = emotionCount["relaxed"] /songCount
    pSad = emotionCount["sad"] /songCount

    return {"percentAngry": pAngry, "percentHappy": pHappy, "percentRelaxed": pRelaxed, "percentSad": pSad}



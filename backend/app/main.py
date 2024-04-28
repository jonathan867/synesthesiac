from fastapi import FastAPI, HTTPException # FastAPI imports
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.Models.model import predict_emotion

import spotipy # lyric parsing imports
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import re
import time

import nltk # NLP imports
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

import os
from openai import OpenAI

client = OpenAI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

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
    playlistName: str
    percentAngry: float
    percentHappy: float
    percentRelaxed: float
    percentSad: float
    motifs: List[str]
    storedSongs: List[dict]
    
class GenerateImageInput(BaseModel):
    playlistName: str
    percentAngry: float
    percentHappy: float
    percentRelaxed: float
    percentSad: float
    motifs: List[str]
    style: str

class GenerateImageOut(BaseModel):
    image_url: str
    
def extractNouns(text):
    
    text = re.sub(r'\[.*?\]', '', text) # Remove text within square brackets
    text = text.lower() # Convert text to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text) # Remove non-alphanumeric characters and extra whitespaces
    text = re.sub(r'\s+', ' ', text) # Replace multiple whitespaces with a single space
    tokens = word_tokenize(text)

    extraStopwords = set([
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', # numerals
        'wow', 'woah', 'yeah', 'oh', 'ooh', 'aha', 'hmm', 'uh', 'uhh', 'uhm', 'um', 'ah', 'ohh', 'woo', 'hey', 'bum', 'dum', 'mm', 'eh' # interjections
        'nothing', 'cause', '\'cause' # other common words
    ]) # filter out common song nouns that aren't motifs
    stop_words = set(stopwords.words('english')) | extraStopwords
    filteredTokens = [word for word in tokens if word.lower() not in stop_words] # Remove stopwords

    taggedTokens = pos_tag(filteredTokens) # tag each word as a part of speech
    nouns = [token for token, pos in taggedTokens if pos.startswith('NN')]
    return nouns
    
def extractPlaylist(clientId, clientSecret, geniusToken, playlistURI):

    spotify_client_credentials_manager = SpotifyClientCredentials(client_id = clientId, client_secret = clientSecret)
    spotify = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)
    genius = lyricsgenius.Genius(geniusToken)

    playlist_info = spotify.playlist(playlistURI)
    playlistName = playlist_info['name']

    results = spotify.playlist_tracks(playlistURI) # Get tracks from the playlist
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])

    emotionCount = {"angry": 0, "happy": 0, "relaxed": 0, "sad": 0}
    motifParseCount = 5 # we will only extract the nouns of the first 5 songs
    motifCounter = Counter()
    storedSongs = []

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

        retries = 3
        while retries > 0: # retry mechanism because the genius API can randomly stall and timeout sometimes
            try:
                song = genius.search_song(song_name, artist_name)
                if song:
                    lyrics = song.lyrics
                    lyrics = re.sub(r'.*?\[.*?\].*?(\n|$)', '', lyrics) # removes all lines with [] in them, like ads
                    lyrics = lyrics[:-5]
                    
                    if (audio_features and lyrics):
                        emotion = predict_emotion(lyrics, tempo, energy, loudness, danceability, liveness, mode, speechiness, valence)
                        print("          ", song_name, ": ", emotion)
                        if (emotion in emotionCount):
                            emotionCount[emotion] += 1

                            storedSongs.append({
                                'song_name': song_name,
                                'artist_name': artist_name,
                                'emotion': emotion
                            })

                        if (motifParseCount > 0): # only noun parse the first 5 songs
                            nouns = extractNouns(lyrics) # Extract nouns from lyrics
                            motifCounter.update(nouns)
                            motifParseCount -= 1
                    else:
                        print(song_name, " audio features could not be found")
                        retries -= 1
                    break  # Exit the retry loop if successful
                else:
                    print(song_name, " lyrics could not be found")
                    break
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                retries -= 1
                time.sleep(1)  # Wait for a short duration before retrying
                continue
        
        if retries == 0:
            print(f"Failed to retrieve lyrics for {song_name} after {retries} retries")

    print(emotionCount)
    # print(motifCounter)
    for key, value in motifCounter.most_common(10):
        print(key, ':', value)
    return playlistName, emotionCount, motifCounter, storedSongs


        
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
    
@app.post("/analyze-playlist/", response_model=PlaylistAnalyzeOut)
async def analyze_playlist_endpoint(playlist_info: PlaylistInput):
    # the spotify playlist must be public
    playlistName, emotionCount, motifCounter, storedSongs = extractPlaylist(playlist_info.spotifyClientId, playlist_info.spotifyClientSecret, playlist_info.geniusAPIToken, playlist_info.playlistURI)
    print("Done")
    songCount = emotionCount["angry"] + emotionCount["sad"] + emotionCount["happy"] + emotionCount["relaxed"]
    pAngry = emotionCount["angry"] /songCount
    pHappy = emotionCount["happy"] /songCount
    pRelaxed = emotionCount["relaxed"] /songCount
    pSad = emotionCount["sad"] /songCount

    motifs = [motif for motif, count in motifCounter.most_common(10)]

    return {"playlistName": playlistName, "percentAngry": pAngry, "percentHappy": pHappy, "percentRelaxed": pRelaxed, "percentSad": pSad, "motifs": motifs, "storedSongs": storedSongs}

@app.post("/generate-image/", response_model=GenerateImageOut)
async def generate_image_endpoint(playlist_info: GenerateImageInput):
    emotions = {
        "angry": playlist_info.percentAngry,
        "happy": playlist_info.percentHappy,
        "relaxed": playlist_info.percentRelaxed,
        "sad": playlist_info.percentSad
    }
    maxEmotion = max(emotions, key=emotions.get)
    color = ""

    if maxEmotion == "happy":
        color += " using bright colors"
    elif maxEmotion == "angry":
        color += " using deep colors"
    elif maxEmotion == "relaxed":
        color += " using muted and pastel colors"
    elif maxEmotion == "sad":
        color += " using darker colors with bold bursts of deep hues"

    prompt = f"Create a textless, {maxEmotion}, {playlist_info.style} titled \"{playlist_info.playlistName}\" {color}"
    
    if playlist_info.motifs:
        motifs= ", ".join(playlist_info.motifs)
        prompt += f", incorporating the motifs: {motifs}"
    print(prompt)

    response = client.images.generate( # set up API key in backend env with: export OPENAI_API_KEY=...
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url # handle error handling
    return {"image_url": image_url}

import time

start_time1 = time.time()
print("********** Importing Dependencies **********")

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import re
from sklearn.preprocessing import StandardScaler

execution_time1 = time.time() - start_time1
print("********** Imports completed in", execution_time1, " seconds **********")


start_time2 = time.time() # Load Model
print("********** Loading Model **********")
model = tf.keras.models.load_model("app/Models/song_emotion_analysis_model_v2.h5")

execution_time2 = time.time() - start_time2
print("********** Model loaded in", execution_time2, " seconds **********")


start_time3 = time.time() # Load Data Processing tools
print("********** Loading Data Processing Tools **********")
use_embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
scaler = StandardScaler()

execution_time3 = time.time() - start_time3
print("********** Tools loaded in", execution_time3, " seconds **********")

def clean_text(text):
    text = re.sub(r'\[.*?\]', '', text) # Remove text within square brackets
    text = text.lower() # Convert text to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # Remove non-alphanumeric characters and extra whitespaces
    text = text.replace('\n', ' ') # Replace line breaks with a space
    text = re.sub(r'\s+', ' ', text) # Replace multiple whitespaces with a single space
    return text.strip()

def predict_emotion(lyrics_text, tempo, energy, loudness, danceability, liveness, mode, speechiness, valence):
    cleaned_text = clean_text(lyrics_text)
    lyrics_embedding = use_embed([cleaned_text])[0]
    lyrics_embedding = np.expand_dims(lyrics_embedding, axis=0) # Reshape the lyrics embedding to include the batch axis
    numerical_features = [tempo, energy, loudness, danceability, liveness, mode, speechiness, valence]
    scaled_numerical_features = scaler.fit_transform([numerical_features])

    predictions = model.predict([lyrics_embedding, scaled_numerical_features])
    predicted_class_label = np.argmax(predictions)
    label_mapping = {0: 'angry', 1: 'happy', 2: 'relaxed', 3: 'sad'}
    return label_mapping[predicted_class_label]


# # Model Tests

# # Mean - Taylor Swift
# lyrics_text = "You, with your words like knives And swords and weapons that you use against me You have knocked me off my feet again Got me feelin' like a nothing You, with your voice like nails on a chalkboard Calling me out when I'm wounded You, pickin' on the weaker man [Pre-Chorus] Well, you can take me down With just one single blow But you don't know what you don't know [Chorus] Someday, I'll be livin' in a big ole city And all you're ever gonna be is mean Someday, I'll be big enough so you can't hit me And all you're ever gonna be is mean Why you gotta be so mean? [Verse 2] You, with your switching sides And your wildfire lies and your humiliation You have pointed out my flaws again As if I don't already see them I walk with my head down, trying to block you out 'Cause I'll never impress you I just wanna feel okay again [Pre-Chorus] I bet you got pushed around Somebody made you cold But the cycle ends right now 'Cause you can't lead me down that road And you don't know what you don't know [Chorus] Someday, I'll be livin' in a big ole city And all you're ever gonna be is mean Someday, I'll be big enough so you can't hit me And all you're ever gonna be is mean Why you gotta be so mean? [Bridge] And I can see you years from now in a bar Talking over a football game With that same big, loud opinion, but nobody's listening Washed up and ranting about the same ole bitter things Drunk and grumbling on about how I can't sing But all you are is mean [Buildup] All you are is mean And a liar, and pathetic And alone in life, and mean And mean, and mean, and mean [Chorus] But someday, I'll be livin' in a big ole city And all you're ever gonna be is mean, yeah Someday, I'll be big enough so you can't hit me And all you're ever gonna be is mean Why you gotta be so mean? Someday, I'll be livin' in a big ole city (Why you gotta be so mean?) And all you're ever gonna be is mean (Why you gotta be so mean?) Someday, I'll be big enough so you can't hit me (Why you gotta be so mean?) And all you're ever gonna be is mean Why you gotta be so mean?"
# tempo = 163.874
# energy = 0.692
# loudness = -3.866
# danceability = 0.524
# liveness = 0.192
# mode = 1
# speechiness = 0.0369
# valence = 0.621

# emotion = predict_emotion(lyrics_text, tempo, energy, loudness, danceability, liveness, mode, speechiness, valence)
# print(emotion)

# Hally's Comet - Billie Eilish
# lyrics_text = '''I don't want it And I don't want to want you 
#                  But in my dreams I seem to be more honest And I must admit, you've been in quite a few 
#                  Halley's Comet Comes around more than I do But you're all it takes for me to break a promise 
#                  Silly me to fall in love with you 
#                  I haven't slept since Sunday Midnight for me is 3:00 a.m. for you 
#                  But my sleepless nights are better With you than nights could ever be alone, ooh-ooh-ooh 
#                  I was good at feeling nothing, now I'm hopeless 
#                  What a drag to love you like I do, ooh-ooh, ooh, ooh Ooh-ooh-ooh, ooh, ooh-ooh, ooh 
#                  I've been loved before, but right now in this moment I feel more and more like I was made for you 
#                  For you 
                 
#                  I'm sitting in my brother's room 
#                  Haven't slept in a week or two, or two 
#                  I think I might have fallen in love 
#                  What am I to do?'''
# emotion = predict_emotion(lyrics_text, 72.38, 0.159, -16.728, 0.403, 0.34, 0, 0.104, 0.0381)
# print(emotion)
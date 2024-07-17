import numpy as np
from sklearn.neighbors import NearestNeighbors
import random

def get_song_features(sp, song_id):
    features = sp.audio_features(song_id)[0]
    feature_vector = [features['danceability'], features['energy'], features['key'], features['loudness'], features['mode'], features['speechiness'], features['acousticness'], features['instrumentalness'], features['liveness'], features['valence'], features['tempo']]
    return np.array(feature_vector)

def fetch_user_top_tracks_features(sp):
    results = sp.current_user_top_tracks(limit=50)
    tracks = results['items']
    track_ids = [track['id'] for track in tracks]
    features = np.array([get_song_features(sp, track_id) for track_id in track_ids])
    return track_ids, features

def train_model(features):
    model = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(features)
    return model

def recommend_song(model, context, track_ids, features):
    context_features = generate_context_features(context)
    distances, indices = model.kneighbors(context_features)
    recommended_song_ids = [track_ids[idx] for idx in indices[0]]
    return recommended_song_ids

def generate_context_features(context):
    mood_mapping = {'happy': 0.8, 'sad': 0.2, 'energetic': 0.9, 'calm': 0.3}
    location_mapping = {'home': 0.5, 'work': 0.6, 'gym': 0.8, 'party': 0.9}
    time_of_day_mapping = {'morning': 0.7, 'afternoon': 0.6, 'evening': 0.5, 'night': 0.4}
    day_of_week_mapping = {'weekday': 0.5, 'weekend': 0.7}
    energy_level_mapping = {'low': 0.2, 'medium': 0.5, 'high': 0.8}

    # Creating a context feature vector with the same number of features as the song features
    context_features = np.array([
        mood_mapping[context['mood']],      # mood influences danceability
        energy_level_mapping[context['energy_level']], # energy influences energy
        5,                                  # placeholder for key
        -5,                                 # placeholder for loudness
        1 if context['mood'] in ['happy', 'energetic'] else 0,  # mode
        0.1,                                # placeholder for speechiness
        location_mapping[context['location']],  # location influences acousticness
        0.1,                                # placeholder for instrumentalness
        0.3,                                # placeholder for liveness
        mood_mapping[context['mood']],      # mood influences valence
        120                                 # placeholder for tempo
    ])
    return context_features.reshape(1, -1)

def generate_description(song):
    adjectives = ["upbeat", "melodic", "rhythmic", "smooth", "intense", "relaxing", "energetic", "calming"]
    return random.choice(adjectives)

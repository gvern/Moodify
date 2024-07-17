import numpy as np
from sklearn.neighbors import NearestNeighbors

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
    context_features = np.random.rand(1, 11)
    distances, indices = model.kneighbors(context_features)
    recommended_song_ids = [track_ids[idx] for idx in indices[0]]
    return recommended_song_ids

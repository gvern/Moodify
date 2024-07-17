from flask import request, jsonify, current_app as app, send_from_directory

from .auth import get_spotify_client
from .context import get_user_context
from .models import fetch_user_top_tracks_features, train_model, recommend_song

sp = get_spotify_client()
track_ids, features = fetch_user_top_tracks_features(sp)
model = train_model(features)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    context = get_user_context()
    recommended_song_ids = recommend_song(model, context, track_ids, features)
    recommended_songs = [sp.track(song_id) for song_id in recommended_song_ids]
    recommendations = [{'name': song['name'], 'artist': song['artists'][0]['name']} for song in recommended_songs]
    return jsonify(recommendations)

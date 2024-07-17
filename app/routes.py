from flask import request, jsonify, current_app as app, send_from_directory
import random

from .auth import get_spotify_client
from .context import get_user_context
from .models import fetch_user_top_tracks_features, train_model, recommend_song, generate_description

sp = get_spotify_client()
track_ids, features = fetch_user_top_tracks_features(sp)
model = train_model(features)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    mood = request.args.get('mood', 'happy')
    location = request.args.get('location', 'home')
    time_of_day = request.args.get('time_of_day', 'morning')
    day_of_week = request.args.get('day_of_week', 'weekday')
    energy_level = request.args.get('energy_level', 'medium')
    
    context = get_user_context()
    context['mood'] = mood
    context['location'] = location
    context['time_of_day'] = time_of_day
    context['day_of_week'] = day_of_week
    context['energy_level'] = energy_level
    
    recommended_song_ids = recommend_song(model, context, track_ids, features)
    recommended_songs = [sp.track(song_id) for song_id in recommended_song_ids]
    recommendations = [{'name': song['name'], 'artist': song['artists'][0]['name'], 'description': generate_description(song)} for song in recommended_songs]
    return jsonify(recommendations)

# imports
from flask import Flask ,render_template, request, redirect, url_for, jsonify
import sys
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
from dotenv import load_dotenv
import os
import random

load_dotenv()  # This loads the variables from the .env file into the environment
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')



def checkNumberOfTracks(numOfTracks):
    '''Check and sanitize user input for an int value, validate int is between 0 and 50.'''
    if type(numOfTracks) is not int:
        try: # convert into int, return False otherwise
            numOfTracks = int(numOfTracks)
        except(ValueError):
            print("Your input is not an integer.\n\n")
            return False

    if ((numOfTracks <= 0) or (numOfTracks > 50)):
        print("Number of tracks must be at least 1, but cannot exceed 50.\n\n")
        return False
    return True

'''
User Playback
inputs: 
    numOfTracks: represents number of songs a user can read of their past listening history
    - can only return between 1 and 50 tracks
return:
    trackDetails: a list of details about a track. included info is order number, title, artist name
'''
def userPlayback(numOfTracks):
    authorizationScope = 'user-read-recently-played'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=authorizationScope))
    print('Your ' + str(numOfTracks) + ' last listened to tracks: ') # direct cast of track number to a string to concatenate it
    results = sp.current_user_recently_played(limit=numOfTracks, after=None)
    trackDetails = []
    for i, item in enumerate(results['items']):
        trackDetails.append({
            'track_number': i + 1,
            'track_name': item['track']['name'],
            'artist_name': item['track']['artists'][0]['name'],
            'album_art' : item['track']['album']['images'][0]['url']
        })
    return trackDetails

'''
User Top Tracks
inputs:
    numOfTracks: numOfTracks: represents number of songs a user can read of their past listening history
    - can only return between 1 and 50 tracks
return:
    trackDetails: a list of details about a track. included info is order number, title, artist name
'''
def userTopTracks(numOfTracks, time_range):
    authorizationScope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=authorizationScope))

    if time_range == 'Short Term':
        results = sp.current_user_top_tracks(time_range='short_term', limit=numOfTracks)
    elif time_range == 'Past 6 months':
        results = sp.current_user_top_tracks(time_range='medium_term', limit=numOfTracks)
    elif time_range == 'All time':
        results = sp.current_user_top_tracks(time_range='long_term', limit=numOfTracks)
    else:
        return []  # Return an empty list if the time_range is invalid

    trackDetails = []
    for i, item in enumerate(results['items']):
        trackDetails.append({
            'track_number': i + 1,
            'track_name': item['name'],
            'artist_name': item['artists'][0]['name'],
            #'album_art' : item['track']['album']['images'][0]['url']
            'album_art': item['album']['images'][0]['url']
        })
    return trackDetails
    
'''
User Top Artists
inputs:
    numOfTracks: numOfTracks: represents number of songs a user can read of their past listening history
    - can only return between 1 and 50 tracks
return:
    trackDetails: a list of details about a track. included info is order number, title, artist name
'''
def userTopArtists(numOfArtists, time_range):
    authorizationScope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=authorizationScope))
        
    if time_range == 'Short Term':
        results = sp.current_user_top_artists(time_range='short_term', limit=numOfArtists)
    elif time_range == 'Past 6 months':
        results = sp.current_user_top_artists(time_range='medium_term', limit=numOfArtists)
    elif time_range == 'All time':
        results = sp.current_user_top_artists(time_range='long_term', limit=numOfArtists)
    else:
        return []  # Return an empty list if the time_range is invalid
        
    artistDetails = []
    for i, item in enumerate(results['items']):
        artistDetails.append({
                'artist_name': item['name'],
                'artist_art': item['images'][0]['url']
            })            
    # print(artistDetails)
    return artistDetails

def trackSuggestion(numOfTracks, time_range):
    authorizationScope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=authorizationScope))
    
    if time_range == 'Short Term':
        results = sp.current_user_top_tracks(time_range='short_term', limit=numOfTracks)
    elif time_range == 'Past 6 months':
        results = sp.current_user_top_tracks(time_range='medium_term', limit=numOfTracks)
    elif time_range == 'All time':
        results = sp.current_user_top_tracks(time_range='long_term', limit=numOfTracks)
    else:
        return []  # Return an empty list if the time_range is invalid

    trackURIList = []
    revisedTrackURIList = []

    for item in results['items']:
        trackURIList.append(item['uri'])

    randomURI = random.sample(trackURIList, min(5, len(trackURIList)))
    revisedTrackURIList.extend(randomURI)

    recommendedSongs = sp.recommendations(seed_tracks=revisedTrackURIList, limit=numOfTracks)

    trackDetails = []
    for i, item in enumerate(recommendedSongs['tracks']):
        trackDetails.append({
            'track_number': i + 1,
            'track_name': item['name'],
            'artist_name': item['artists'][0]['name'],
            #'album_art' : item['track']['album']['images'][0]['url']  
            'album_art': item['album']['images'][0]['url']
        })
    return trackDetails


app = Flask(__name__)


@app.route('/', methods = ['GET','POST'])
def menu():
    return render_template('menu.html')

@app.route('/listeninghistory', methods=['GET'])
def listening_history():
    return render_template('listeningHistory.html')


@app.route('/displayListeningHistory', methods=['GET'])
def display_listening_history():
    numOfTracks = request.args.get('numOfTracks', type=int)
    tracks = userPlayback(numOfTracks)
    return render_template('displayListeningHistory.html', tracks=tracks)#, jsonify(tracks)

@app.route('/toptracks', methods = ['GET'])
def top_tracks():
    return render_template('topTracks.html')

@app.route('/displaytoptracks', methods = ['GET'])
def display_top_tracks():
    numOfTracks = request.args.get('numOfTracks', type = int)
    time_range = request.args.get('time_range', type = str)
    tracks = userTopTracks(numOfTracks, time_range)
    return render_template('displayTopTracks.html', tracks = tracks)#, jsonify(tracks)

@app.route('/topartists', methods = ['GET'])
def top_artists():
    return render_template('topArtists.html')

@app.route('/displayTopArtists', methods = ['GET'])
def display_top_artists():
    numOfArtists = request.args.get('numOfArtists', type = int)
    time_range = request.args.get('time_range', type= str)
    artists = userTopArtists(numOfArtists, time_range)
    return render_template('displayTopArtists.html', artists = artists)

@app.route('/tracksuggestions', methods=['GET'])
def track_suggestion():
    return render_template('trackSuggestion.html')

@app.route('/displayTrackSuggestions', methods = ['GET'])
def display_track_suggestions():
    numOfTracks = request.args.get('numOfTracks', type= int)
    time_range = request.args.get('time_range', type= str)
    tracks = trackSuggestion(numOfTracks, time_range)
    return render_template('displayTrackSuggestions.html', tracks = tracks)#, jsonify(tracks)

# Shows the top artists for a user
import spotipy
from spotipy.oauth2 import SpotifyOAuth

'''shows top artists for myself, in 3 different time ranges
'''
# topArtistsAndTrackScope = 'user-top-read'
playbackScope = 'user-read-recently-played'
# ranges = ['short_term', 'medium_term', 'long_term']

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=topArtistsAndTrackScope))
# print('Top artists:/n')
# for sp_range in ['short_term', 'medium_term', 'long_term']:
#     print("range:", sp_range)

#     results = sp.current_user_top_artists(time_range=sp_range, limit=50)

#     for i, item in enumerate(results['items']):
#         print(i, item['name'])
#     print()
# print playback
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=playbackScope)) 
results = sp.current_user_recently_played(limit=50, after=None, before=None)
print('Recent Listening')
results = sp.current_user_recently_played(limit=20, after=None)
for i, item in enumerate(results['items']):
    #print(i, item['track']['name']['artist'])
    # vs
     print(i, item['track']['name'], "-", item['track']['artists'][0]['name'])
print()
'''
shows led zeppelin audio samples and cover art for top ten tracks
'''
# from spotipy.oauth2 import SpotifyClientCredentials
# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
# results = spotify.artist_top_tracks(lz_uri)

# for track in results['tracks'][:10]:
#     print('track    : ' + track['name'])
#     print('audio    : ' + track['preview_url'])
#     print('cover art: ' + track['album']['images'][0]['url'])
#     print()
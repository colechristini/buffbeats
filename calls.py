import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yaml


with open('keys.yml', 'r') as file:
    keys = yaml.safe_load(file)

client_id = keys["SPOTIFY_CLIENT_ID"]  
client_secret = keys["SPOTIFY_CLIENT_ID"]

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='_',
                                                                              client_secret='_'))

def getUri(s):
    return spotify.playlist(playlist_id=s, additional_types=('track',))['tracks']

results = getUri('https://open.spotify.com/playlist/2kTwuQqA8VlSFXVKwHB3sf?si=179e53d5ffc94b31')

sections = []

for idx, item in enumerate(results['items']):
    track = item['track']
    seggs = spotify.audio_analysis(track['uri'])['sections']
    sections.append((seggs[0], seggs[-1]))






def printPlaylist(finalOrder):
    for idx, _ in enumerate(results['items']):
        track = results['items'][finalOrder[idx]]['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])


def makePlaylist(finalOrder, user):
    woohoo = spotify.user_playlist_create(user=user, public=True, collaborative=False, description='')
    tracks = []
    for idx, _ in enumerate(results['items']):
        tracks.append(results['items'][finalOrder[idx]]['track'])
    spotify.user_playlist_add_tracks(user=user, playlist_id=woohoo, position=0, tracks=tracks)

# ###Making the playlist
# #let's assume we have the finished songs - put it in the following array
# finalOrder = []

# woohoo = spotify.user_playlist_create(user = "dummy account", name='best playlist ever',
#                             public=True, collaborative=False, description='here ya go')

# for song in finalOrder:
#     spotify.playlist_add_items(playlist_id=woohoo[id], items=finalOrder)


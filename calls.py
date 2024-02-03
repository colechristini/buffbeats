import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

### Replace this with the user's uri i think
playlist_uri = 'get this shit from them'
########


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

##### Getting the damn songs and info
songs = spotify.playlist_tracks(playlist_id = playlist_uri, limit=200)

songSegments = []
for song in songs:
    first = spotify.audio_analysis(track_id=song[id])['sections'][0]
    last = spotify.audio_analysis(track_id=song[id])['sections'][-1]
    songSegments.append((first, last))






###Making the playlist
#let's assume we have the finished songs - put it in the following array
finalOrder = []

woohoo = spotify.user_playlist_create(user = "dummy account", name='best playlist ever',
                            public=True, collaborative=False, description='here ya go')

for song in finalOrder:
    spotify.playlist_add_items(playlist_id=woohoo[id], items=finalOrder)


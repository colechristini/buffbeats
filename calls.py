import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

playlist_uri = 'spotify:playlist:2kTwuQqA8VlSFXVKwHB3sf'


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='02fb254044ab46459048afd12ccb39ec',
                                                                              client_secret='ba0d5a9e1b2a42c294c404520abe0e00'))
results = spotify.playlist(playlist_id=playlist_uri, additional_types=('track',))['tracks']

sections = []
for idx, item in enumerate(results['items']):
    track = item['track']
    seggs = spotify.audio_analysis(track['uri'])['sections']
    sections.append((seggs[0], seggs[-1]))









# ###Making the playlist
# #let's assume we have the finished songs - put it in the following array
# finalOrder = []

# woohoo = spotify.user_playlist_create(user = "dummy account", name='best playlist ever',
#                             public=True, collaborative=False, description='here ya go')

# for song in finalOrder:
#     spotify.playlist_add_items(playlist_id=woohoo[id], items=finalOrder)


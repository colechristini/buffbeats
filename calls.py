import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

playlist_uri = 'spotify:playlist:2kTwuQqA8VlSFXVKwHB3sf'


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='02fb254044ab46459048afd12ccb39ec',
                                                                              client_secret='ba0d5a9e1b2a42c294c404520abe0e00'))
results = spotify.playlist(playlist_id=playlist_uri, additional_types=("track"))

print(results.keys())
# ### Replace this with the user's uri i think
# playlist_uri = 'get this shit from them'
# ########

# ##### Getting the damn songs and info
# songs = spotify.playlist_tracks(playlist_id = playlist_uri, limit=200)

# songSections = []
# for song in songs:
#     first = spotify.audio_analysis(track_id=song[id])['sections'][0]
#     last = spotify.audio_analysis(track_id=song[id])['sections'][-1]
#     songSections.append((first, last))






# ###Making the playlist
# #let's assume we have the finished songs - put it in the following array
# finalOrder = []

# woohoo = spotify.user_playlist_create(user = "dummy account", name='best playlist ever',
#                             public=True, collaborative=False, description='here ya go')

# for song in finalOrder:
#     spotify.playlist_add_items(playlist_id=woohoo[id], items=finalOrder)


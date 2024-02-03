import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yaml
from algo import processPlaylist


with open('keys.yml', 'r') as file:
    keys = yaml.safe_load(file)

client_id = keys["SPOTIFY_CLIENT_ID"]  
client_secret = keys["SPOTIFY_CLIENT_ID"]

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='_',
                                                                              client_secret='_'))

def getUri(s):
    return spotify.playlist(playlist_id=s, additional_types=('track',))['tracks']


# Takes in list of segments and returns tuple of segments
# corresponding to intro and outro sections
# Inputs: The list of segments for the song, the length of the intro section,
# and the length of the outro section.
# Outputs: A tuple containing the list of intro segments and the list of
# outro segments.
def get_segments(segments, intro_length, outro_length):
    intro_segments = []
    outro_segments = []
    accumulated_time_intro = 0
    intro_index = 0
    # Get segments corresponding to intro
    while accumulated_time_intro < intro_length:
        accumulated_time_intro += segments[intro_index]['duration']
        intro_segments.append(segments[intro_index])
        intro_index += 1
    accumulated_time_outro = 0
    outro_index = len(segments) - 1
    # Get segments corresponding to outro
    while accumulated_time_outro < outro_length:
        accucumulated_time_outro += segments[outro_index]['duration']
        outro_segments.append(segments[outro_index])
        outro_index -= 1
    return (intro_segments,outro_segments)

def getSongs(uris):
    songs = []
    for _, item in enumerate(uris['items']):
        track = item['track']
        aa = spotify.audio_analysis(track['uri'])
        secs = aa['sections']
        segs = aa['segments']
        intro = secs[0]
        outro = secs[-1]
        intro_segments, outro_segments = get_segments(segs, intro['duration'], outro['duration'])
        songs.append((intro, intro_segments, outro, outro_segments))
    return songs


def printPlaylist(finalOrder, results):
    for idx, _ in enumerate(results['items']):
        track = results['items'][finalOrder[idx]]['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])


def makePlaylist(finalOrder, user, results):
    woohoo = spotify.user_playlist_create(user=user, public=True, collaborative=False, description='')
    tracks = []
    for idx, _ in enumerate(results['items']):
        tracks.append(results['items'][finalOrder[idx]]['track'])
    spotify.user_playlist_add_tracks(user=user, playlist_id=woohoo, position=0, tracks=tracks)


def main():
    results = getUri('https://open.spotify.com/playlist/2kTwuQqA8VlSFXVKwHB3sf?si=179e53d5ffc94b31')
    songs = getSongs(results)
    finalOrder = processPlaylist(songs, 10)
    printPlaylist(finalOrder, results)


    
main()
    
# ###Making the playlist
# #let's assume we have the finished songs - put it in the following array
# finalOrder = []

# woohoo = spotify.user_playlist_create(user = "dummy account", name='best playlist ever',
#                             public=True, collaborative=False, description='here ya go')

# for song in finalOrder:
#     spotify.playlist_add_items(playlist_id=woohoo[id], items=finalOrder)


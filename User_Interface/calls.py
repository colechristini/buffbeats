import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yaml
from algo import processPlaylist


with open('keys.yml', 'r') as file:
    keys = yaml.safe_load(file)

client_id = keys["SPOTIFY_CLIENT_ID"]  
client_secret = keys["SPOTIFY_CLIENT_SECRET"]

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id,
                                                                              client_secret=client_secret))

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
        accumulated_time_outro += segments[outro_index]['duration']
        outro_segments.append(segments[outro_index])
        outro_index -= 1
    return (intro_segments,outro_segments)

def getSongs(uris):
    songs = []
    for idx, item in enumerate(uris['items']):
        track = item['track']
        print(idx, f'{track["artists"][0]} - {track["name"]}')
        aa = spotify.audio_analysis(track['uri'])
        secs = aa['sections']
        segs = aa['segments']
        intro = secs[0]
        outro = secs[-1]
        intro_segments, outro_segments = get_segments(segs, intro['duration'], outro['duration'])
        songs.append((intro, intro_segments, outro, outro_segments))
    return songs


def printPlaylist(finalOrder, results):
    songsInOrder = []
    for idx, _ in enumerate(results['items']):
        track = results['items'][finalOrder[idx]]['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
        songsInOrder.append(''.join((idx, track['artists'][0]['name'], " – ", track['name'])))
    return songsInOrder


def makePlaylist(finalOrder, user, results):
    play = spotify.user_playlist_create(user=user, public=True, collaborative=False, description='')
    id, url = play['id'], play['external_urls']['spotify']
    tracks = []
    for idx, _ in enumerate(results['items']):
        tracks.append(results['items'][finalOrder[idx]]['track'])
    spotify.user_playlist_add_tracks(user=user, playlist_id=id, position=0, tracks=tracks)
    return url


def call(url):
    results = getUri(url)
    songs = getSongs(results)
    finalOrder = processPlaylist(songs, 10)
    return printPlaylist(finalOrder, results)

    
# ###Making the playlist
# #let's assume we have the finished songs - put it in the following array
# finalOrder = []

# woohoo = spotify.user_playlist_create(user = "dummy account", name='best playlist ever',
#                             public=True, collaborative=False, description='here ya go')

# for song in finalOrder:
#     spotify.playlist_add_items(playlist_id=woohoo[id], items=finalOrder)


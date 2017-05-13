
import spotipy
import sys
import spotipy.util as util

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print "   %d %32.32s %s \t%s" % (i, track['artists'][0]['name'],
            track['name'], track['id'])


scope = 'playlist-read-private playlist-modify-private'


username = "danlon96"
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
         if playlist['name'] == "Discover Weekly":
            print
            print playlist['name']
            print '  total tracks', playlist['tracks']['total']
            results = sp.user_playlist("spotify", playlist['id'],
                fields="tracks,next,id")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)

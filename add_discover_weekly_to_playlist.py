import spotipy
import sys
import spotipy.util as util

scope = 'playlist-read-private playlist-modify-private'

username = "danlon96"
token = util.prompt_for_user_token(username, scope)

def get_track_list(tracks):
    track_list = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_list.append(track['id'])
    return track_list

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists("danlon96")
    compilation_playlist = None
    discover_weekly_playlist = None

    for playlist in playlists['items']:
        if playlist['name'] == "Discover Weekly" and playlist['owner']['id'] == "spotify":
            discover_weekly_playlist = playlist
        if playlist['name'] == "Discover Weekly Compilation" and playlist['owner']['id'] == username:
            compilation_playlist = playlist

    if discover_weekly_playlist == None:
        print ("Error: Cannot find Discover Weekly playlist. Please make sure"
                "you are following it.")

    else:
        if compilation_playlist == None:
            compilation_playlist = sp.user_playlist_create(username,
                    "Discover Weekly Compilation", False)
            print "Created new Discover Weekly Compilation playlist."

        dw_tracks_raw = sp.user_playlist("spotify", discover_weekly_playlist['id'],
                fields="tracks")['tracks']
        compilation_tracks_raw = sp.user_playlist(username, compilation_playlist['id'],
                fields="tracks")['tracks']

        dw_track_list = get_track_list(dw_tracks_raw)
        c_track_list = get_track_list(compilation_tracks_raw)

        tracks_to_add = [ x for x in dw_track_list if x not in c_track_list]

        if tracks_to_add:
            sp.user_playlist_add_tracks(username, compilation_playlist['id'], tracks_to_add)
            print "Successfully added tracks."
        else:
            print "No tracks to add."
else:
    print "Failed to retrieve token."

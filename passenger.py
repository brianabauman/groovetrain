import socket
import sys
import time

import spotipy
from util import util

#constants
HOST = "localhost"
PORT = 8000

#parse arguments
if len(sys.argv) == 2:
    username = sys.argv[1]
else:
    util.log("Usage: python %s username" % sys.argv[0])
    sys.exit()

#determine necessary scope and authorize
scope = util.gatherScope()
sp = util.promptAuth(username, scope)

while (True):
	#make request to conductor server
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	    sock.connect((HOST, PORT))
	    responseArr = sock.recv(1024).strip().split("|")
	    conductorTrackURI = responseArr[0]
	    conductorTrackProgressMS = int(responseArr[1])
	except KeyboardInterrupt:
		pass
	finally:
	    sock.close()

	#gather passenger's current track info
	currentTrack = sp.current_user_playing_track()
	if (currentTrack != None):
		currentTrackURI = util.propertyToString(currentTrack["item"]["uri"])
		currentTrackProgressMS = int(util.propertyToString(currentTrack["progress_ms"]))
	else:
		currentTracURI = "none"
		currentTrackProgressMS = 0

	#decide if/how to update the passenger's playback
	if (conductorTrackURI != currentTrackURI):
		#switch passenger to conductor's track
		conductorTrackName = util.propertyToString(sp.track(conductorTrackURI)["name"])
		util.log("Conductor is playing a different track, switching you to %s..." % conductorTrackName)
		sp.start_playback(uris=[ conductorTrackURI ])
		sp.seek_track(conductorTrackProgressMS)

	elif (abs(conductorTrackProgressMS - currentTrackProgressMS) >= 10000):
		#sync up the passenger if they're more than 10 seconds delayed
		util.log("Resyncing you with the conductor...")
		sp.seek_track(conductorTrackProgressMS)

	else:
		util.log("You're synced with the Conductor!")
		
	#wait 30 seconds, then check again.
	time.sleep(5)





import SocketServer
import sys

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

#define request handler
class Handler(SocketServer.BaseRequestHandler):
	def handle(self):
		currentTrack = sp.current_user_playing_track()
		currentTrackURI = util.propertyToString(currentTrack["item"]["uri"])
		currentTrackProgressMS = util.propertyToString(currentTrack["progress_ms"])

		util.log("Request made, responding with: %s|%s" % (currentTrackURI, currentTrackProgressMS))
		self.request.sendall("%s|%s\n" % (currentTrackURI, currentTrackProgressMS))

#create server and bind to port
server = SocketServer.TCPServer((HOST, PORT), Handler)
try:
	server.serve_forever()
except KeyboardInterrupt:
	pass
server.server_close()








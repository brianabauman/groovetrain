import json
import datetime

import spotipy.util

class util:
	@staticmethod
	def promptAuth(username, scope):
		#authorize the conductor
		token = spotipy.util.prompt_for_user_token(username,
			                               scope,
			                               client_id='0ebd3ef528a3403dbe9ab44eed6a727a',
			                               client_secret='4a36c9d01a4542c292de20ec90f967bf',
			                               redirect_uri='http://localhost/')

		if token:
		    return spotipy.Spotify(auth=token)
		else:
		    print "Can't get token for %s." % username
		    sys.exit()

	@staticmethod
	def gatherScope():
		#determine necessary scope
		return (
			"user-read-playback-state "
			#+ "user-read-currently-playing "
			#+ "user-modify-playback-state  "	
			+ "streaming "
			#+ "app-remote-control "
			#+ "playlist-read-collaborative "
			#+ "playlist-modify-private  "
			#+ "playlist-modify-public  "
			#+ "playlist-read-private "
			#+ "user-read-birthdate "
			#+ "user-read-email "
			#+ "user-read-private "
			#+ "user-follow-modify "
			#+ "user-follow-read "	
			#+ "user-library-read "
			+ "user-library-modify "
			+ "user-read-recently-played "
			#+ "user-top-read ")
		).strip()

	@staticmethod
	def propertyToString(s):
		return json.dumps(s).strip().replace('"', '')

	@staticmethod
	def log(message):
		print "[%s] %s" % (str(datetime.datetime.now()), message)

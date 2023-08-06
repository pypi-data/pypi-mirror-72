import re
import json
import urllib.request
import urllib.parse
import urllib.error

from castberry.youtube.resolvers.iresolver import IResolver
from castberry.youtube.video import VideoInfo

# Constants
LINK_GET_VIDEO_INFO = "http://youtube.com/get_video_info"


class ResGVI(IResolver):
	"""
	Retrieves video info from youtube.com/get_video_info
	It's a fast method but fails on copyrighted videos
	"""

	def get_video_info(self, video_id):
		# Also possible:
		# video_details = player_response["videoDetails"]
		# video_title = video_details["title"]
		# and captions, cards, endscreen etc...

		try:
			with urllib.request.urlopen(
					LINK_GET_VIDEO_INFO + "?video_id=" + video_id
			) as connection:
				response_bytes = connection.read()
				response_string = response_bytes.decode('utf-8')
				response_decoded = urllib.parse.unquote(response_string).split("&")
				response = dict()
				for item in response_decoded:
					name, data = item.split("=", 1)
					response[name] = data
		except urllib.error.URLError as urle:
			raise KeyError("Could not get response for video_id " + video_id + ": " + str(urle))

		if response["status"] != "ok":
			raise KeyError("Received bad response for video_id " + video_id)

		player_response = json.loads(response["player_response"])

		if player_response["playabilityStatus"]["status"] != "OK":
			raise KeyError("Video is unavailable for video_id " + video_id)

		# Replaces the last repeating + to a space
		# "Test+Video++Title" -> "Test Video+ Title"
		title = re.sub("(?!.\\+)\\+", " ", player_response["videoDetails"]["title"])

		video_formats = player_response["streamingData"]["formats"]
		best_video = max(video_formats, key=lambda video: video["bitrate"])

		return VideoInfo(
			title=title,
			source=best_video["url"]
		)

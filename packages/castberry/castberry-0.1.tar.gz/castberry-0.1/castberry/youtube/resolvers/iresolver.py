class IResolver:
	"""
	A resolver converts a youtube video id to video info: video stream link, duration, etc...
	"""

	def get_video_info(self, video_id):
		"""
		Convert a video id to youtube.video.VideoInfo

		:param video_id: The id of the video
		:type video_id: str

		:return: Information about the video
		:rtype: castberry.youtube.video.VideoInfo

		:raises KeyError: If information about the video could not be retrieved
		"""
		raise NotImplementedError

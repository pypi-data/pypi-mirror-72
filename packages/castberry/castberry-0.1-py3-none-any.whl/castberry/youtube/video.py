from queue import Queue
from threading import Thread


class VideoInfo:
	"""
	A container for information about the video
	Not to be initialized anywhere but in resolvers
	"""
	title = None
	source = None

	def __init__(self, title, source):
		"""
		:param title: Title of the video
		:type title: str

		:param source: MRL of the video
		:type source: str
		"""
		self.title = title
		self.source = source


class Video:
	"""
	A "container" for video info. Only stores the video_id.
	Attempts to get video info when asked.
	On initialization starts a thread to get video info asynchronously.
	"""

	video_id = None
	__video_info = None
	__q_video_info = None

	def __init__(self, video_id, iresolver):
		"""
		:param video_id: The id of the video
		:type video_id: str

		:param iresolver: Video id to video info resolver
		:type iresolver: castberry.youtube.resolvers.iresolver.IResolver
		"""
		self.video_id = video_id
		self.__q_video_info = Queue()
		Thread(
			target=self._t_resolve_video_info,
			args=[iresolver]
		).start()

	def _t_resolve_video_info(self, iresolver):
		"""
		:param iresolver: Video id to video info resolver
		:type iresolver: castberry.youtube.resolvers.iresolver.IResolver
		"""
		try:
			self.__q_video_info.put(iresolver.get_video_info(self.video_id))
		except KeyError as ke:
			self.__q_video_info.put(ke)

	def get_video_info(self):
		"""
		Returns information about the video

		:return: Information about the video
		:rtype: VideoInfo

		:raises KeyError: When the resolver could not retrieve information about the video
		"""
		if self.__video_info is None:
			# Wait for resolver to finish
			self.__video_info = self.__q_video_info.get()

		if isinstance(self.__video_info, KeyError):
			raise self.__video_info

		return self.__video_info

class IPlayer:
	""" A media player interface """
	_qplaylist = None

	def __init__(self, qplaylist):
		"""
		:param qplaylist: Playlist command queue
		:type qplaylist: castberry.playlist.QPlaylist
		"""
		self._qplaylist = qplaylist

	@property
	def source(self):
		"""
		The media to play
		:return: Media resource locator
		:rtype: str | None
		"""
		raise NotImplementedError

	@source.setter
	def source(self, mrl):
		"""
		Sets the media to play
		:param mrl: Media resource locator
		:type mrl: str
		"""
		raise NotImplementedError

	@property
	def position(self):
		"""
		Returns the current media playback position
		:return: Track position in milliseconds
		:rtype: int | None
		"""
		raise NotImplementedError

	@position.setter
	def position(self, position):
		"""
		Sets the current media playback position of the player
		:param position: Track position in milliseconds
		:type position: int
		"""
		raise NotImplementedError

	@property
	def volume(self):
		"""
		Returns the current volume of the player
		:return: A number from 0 to 100
		:rtype: int | None
		"""
		raise NotImplementedError

	@volume.setter
	def volume(self, volume):
		"""
		Sets the volume of the player
		:param volume: A number from 0 to 100
		:type volume: int
		"""
		raise NotImplementedError
	
	@property
	def duration(self):
		"""
		Returns the length of the currently playing media
		:return: Total length in milliseconds
		:rtype: int | None
		"""
		raise NotImplementedError

	def play(self):
		"""
		Start media playback from where it stopped,
		Do not pause if it's playing already.
		"""
		raise NotImplementedError

	def pause(self):
		"""
		Pause the playback
		"""
		raise NotImplementedError

	def show_text(self, message, timeout):
		"""
		Displays a message for a period of time

		:param message: The message to display
		:type message: str

		:param timeout: How long to display it for, in milliseconds
		:type timeout: int
		"""
		raise NotImplementedError

	def _finished(self):
		"""
		Signals the playlist that the player has done playing a video.
		"""
		self._qplaylist.send("cb_iplayer_finished")

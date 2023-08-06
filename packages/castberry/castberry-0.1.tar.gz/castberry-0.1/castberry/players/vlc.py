import vlc
import time
from castberry.players.iplayer import IPlayer


class VLC(IPlayer):
	"""
	VLC media player realized as an IPlayer.
	Requires python-vlc
	https://www.videolan.org/
	https://pypi.org/project/python-vlc/
	"""

	__instance = None
	__player = None

	def __init__(self, qplaylist, splash_screen=None):
		"""
		Initializes the player and displays the given splash screen, if any

		:param qplaylist: Playlist command queue
		:type qplaylist: castberry.playlist.QPlaylist

		:param splash_screen: The media to display on initialization
		:type splash_screen: str
		"""
		super().__init__(qplaylist)
		# Start VLC
		self.__instance = vlc.Instance("--play-and-pause --sub-source marq --verbose=-1")
		self.__player = self.__instance.media_player_new()
		# Player settings
		self.__player.set_fullscreen(True)
		self.__player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, vlc.Position.Bottom)
		self.__player.video_set_marquee_int(vlc.VideoMarqueeOption.Y, 20)
		# Attach IPlayer's _e_finished to the vlc player's finished event.
		self.__player.event_manager().event_attach(vlc.EventType.MediaPlayerPaused, self._e_finished)
		# NOTE: see _e_finished
		# # # self.__player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self._t_finished)

		# Display the splash screen, if given
		if splash_screen is not None:
			self.source = splash_screen
			self.play()
			self.pause()

	def _e_finished(self, event):
		"""
		Signals the playlist that the player has done playing the current media.
		NOTE: Not an ideal solution:
		vlc.Event.Type.MediaPlayerEndReached does not fire
		if flag --play-and-pause is set, so I had to resort to this.

		:param event: VLC Event
		:type event: vlc.Event
		"""
		# Assuming this is fired on MediaPlayerPaused.
		# Check if the video has been paused approximately at the end, if so - signal.
		if self.position >= self.duration-500:
			self._finished()

	@property
	def source(self):
		media = self.__player.get_media()
		return None if media is None else media.get_mrl()

	@source.setter
	def source(self, mrl):
		self.__player.set_mrl(mrl)
		# VLC displays the last text on the new source. This prevents displaying that last text.
		self.show_text("", 0)

	@property
	def position(self):
		# VLC returns the position as a ratio of position/duration.
		duration = self.duration
		position = self.__player.get_position()
		# Interface returns milliseconds
		return duration*position

	@position.setter
	def position(self, position):
		# VLC requires the position as a ratio of position/duration.
		duration = self.duration
		self.__player.set_position(float(position)/duration)

	@property
	def volume(self):
		# Sleep needed here because VLC tends to
		# prioritize returning current volume
		# even when it's being set
		time.sleep(0.5)
		return self.__player.audio_get_volume()

	@volume.setter
	def volume(self, volume):
		self.__player.audio_set_volume(volume)

	@property
	def duration(self):
		return self.__player.get_length()

	def play(self):
		self.__player.play()

	def pause(self):
		self.__player.pause()

	def show_text(self, message, timeout):
		self.__player.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, timeout)
		self.__player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, message)

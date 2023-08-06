import logging
import json
import time
from queue import Queue
from threading import Thread
from castberry.youtube.video import Video

# region Constants
# These are arbitrary, defined by youtube
STATE_PLAY = 1
STATE_PAUSE = 2
STATE_NOW = 3
# IPlayer.show_text timeouts (ms)
TIMEOUT_PAIRING_INFO = 8000
TIMEOUT_TEXT = 2000
TIMEOUT_MCS = 500  # MCS = Media Control Symbols
# endregion


# region Static Functions
def _s_to_ms(seconds):
	"""
	Converts seconds to milliseconds

	:param seconds: Seconds to convert
	:type: int | float | long

	:return: Seconds as milliseconds
	:rtype: int | float | long
	"""
	return seconds * 1000


def _ms_to_s(milliseconds):
	"""
	Converts milliseconds to seconds

	:param milliseconds: milliseconds to convert
	:type: int | float | long

	:return: milliseconds as seconds
	:rtype: int | float | long
	"""
	return int(milliseconds / 1000)


def _format_pairing_code(pairing_code):
	"""
	Formats a string so that after every three characters a dash is added.
	E.g. _format_pairing_code(123456789) = 123-456-789

	:param pairing_code: The string to format
	:type pairing_code: str

	:return: A string with a dash after every third character
	:rtype: str
	"""
	return '-'.join(pairing_code[i:i + 3] for i in range(0, len(pairing_code), 3))
# endregion


class QPlaylist:
	"""
	A queue wrapper, to send commands to the playlist
	"""
	__q_playlist = Queue()

	def get(self):
		"""
		:return:
		:rtype: (str, dict)
		"""
		return self.__q_playlist.get()

	def send(self, command, data=None):
		"""
		:param command:
		:type command: str

		:param data:
		:type data: dict | None
		"""
		self.__q_playlist.put((command, data))


class Playlist:
	"""
	A link between youtube and a video player.
	Receives the commands from youtube (via QPlaylist),
	controls the player, keeps track of the playlist,
	and sends responses back to youtube (via QCast) accordingly.
	"""
	__qplaylist = None
	__qcast = None
	__iresolver = None
	__iplayer = None

	__videos = None
	__current_id = None
	__state = None
	__list_id = None
	__list_ctt = None
	__remote_count = None
	__pairing_info = None

	def __init__(self, qplaylist, qcast, iresolver, iplayer):
		"""
		Initialize the playlist

		:param qplaylist: Playlist command queue
		:type qplaylist: QPlaylist

		:param qcast: Cast send thread command queue, for sending data
		:type qcast: castberry.youtube.cast.QCast

		:param iresolver: Video id to video info resolver
		:type iresolver: castberry.youtube.resolvers.iresolver.Iresolver

		:param iplayer: A video player
		:type iplayer: castberry.players.iplayer.IPlayer
		"""
		self.__qplaylist = qplaylist
		self.__qcast = qcast
		self.__iresolver = iresolver
		self.__iplayer = iplayer

		self.__videos = []
		self.__state = STATE_PAUSE
		self.__remote_count = 0

	def t_listen(self):
		""" Playlist listener thread. Fetches commands from the command queue and executes them """
		while True:
			command, data = self.__qplaylist.get()
			logging.debug(f"Received command \"{command}\" with data: {data}")

			if command == "cb_cast_pairing_info":
				self.__pairing_info = data
				Thread(target=self._t_show_pairing_info).start()
			elif command == "cb_iplayer_finished":
				self._play_next()
			elif command == "remoteConnected":
				self.__remote_count += 1
				self.__iplayer.show_text(data["name"] + " connected", TIMEOUT_TEXT)
			elif command == "remoteDisconnected":
				self.__remote_count = 0 if self.__remote_count == 1 else self.__remote_count - 1
				self.__iplayer.show_text(data["name"] + " disconnected", TIMEOUT_TEXT)
				Thread(target=self._t_show_pairing_info).start()
			elif command == "loungeStatus":
				devices = json.loads(data["devices"])
				for device in devices:
					if device["type"] == "REMOTE_CONTROL":
						# NOTE: Does not check by unique ID, might have duplicates
						self.__remote_count += 1
						self.__iplayer.show_text(device["name"] + " connected", TIMEOUT_TEXT)
			elif command == "play":
				self.__state = STATE_PLAY
				self.__iplayer.play()
				self._send_state_info()
				self.__iplayer.show_text("▶", TIMEOUT_MCS)
			elif command == "pause":
				self.__state = STATE_PAUSE
				self.__iplayer.pause()
				self._send_state_info()
				self.__iplayer.show_text("⏸", TIMEOUT_MCS)
			elif command == "stopVideo":
				# Nothing, let the video play while changing sources?
				# self.__iplayer.show_text("⏹", TIMEOUT_MCS)
				pass
			elif command == "next":
				self._play_next()
				self.__iplayer.show_text("⏭", TIMEOUT_MCS)
			elif command == "previous":
				self._play_previous()
				self.__iplayer.show_text("⏮", TIMEOUT_MCS)
			elif command == "seekTo":
				# Save the current position for comparison
				old_position = self.__iplayer.position
				# Set the new pos and send info
				new_position = _s_to_ms(int(data["newTime"]))
				self.__iplayer.position = new_position
				self._send_state_info()
				# Display whether seeked forwards or backwards
				self.__iplayer.show_text("⏩" if new_position > old_position else "⏪", TIMEOUT_MCS)
			elif command == "getVolume":
				self._send_volume_info()
			elif command == "setVolume":
				volume_new = int(data["volume"])
				self.__iplayer.volume = volume_new
				self.__iplayer.show_text(f"🔊 {volume_new}", TIMEOUT_MCS)
				self._send_volume_info()
			elif command == "getNowPlaying":
				self._send_now_playing()
			elif command == "setPlaylist":
				self.__list_id = data["listId"]
				self.__list_ctt = data["ctt"]

				video_ids = data["videoIds"].split(",") if "videoIds" in data else []
				self._sync_playlists(video_ids)

				self.__current_id = int(data["currentIndex"])
				self._play_current()
			elif command == "updatePlaylist":
				event_details = json.loads(data["eventDetails"])
				video_ids = data["videoIds"].split(",") if "videoIds" in data else []

				if event_details["eventType"] == "VIDEO_ADDED" and self.__current_id is None:
					# If a video has been added before receiving a setPlaylist command
					self.__current_id = 0

				self._sync_playlists(video_ids)
			elif command == "dpadCommand":
				# UP DOWN LEFT RIGHT ENTER BACK
				key = data["key"]
				if key == "UP":
					self._show_pairing_info()
			elif command == "noop":
				# nothing
				pass
			elif command == "getSubtitlesTrack":
				# TODO find out what this is for
				pass
			elif command == "onUserActivity":
				# nothing
				pass
			else:
				logging.warning("Playlist received unknown command: " + command)

	def _t_show_pairing_info(self):
		"""
		Keeps showing the pairing info until a remote connects
		"""
		while self.__remote_count == 0:
			if self.__state == STATE_PAUSE:
				self._show_pairing_info()
				time.sleep(TIMEOUT_PAIRING_INFO/1000)

	# region Control methods
	def _play_next(self):
		"""
		Play the next video, if there's any.
		If no video is selected, the first one plays
		"""
		if self.__current_id is not None:
			if self.__current_id + 1 < len(self.__videos):
				self.__current_id += 1
				self._play_current()
		else:
			self.__current_id = 0
			self._play_current()

	def _play_previous(self):
		"""
		Play the previous video, if the current one isn't the first
		If no video is selected, the first one plays
		"""
		if self.__current_id is not None:
			if self.__current_id - 1 > 0:
				self.__current_id -= 1
				self._play_current()
		else:
			self.__current_id = 0
			self._play_current()

	def _play_current(self):
		"""
		Attempts to play the current video.
		"""
		try:
			current_video = self._get_current_video()
		except KeyError:
			logging.warning("Tried to start the current video, but no video selected")
			return

		try:
			current_video_info = current_video.get_video_info()
		except KeyError as ve:
			logging.error("Video could not be played: " + str(ve))
			self.__iplayer.show_text("Video unavailable", TIMEOUT_TEXT)
			return

		self.__iplayer.source = current_video_info.source
		self.__iplayer.play()
		self.__iplayer.show_text(current_video_info.title, TIMEOUT_TEXT)
		self.__state = STATE_PLAY
		# Inform that a new video is playing
		self._send_now_playing()
		# Inform that the player's state has changed (to playing)
		self._send_state_info()

	def _get_current_video(self):
		"""
		Returns the currently selected video

		:return: Current video
		:rtype: castberry.youtube.video.Video

		:raises KeyError: When there's no video playing
		"""
		if self.__current_id is not None:
			try:
				return self.__videos[self.__current_id]
			except IndexError:
				raise KeyError("Current video is not in playlist")
		else:
			raise KeyError("Current video id is not set")

	def _show_pairing_info(self):
		"""
		Displays the screen name and pairing code via the player
		"""
		name = self.__pairing_info["name"]
		code = _format_pairing_code(self.__pairing_info["code"])
		self.__iplayer.show_text(f"{name}\n{code}", TIMEOUT_PAIRING_INFO)

	def _sync_playlists(self, video_ids):
		"""
		Creates a new video list based on given video_ids and updates the current_id.
		Does not discard videos from the old list that exist in the new list.
		This is needed to avoid resolving video info multiple times for the same video,
		assuming the old list and the new list contain some videos with the same ids

		:param video_ids: A list of new videos/video ids
		:type video_ids: List[str]
		"""
		if len(video_ids) < 1:
			self.__videos = []
			self.__current_id = None
		else:
			# Get current_video video_id for updating the current_id later
			current_video_id = None
			try:
				current_video = self._get_current_video()
				current_video_id = current_video.video_id
			except KeyError:
				# No video playing
				pass
			# Create a synced playlist
			playlist_old = self.__videos
			playlist_new = []
			for new_video_id in video_ids:
				# Check if video already exists
				found_video = None
				for video in playlist_old:
					if video.video_id == new_video_id:
						found_video = video
						break
				# If video already exists, keep it, else create a new one
				if found_video is not None:
					playlist_new.append(found_video)
				else:
					playlist_new.append(Video(new_video_id, self.__iresolver))
			# Update current video id
			if current_video_id is not None:
				try:
					# Update the current video id
					self.__current_id = playlist_new.index(current_video_id)
				except ValueError:
					# Current video was removed
					self.__current_id = 0
			self.__videos = playlist_new
	# endregion

	# region Youtube communication via QCast
	def _send_state_info(self):
		"""
		Sends information about the player's playback, via QCast
		"""
		position = self.__iplayer.position
		if position is not None:
			duration = self.__iplayer.duration
			if duration is not None:
				self.__qcast.send_on_state_change(
					_ms_to_s(position),
					self.__state,
					_ms_to_s(duration),
				)

	def _send_volume_info(self):
		"""
		Sends information about the player's volume, via QCast
		"""
		player_volume = self.__iplayer.volume
		if player_volume is not None:
			self.__qcast.send_on_volume_changed(
				player_volume,
				player_volume == 0
			)

	def _send_now_playing(self):
		"""
		Sends information about the current status of the playlist
		"""
		try:
			current_video = self._get_current_video()
		except KeyError:
			self.__qcast.send_now_playing_empty()
			return

		position = self.__iplayer.position
		# This might be wrong but I prioritize sending...
		if position is None:
			position = 0
		# ...currently playing info over the correct position

		self.__qcast.send_now_playing(
			current_video.video_id,
			_ms_to_s(position),
			self.__list_ctt,
			self.__list_id,
			self.__current_id,
			self.__state
		)
	# endregion

import json
import urllib.parse
import urllib.request
from queue import Queue


# region Constants
LINK_GEN_SCREEN_ID = "https://www.youtube.com/api/lounge/pairing/generate_screen_id"
LINK_GET_LOUNGE_TOKEN = "https://www.youtube.com/api/lounge/pairing/get_lounge_token_batch"
LINK_LOUNGE_BIND = "http://www.youtube.com/api/lounge/bc/bind"
LINK_GET_PAIRING_CODE = "https://www.youtube.com/api/lounge/pairing/get_pairing_code"
# endregion


# region Static functions
def get_screen_id():
	"""
	Requests a unique screen id from the api

	:return: A screen id string
	:rtype: str
	"""
	with urllib.request.urlopen(LINK_GEN_SCREEN_ID) as connection:
		return connection.read().decode("utf-8")


def _generate_lounge_token(screen_id):
	"""
	Generates an api lounge token for the screen
	Or adds a screen to the lounge? Documentation? None.

	:param str screen_id: The screen id
	:type screen_id: str

	:return: A lounge token string
	:rtype: str

	:raises ValueError: When the response does not contain a token for the screen
	"""
	with urllib.request.urlopen(
			LINK_GET_LOUNGE_TOKEN,
			data=_encode_dict_for_post({"screen_ids": screen_id})
	) as connection:
		connection_string = connection.read().decode("utf-8")
		connection_json = json.loads(connection_string)

		for screen_data in connection_json["screens"]:
			if screen_data["screenId"] == screen_id:
				return screen_data["loungeToken"]
		raise ValueError("No lounge token received for given screen id")


def _encode_dict_for_post(post_values):
	"""
	Converts a dictionary to bytes, for sending it through POST.

	:param post_values: A dict of values to encode
	:type post_values: dict

	:return: The dict as bytes ready for POST
	:rtype: bytes
	"""
	return urllib.parse.urlencode(post_values).encode('ascii')


def _read_cte(connection):
	"""
	https://en.wikipedia.org/wiki/Chunked_transfer_encoding

	:param connection: The open http connection
	:type connection: http.client.HTTPResponse

	:return: The received message chunk as a dict
	:rtype: dict
	"""
	# Read the bytes representing the length of the message
	message_length_bytes = bytearray()
	byte = connection.read(1)
	while byte != str.encode('\n'):
		message_length_bytes += byte
		byte = connection.read(1)
	message_length_string = message_length_bytes.decode("utf-8")
	message_length = int(message_length_string)
	# Read the message itself
	message = connection.read(message_length)
	message_string = message.decode("utf-8")
	return json.loads(message_string)
# endregion


class QCast:
	"""
	A queue wrapper, to send commands to the send thread
	"""
	__q_cast = Queue()

	def get(self):
		"""
		:return: The command and data to send
		:rtype: (str,dict)
		"""
		return self.__q_cast.get()

	def send_now_playing(self, video_id, current_time, ctt, list_id, current_id, state):
		"""
		Sends information about the current status of the player and playlist

		:param video_id: Current video id
		:type video_id: str

		:param current_time: Current player position in seconds
		:type current_time: int

		:param ctt: No idea
		:type ctt: str

		:param list_id: Current playlist id
		:type list_id: str

		:param current_id: The position of the current video in the playlist
		:type current_id: int

		:param state: An arbitrary integer representing a player's state
		:type state: int
		"""
		self.__q_cast.put((
			"nowPlaying",
			{
				"videoId": video_id,
				"currentTime": current_time,
				"ctt": ctt,
				"listID": list_id,
				"currentIndex": current_id,
				"state": state,
			}
		))

	def send_now_playing_empty(self):
		"""
		Same as send_now_playing, except for when there's no video playing
		"""
		self.__q_cast.put(("nowPlaying", {}))

	def send_on_state_change(self, current_time, state, duration, cpn="foo"):
		"""
		Sends information about the new status of the player

		:param current_time: Current player position in seconds
		:type current_time: int

		:param state: An arbitrary integer representing a player's state
		:type state: int

		:param duration: Current video duration in seconds
		:type duration: int

		:param cpn: No idea
		:type cpn: str
		"""
		self.__q_cast.put((
			"onStateChange",
			{
				"currentTime": current_time,
				"state": state,
				"duration": duration,
				"cpn": cpn,
			}
		))

	def send_on_volume_changed(self, volume, muted):
		"""
		Sends information about the player's volume

		:param volume: Current player volume in the range of 0 to 100
		:type volume: float

		:param muted: Whether sound is muted or not
		:type muted: bool
		"""
		self.__q_cast.put((
			"onVolumeChanged",
			{
				"volume": volume,
				"muted": muted,
			}
		))


class Cast:
	"""
	A link between youtube and the playlist.
	Receives the commands from youtube and passes it on to the playlist.
	Also sends data to youtube via QCast
	"""
	__qcast = None
	__qplaylist = None
	__cast_info = None

	def __init__(self, qcast, qplaylist, screen_id, screen_name, screen_app):
		"""
		Initializes the session with youtube, gets initial data.

		:param qcast: Send thread command queue
		:type qcast: QCast

		:param qplaylist Playlist command queue
		:type qplaylist: castberry.playlist.QPlaylist

		:param screen_id: Screen id
		:type screen_id: str

		:param screen_name: Screen name
		:type screen_name: str

		:param screen_app: Screen app name
		:type screen_app: str
		"""
		self.__qcast = qcast
		self.__qplaylist = qplaylist
		# Get lounge token
		lounge_token = _generate_lounge_token(screen_id)
		# Set up session info
		self.__cast_info = {
			"device": "LOUNGE_SCREEN",
			"id": screen_id,
			"name": screen_name,
			"app": screen_app,
			"loungeIdToken": lounge_token,
			"theme": "cl",
			"capabilities": {},
			"mdx-version": "2",
			"VER": "8",
			"v": "2",
			"RID": "1337",
			"AID": "42",
			"zx": "xxxxxxxxxxxx",
			"t": "1",
		}
		# Get initial data
		with urllib.request.urlopen(
				self._prepare_get_link(LINK_LOUNGE_BIND),
				_encode_dict_for_post({"count": "0"})
		) as connection:
			response = _read_cte(connection)
			self._process_response(response)
		self.__cast_info["RID"] = "rpc"
		self.__cast_info["CI"] = "0"
		self.send_pairing_info()

	def send_pairing_info(self):
		""" Sends the information needed for pairing to the playlist """
		self.__qplaylist.send(
			"cb_cast_pairing_info",
			{
				"code": self._get_pairing_code(),
				"name": self.__cast_info["name"]
			}
		)

	def t_listen(self):
		""" Waits for commands from youtube """
		with urllib.request.urlopen(
				self._prepare_get_link(LINK_LOUNGE_BIND)
		) as connection:
			while True:
				response = _read_cte(connection)
				self._process_response(response)

	def t_send(self):
		""" Sends commands from QCast to youtube """
		offset = 0
		while True:
			command, data = self.__qcast.get()
			# Prepare link : Making a copy of cast info would be inefficient?
			# This works so I'm not gonna change it
			self.__cast_info["RID"] = "1337"
			link = self._prepare_get_link(LINK_LOUNGE_BIND)
			self.__cast_info["RID"] = "rpc"
			# Prepare post data
			post_values = {
				"count": "1",
				"ofs": offset,
				"req0__sc": command
			}
			for key in data:
				post_values["req0_" + key] = data[key]
			# Send it
			urllib.request.urlopen(
				link, _encode_dict_for_post(post_values)
			)
			offset += 1

	def _process_response(self, response):
		"""
		Extracts the command and it's data from the message received from youtube.
		Processes session information, passes anything else onto the QPlaylist.
		:param response: The received response
		:type response: dict
		"""
		for index, message in response:
			command = message[0]
			data = message[1] if len(message) > 1 else None
			if command == "c":
				self.__cast_info["SID"] = data
			elif command == "S":
				self.__cast_info["gsessionid"] = data
			else:
				self.__qplaylist.send(command, data)

	def _prepare_get_link(self, link):
		"""
		Appends the information about the current session to the given link

		:param link: The link
		:type link: str

		:return: The link with the appropriate get arguments
		:rtype str:
		"""
		return link + "?" + urllib.parse.urlencode(self.__cast_info)

	def _get_pairing_code(self):
		"""
		Requests the pairing code for this session

		:return: The pairing code
		:rtype: str
		"""
		post_values = {
			"screen_id": self.__cast_info["id"],
			"screen_name": self.__cast_info["name"],
			"app": self.__cast_info["app"],
			"lounge_token": self.__cast_info["loungeIdToken"],
			"access_type": "permanent",
		}
		with urllib.request.urlopen(
				LINK_GET_PAIRING_CODE + "?ctx=pair",
				data=_encode_dict_for_post(post_values)
		) as connection:
			return connection.read().decode("utf-8")

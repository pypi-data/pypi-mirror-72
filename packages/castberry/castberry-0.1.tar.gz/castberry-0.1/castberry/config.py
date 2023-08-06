import logging
import os
import platform
from pathlib import Path
from shutil import which
from configparser import ConfigParser

# Default values
DEFAULT_SCREEN_NAME = "CastberryTV"
DEFAULT_SCREEN_APP = "CastberryApp"
DEFAULT_PLAYERS = ["vlc"]
DEFAULT_RESOLVERS = ["resgvi", "youtube-dl"]
DEFAULT_SPLASH_SCREEN = str(Path(__file__).parent.absolute() / "resources/splash_screen.png")


# region Static functions
def _get_config_file():
	"""
	Attempts to get a config file from user's config folder.
	If config folder doesn't have a project folder, it creates it.
	If config file doesn't exist, creates an empty one.

	:return: Path to the config file
	:rtype: str
	"""
	if "APPDATA" in os.environ:
		config_home = Path(os.environ["APPDATA"])
	elif "XDG_CONFIG_HOME" in os.environ:
		config_home = Path(os.environ["XDG_CONFIG_HOME"])
	else:
		os_home = os.environ["HOME"]
		config_home = Path(os_home) / ".config"

	config_folder = config_home / "castberry"
	config_folder.mkdir(parents=False, exist_ok=True)

	config_file = config_folder / "config.ini"
	if not config_file.exists():
		logging.warning(f"Config file will be created because it does not exist at {config_file}")
		config_file.touch()
	return str(config_file)


def _get_player(player_name, qplaylist, path_splash_screen):
	"""
	Returns a player if it is supported

	:param player_name: The name of the player
	:type player_name: str

	:param qplaylist: Playlist command queue for the player
	:type qplaylist: castberry.playlist.QPlaylist

	:param path_splash_screen: Path to the splash screen for the player to display at first
	:type path_splash_screen: str

	:return: The player as IPlayer
	:rtype: castberry.players.iplayer.IPlayer

	:raises EnvironmentError: If player is not supported
	"""
	if player_name == "vlc":
		if which("vlc") is not None:
			from castberry.players.vlc import VLC
			return VLC(qplaylist, path_splash_screen)
		elif platform.system() == "Windows":
			# TODO find a way to check if VLC exists in windows
			from castberry.players.vlc import VLC
			return VLC(qplaylist, path_splash_screen)
	# elif player_name == "future_player":
	# 	if "future player" is "supported":
	# 	from players.future_player import FuturePlayer
	# 	return FuturePlayer(qplaylist)
	raise EnvironmentError("Player " + player_name + " is not supported by the current environment")


def _get_resolver(resolver_name):
	"""
	Returns a resolver if it is supported

	:param resolver_name:
	:type: str

	:return: A resolver
	:rtype: castberry.youtube.resolvers.iresolver.Iresolver

	:raises EnvironmentError: If the resolver is not supported
	"""
	if resolver_name == "resgvi":
		# Resgvi does not depend on anything, so always supported
		from castberry.youtube.resolvers.resgvi import ResGVI
		return ResGVI()
	elif resolver_name == "youtube-dl":
		if which("youtube-dl"):
			from castberry.youtube.resolvers.resytdl import ResYTDL
			return ResYTDL()
	raise EnvironmentError("Resolver " + resolver_name + " is not supported by the current environment")
# endregion


class Config:
	__file_path = None
	__parser = None

	def __init__(self):
		self.__file_path = _get_config_file()
		self.__parser = ConfigParser(allow_no_value=True)
		self.__parser.read(self.__file_path)
		logging.info("Ready to read config file: " + self.__file_path)

	# region Utility methods
	def _save_changes(self):
		"""
		Opens the config file and writes the values from __parser
		"""
		with open(self.__file_path, "w", newline="\n") as config_file:
			self.__parser.write(config_file)

	def _ensure_section_exists(self, section):
		"""
		Adds a section to the config, if it doesn't exit already.

		:param section: The name of the section
		:type section: str
		"""
		if not self.__parser.has_section(section):
			self.__parser.add_section(section)

	def _save_value(self, section, option, value):
		"""
		Sets a value in the config file.

		:param section: The name of the section the key is in
		:type section: str

		:param option: The name of the key
		:type option: str

		:param value: The value to set it to
		:type value: str
		"""
		self._ensure_section_exists(section)
		self.__parser.set(section, option, value)
		self._save_changes()

	def _save_section_keys(self, section, keys):
		"""
		Adds all the keys to the section, if they don't exist already.

		:param section: The name of the section
		:type section: str

		:param keys: The names of the keys to add
		:type keys: List[str]
		"""
		self._ensure_section_exists(section)
		for key in keys:
			self.__parser.set(section, key)
		self._save_changes()

	def _get_string_val(self, section, key, default):
		"""
		Attempts to get 'key' value from a 'section' in the config file.
		If not found, returns default, and saves it to the config file.

		:param section: Section in the config file
		:type section: str

		:param key: Key to look for
		:type key: str

		:param default: Default value to save and return if not found
		:type default: str

		:return: The value in the config file or default
		:rtype: str
		"""
		try:
			key_value = self.__parser[section][key]
			if len(key_value) > 0:
				return key_value
			else:
				warning_message = "Config file does not have a " + key + " specified."
		except KeyError:
			warning_message = "Config file does not have an entry for " + key

		logging.warning(warning_message + " Using the default: " + default)
		self._save_value(section, key, default)
		return default
	# endregion

	# region Config values getters
	def get_screen_id(self):
		"""
		Attempts to get the screen_id value from the config file.
		If it doesn't exist, generates a new one and saves it.
		:return: A screen ID either from the config file, or generated
		:rtype: str
		"""
		section = "Cast"
		key = "screen_id"
		try:
			screen_id = self.__parser[section][key]
			if len(screen_id) > 0:
				return screen_id
			else:
				logging.warning("Config file does not have a " + key + "specified. A new one will be generated.")
		except KeyError:
			logging.warning("Config file does not have an entry for " + key + ". A new one will be generated.")

		from castberry.youtube.cast import get_screen_id
		screen_id = get_screen_id()

		self._save_value(section, key, screen_id)
		return screen_id

	def get_screen_name(self):
		return self._get_string_val("Cast", "screen_name", DEFAULT_SCREEN_NAME)

	def get_screen_app(self):
		return self._get_string_val("Cast", "screen_app", DEFAULT_SCREEN_APP)

	def get_player(self, qplaylist):
		"""
		Attempts to read the selected video players from the config file.
		If provided, returns the first supported player.
		If none are supported or none are provided in the config,
		uses the default player list. Saves supported ones in the config
		and returns the first supported player. If none are supported, raises an error.

		:param qplaylist: The command queue to pass to the player
		:type qplaylist: castberry.playlist.QPlaylist

		:return: The first supported player
		:rtype: castberry.players.iplayer.IPlayer

		:raises EnvironmentError: When none of the provided players or default players are supported.
		"""
		section_name = "Players"

		splash_screen = self._get_splash_screen()
		try:
			players = list(self.__parser[section_name].keys())
			for player in players:
				try:
					return _get_player(player, qplaylist, splash_screen)
				except EnvironmentError:
					logging.warning(
						"Provided player " + player +
						" is not supported by the current environment."
					)
			logging.warning(
				"None of the players provided in the config file are supported " +
				"by the current environment. Defaults will be used")
		except KeyError:
			logging.warning("Config file does not have a " + section_name + " section. Defaults will be used.")

		logging.warning("Trying default players:" + str(DEFAULT_PLAYERS))
		players = DEFAULT_PLAYERS
		supported_player_names = []
		first_supported_player = None
		for player in players:
			try:
				iplayer = _get_player(player, qplaylist, splash_screen)
				if first_supported_player is None:
					first_supported_player = iplayer
				supported_player_names.append(player)
			except EnvironmentError:
				logging.warning(
					"Default player " + player +
					" is not supported by the current environment."
				)
		if first_supported_player is not None:
			self._save_section_keys(section_name, supported_player_names)
			return first_supported_player
		else:
			message = "None of the default players are supported by the current environment."
			logging.critical(message)
			raise EnvironmentError(message)

	def get_resolvers(self):
		"""
		Attempts to read the selected video resolvers from the config file.
		If provided, returns the supported resolvers as CResolvers
		If none are supported or none are provided in the config,
		uses the default resolver list. Saves supported ones in the config
		and returns them as CResolvers. If none are supported, raises an error.

		:return: Supported resolvers as a resolver collection (CResolvers)
		:rtype: castberry.youtube.resolvers.cresolvers.CResolvers

		:raises EnvironmentError: When none of the provided resolvers or default players are supported.
		"""
		section_name = "Resolvers"

		try:
			resolver_names = list(self.__parser[section_name].keys())
			iresolvers = []
			for resolver_name in resolver_names:
				try:
					iresolvers.append(_get_resolver(resolver_name))
				except EnvironmentError:
					logging.warning(
						"Provided resolver " + resolver_name +
						" is not supported by the current environment."
					)
			# Return as a collection or just the single one. Error if none
			if len(iresolvers) > 1:
				from castberry.youtube.resolvers.cresolvers import CResolvers
				return CResolvers(iresolvers)
			elif len(iresolvers) == 1:
				return iresolvers[0]
			else:
				logging.warning(
					"None of the resolvers provided in the config are supported " +
					"by the current environment. Defaults will be used.")
		except KeyError:
			logging.warning("Config file does not have a " + section_name + " section. Defaults will be used.")

		logging.warning("Trying default resolvers: " + str(DEFAULT_RESOLVERS))
		resolver_names = DEFAULT_RESOLVERS
		supported_resolver_names = []
		supported_resolvers = []
		for resolver_name in resolver_names:
			try:
				iresolver = _get_resolver(resolver_name)
				supported_resolver_names.append(resolver_name)
				supported_resolvers.append(iresolver)
			except EnvironmentError:
				logging.warning(
					"Default resolver " + resolver_name +
					" is not supported by the current environment."
				)
		if len(supported_resolver_names) > 0:
			self._save_section_keys(section_name, supported_resolver_names)
			from castberry.youtube.resolvers.cresolvers import CResolvers
			return CResolvers(supported_resolvers)
		else:
			message = "None of the provided resolvers are supported by the current environment."
			logging.critical(message)
			raise EnvironmentError(message)

	def _get_splash_screen(self):
		config_splash = self._get_string_val("Cast", "splash_screen", DEFAULT_SPLASH_SCREEN)
		if config_splash == DEFAULT_SPLASH_SCREEN:
			return config_splash

		if Path(config_splash).exists():
			return config_splash
		else:
			logging.warning("Provided splash screen file does not exist, using the default: " + DEFAULT_SPLASH_SCREEN)
			return DEFAULT_SPLASH_SCREEN
	# endregion

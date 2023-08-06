import logging
import time
from threading import Thread

from castberry.config import Config
from castberry.youtube.cast import QCast
from castberry.youtube.cast import Cast
from castberry.playlist import QPlaylist
from castberry.playlist import Playlist

# Logging configuration
logging.basicConfig(
	level=logging.DEBUG,
	format="%(asctime)s %(module)-10s %(levelname)8s: %(message)s"
)

# Constants
TIMEOUT_T_RESTART = 1


def _t_runner(function):
	"""
	Keeps running a function. Restarts if it raises an exception.

	:param function: Function to keep running
	:type function: typing.Callable
	"""
	while True:
		try:
			function()
		except Exception:
			f_name = function.__name__
			f_file = function.__module__.split(".")[-1]
			logging.exception(f"Restarting {f_name}.{f_file} because an error occurred:")
			time.sleep(TIMEOUT_T_RESTART)


def main():
	logging.info("Starting")
	qcast = QCast()
	qplaylist = QPlaylist()

	logging.info("Reading the configuration file")
	config = Config()
	screen_id = config.get_screen_id()
	screen_name = config.get_screen_name()
	screen_app = config.get_screen_app()
	iplayer = config.get_player(qplaylist)
	iresolver = config.get_resolvers()

	logging.info("Initializing cast")
	cast = Cast(qcast, qplaylist, screen_id, screen_name, screen_app)

	logging.info("Initializing the playlist")
	playlist = Playlist(qplaylist, qcast, iresolver, iplayer)

	logging.info("Starting cast")
	Thread(target=_t_runner, args=[cast.t_listen]).start()
	Thread(target=_t_runner, args=[cast.t_send]).start()

	logging.info("Starting playlist")
	Thread(target=_t_runner, args=[playlist.t_listen]).start()

	logging.info("Everything is ready")

import youtube_dl

from castberry.youtube.resolvers.iresolver import IResolver
from castberry.youtube.video import VideoInfo

# Constants
LINK_YOUTUBE_WATCH = "https://www.youtube.com/watch"


class ResYTDL(IResolver):
	""" Retrieves video info using youtube-dl. """

	class _NoLogger(object):
		"""
		A logger that does nothing.
		Used to hide youtube-dl's logging.
		"""
		def debug(self, msg):
			pass

		def warning(self, msg):
			pass

		def error(self, msg):
			pass

	def get_video_info(self, video_id):
		try:
			options = {"quiet": True, "logger": self._NoLogger()}
			with youtube_dl.YoutubeDL(options) as ytdl:
				result = ytdl.extract_info(
					LINK_YOUTUBE_WATCH+"?v="+video_id,
					download=False,
				)
			best = max(result["formats"], key=lambda video: video["filesize"])
			return VideoInfo(
				title=result["title"],
				source=best["url"]
			)
		except youtube_dl.utils.YoutubeDLError as ydle:
			raise KeyError(ydle)



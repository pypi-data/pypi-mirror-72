from castberry.youtube.resolvers.iresolver import IResolver


class CResolvers(IResolver):
	"""
	A collection of resolvers.
	If one resolver fails, moves onto another.
	"""
	__resolvers = None

	def __init__(self, resolvers):
		"""
		:param resolvers: A list of resolvers
		:type resolvers: List[youtube.resolvers.iresolver.IResolver]
		"""
		self.__resolvers = resolvers

	def get_video_info(self, video_id):
		last_error = None
		for resolver in self.__resolvers:
			try:
				return resolver.get_video_info(video_id)
			except KeyError as ke:
				last_error = ke
				# Try another
				pass
		raise KeyError(f"All provided resolvers failed for video {video_id}. Last error:{str(last_error)}")

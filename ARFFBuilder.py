class ARFFBuilder():

	"""
	ATTRIBUTES:
		feature_dir	-->	directory of JSON files containing the feature maps of preprocessed texts
	"""

	def __init__(self, feature_dir):
		self.feature_dir = feature_dir

	# WRITE COMPONENTS
	def writeHead(self):
		pass

	def writeFeatureList(self):
		pass

	def writeVectors(self):
		pass

	# MAIN PROCESSORS
	def finalize(self):
		pass

if __name__ == "__main__":
	builder = ARFFBuilder("feature_maps/")
	builder.finalize()

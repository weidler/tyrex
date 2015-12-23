import json

class FeatureExtractor():

	"""
	ATTRIBUTES:
		source	-->	string representation of the normalized text
		data	-->	dict object of already calculated data and destination of newly calculated data
	"""

	def __init__(self, source, json_data=None):
		try:
			self.source = self.readFile("../data/"+source)
		except IOError:
			print("SOURCE FILE does not exist. Please provide valid path name.\nFiles are expected to be in '../data/'")

		if json_data:
			self.data = json.load(json_data)
		else:
			self.data = {}

	# PREPROCESSORS
	def readFile(self, filename):
		with open(filename) as f:
			return f.read()

	# EXTRACTION ALGORITHMS
	def calcExample(self):
		pass

	def calcTextLength(self):
		pass

	def calcSentenceLengthAvg(self):
		pass

	def calcSentenceLenthMax(self):
		pass

	def calcSentenceLengthMin(self):
		pass

	# MAIN PROCESSORS
	def finalize(self):
		pass


if __name__ == "__main__":
	fea = FeatureExtractor("test.txt")
	fea.finalize()

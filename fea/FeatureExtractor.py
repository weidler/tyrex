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
			exit()

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
		"""
			Structure calc* methods like this. Calculate based on source string and RETURN the value that
			is meant to be written into the final output
		"""

		return len(self.source)

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
		if "example" not in self.data.keys():
			self.data.update({"example": self.calcExample()})

		return self.data

if __name__ == "__main__":
	fea = FeatureExtractor("normalized_test.txt")
	print(fea.finalize())

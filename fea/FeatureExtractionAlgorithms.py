import sys
import json
import re
from pathlib import Path

class FEA():

	"""
	Feature Extraction Algorithms
	-----------------------------

	ATTRIBUTES:
		source	-->	string representation of the normalized text
		data	-->	dict object of already calculated data and destination of newly calculated data
	"""

	def __init__(self, source, use_json=False):
		try:
			m = re.search(".*\/(.*)\..*", source)
			self.filename = m.group(1)
			print(self.filename)
			self.source = self.readFile(source)
		except IOError:
			print("SOURCE FILE does not exist. Please provide valid path name.")
			exit()

		if use_json:
			self.data = json.loads(self.readFile("../feature_maps/" + source.split("."[0])))
		else:
			self.data = {}

	# PREPROCESSORS
	def readFile(self, filename):
		with open(filename) as f:
			return f.read()

	def writeFeatureMaps(self):
		path = Path("../feature_maps/" + self.filename + ".json")
		path.touch(exist_ok=True)
		with path.open("w") as f:
			f.write(json.dumps(self.data))

	# EXTRACTION ALGORITHMS
	def calcExample(self):
		"""
			Structure calc* methods like this. Calculate based on source string and RETURN the value that
			is meant to be written into the final output
		"""

		return len(self.source)

	def calcExample2(self):
		"""
			Test the precalced data from json_data
		"""

		return len(self.source)*3

	def calcTextLength(self):
		# TODO
		pass

	def calcSentenceLengthAvg(self):
		# TODO
		pass

	def calcSentenceLengthMax(self):
		# TODO
		pass

	def calcSentenceLengthMin(self):
		# TODO
		pass

	# MAIN PROCESSORS
	def finalize(self):
		if "example" not in self.data.keys():
			self.data.update({"example": self.calcExample()})
			print("calculated example")
		if "example2" not in self.data.keys():
			self.data.update({"example2": self.calcExample()})
			print("calculated example2")

		self.writeFeatureMaps()


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("USAGE: python FeatureExtractionAlgorithms.py [filename]\n")
		sys.exit()
	fea = FEA(sys.argv[1])
	fea.finalize()

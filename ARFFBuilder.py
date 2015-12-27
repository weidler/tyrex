import json
from pathlib import Path
from tyrex_lib import checkFileExistance

class ARFFBuilder():

	"""
	ATTRIBUTES:
		feature_dir	-->	directory of JSON files containing the feature maps of preprocessed texts
		files		--> Path Objects of all files found in feature_dir
		f_order		-->	Order of features in ARFF file
	"""

	def __init__(self, feature_dir, arff_filename):
		self.feature_dir = feature_dir
		self.files = list(Path(feature_dir).rglob("*.json"))

		# test if any files found in feature directory, else shut down process
		if len(self.files) < 1:
			print("NO DATA found! Exiting...")
			exit()

		self.checkVektorLengths()
		self.arff = checkFileExistance(arff_filename)

		self.f_order = sorted(list(self.readJSONToDict(self.files[0]).keys()))

	# PREPROCESSORS
	def checkVektorLengths(self):
		last_length = len(self.readJSONToDict(self.files[0]))
		for pos, vector in enumerate(self.files):
			if len(self.readJSONToDict(vector)) != last_length:
				print("Vectors don't have equal length. This was recognized for " + vector.name + ". Until that point " + str(pos) + " were compared.")
				exit()
		return True

	def readJSONToDict(self, json_file):
		with json_file.open() as f:
			return json.loads(f.read())

	def addToARFF(self, line):
		with open(self.arff, "a") as arff:
			arff.write(line+"\n")

	# WRITE COMPONENTS
	def writeHead(self):
		pass

	def writeFeatureList(self):
		for feature in self.f_order:
			line = "@attribute " + feature
			self.addToARFF(line)

	def writeVectors(self):
		pass

	# MAIN PROCESSORS
	def finalize(self):
		self.writeHead()
		self.writeFeatureList()
		self.writeVectors()

if __name__ == "__main__":
	builder = ARFFBuilder("feature_maps/", "data.arff")
	builder.finalize()

import json
from pathlib import Path
from tyrex_lib import checkFileExistance
import sys

class ARFFBuilder():

	"""
	ATTRIBUTES:
		feature_dir	-->	directory of JSON files containing the feature maps of preprocessed texts
		files		--> Path Objects of all files found in feature_dir
		f_order		-->	Order of features in ARFF file
	"""

	def __init__(self, feature_dir, arff_filename, relation_name="tyrex"):
		self.feature_dir = feature_dir
		self.files = list(Path(feature_dir).rglob("*.json"))
		self.relation = relation_name

		# test if any files found in feature directory, else shut down process
		if len(self.files) < 1:
			print("NO DATA found! Exiting...")
			exit()

		self.checkVektorLengths()
		self.arff = checkFileExistance(arff_filename)

		self.f_order = sorted(list(self.readJSONToDict(self.files[0]).keys()))
		self.f_order[-1], self.f_order[self.f_order.index("class")] = "class", self.f_order[-1]

		self.vectors = [self.readJSONToDict(self.files[i]) for i in range(len(self.files))]
		self.class_distribution = self.getClassDistribution()

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

	def extractPossibleValues(self, feature):
		poss = set([vector[feature] for vector in self.vectors])
		return poss

	def toAtrrListString(self, attr_list):
		out = "{ "
		for attr in attr_list:
			out += attr + ", "
		out = out[:-2] + " }"
		return out

	def getClassDistribution(self):
		distr = {c: 0 for c in set([c["class"] for c in self.vectors])}
		for c in self.vectors:
			distr[c["class"]] += 1
		print(distr)
		return distr


	# WRITE COMPONENTS
	def writeHead(self):
		head = ""
		head += "@relation " + self.relation
		self.addToARFF(head)

	def writeFeatureList(self):
		for feature in self.f_order:
			if feature == "class":
				possible_values = self.toAtrrListString(self.extractPossibleValues(feature))
			elif isinstance(self.vectors[0][feature], int) or isinstance(self.vectors[0][feature], float):
				possible_values = "numeric"
			elif isinstance(self.vectors[0][feature], bool):
				possible_values = "{true, false}"
			elif isinstance(self.vectors[0][feature], str):
				possible_values = "string"
			else:
				print("COULDNT RECOGNIZE TYPE")
				possible_values = "string"

			line = "@attribute\t" + feature + "\t" + possible_values
			self.addToARFF(line)

	def writeVectors(self):
		self.addToARFF("@DATA")
		for vector in self.vectors:
			line = ""
			for feature in self.f_order:
				line += str(vector[feature]) + ", "
			line = line[:-2]  #delete last comma
			self.addToARFF(line)

	def writeSpacer(self):
		spacer = "\n"
		self.addToARFF(spacer)

	# MAIN PROCESSORS
	def finalize(self):
		self.writeHead()
		self.writeSpacer()
		self.writeFeatureList()
		self.writeSpacer()
		self.writeVectors()

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print(len(sys.argv))
		print("USAGE: python3 ARFFBuilder.py [vector dir] [output filename]")
		exit()
	else:
		builder = ARFFBuilder(sys.argv[1], sys.argv[2])
		builder.finalize()

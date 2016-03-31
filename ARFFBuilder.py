import json
from pathlib import Path
import sys

class ARFFBuilder():
	"""
	Class manages ARFF FIle Construction.

	@parameters
	feature_dir				string		directory of json vector files
	arff_filename			string		created arff file will be named like This
	relation_name[=tyrex]	string		name of the relation in arff file
	"""

	def __init__(self, feature_dir, arff_filename, relation_name="tyrex"):
		"""
		@attributes
		self.feature_dir		string	directory of JSON files containing the feature maps of preprocessed texts
		self.files				list	Path Objects of all files found in feature_dir
		self.f_order			list	arrangement of features in ARFF file
		self.relation			string	relation will be named like this
		self.arff				string	path/name of arff file
		self.vectors			list	list of vector dicts retrieved from JSON files
		self.class_distribution dict	stores amount of vectors per class
		"""
		self.feature_dir = feature_dir
		self.files = list(Path(feature_dir).rglob("*.json"))
		self.relation = relation_name

		# test if any files found in feature directory, else shut down process
		if len(self.files) < 1:
			print("NO DATA found! Exiting...")
			exit()

		self.checkVektorLengths()
		self.arff = self.checkFileExistance(arff_filename)

		self.f_order = sorted(list(self.readJSONToDict(self.files[0]).keys()))
		self.f_order[-1], self.f_order[self.f_order.index("class")] = "class", self.f_order[-1]  # move class to last position

		self.vectors = [self.readJSONToDict(self.files[i]) for i in range(len(self.files))]
		self.class_distribution = self.getClassDistribution()

	# PREPROCESSORS

	def checkFileExistance(self, filename):
		"""
		Checks if a file at filename exists, if yes asks to overwrite or choose new filename. If overwriting, it
		clears the old file completely.

		@parameters
		filename		string		name of the file that will be checked

		@returns		string		the (maybe new) filename
		"""
		while Path(filename).exists():
			answer = input("This file already exists, do you want to overwrite? [choose new filename otherwise] (Y/n) ")
			if answer in ["Y", "y"]:
				with open(filename, "w") as f: f.write("")
				break
			elif answer in ["N", "n"]:
				filename = input("New path: ")
		return filename

	def checkVektorLengths(self):
		"""
		Checks if all vectors have the same length. if not, error will be displayed and process stops.

		@returns	bool		True if all vectors have same length
		"""

		last_length = len(self.readJSONToDict(self.files[0]))
		for pos, vector in enumerate(self.files):
			if len(self.readJSONToDict(vector)) != last_length:
				print("Vectors don't have equal length. This was recognized for " + vector.name + ". Until that point " + str(pos) + " were compared.")
				exit()
		return True

	def readJSONToDict(self, json_file):
		"""
		Reads a file, decodes its JSON and returns the dict.

		@parameters
		json_file		string		path to json file

		@returns		dict		json file as dict
		"""

		with json_file.open() as f:
			return json.loads(f.read())

	def addToARFF(self, line):
		"""
		Adds a line to the arff file.

		@parameters
		line		string		the line that will be added

		@returns	None
		"""
		with open(self.arff, "a") as arff:
			arff.write(line+"\n")

	def extractPossibleValues(self, feature):
		"""
		Extracts all possible Values for a specified feature from the vectors.

		@parameters
		feature			string		method will look for all possible values for the feature with this name

		@returns		set			distinct list of all those values
		"""

		poss = set([vector[feature] for vector in self.vectors])
		return poss

	def toAtrrListString(self, attr_list):
		"""
		Converts a python list to an ARFF Attribute List for Features

		@parameters
		attr_list		list		python list with feature values

		@returns		string		ARFF Attribute List
		"""

		out = "{ "
		for attr in attr_list:
			out += attr + ", "
		out = out[:-2] + " }"
		return out

	def getClassDistribution(self):
		"""
		Calculates distribution of vectors among classes

		@returns	dict	distribution with class as key, amount of instances as values
		"""

		distr = {c: 0 for c in set([c["class"] for c in self.vectors])}
		for c in self.vectors:
			distr[c["class"]] += 1
		print("Class Distribution: " + str(distr))
		return distr

	# WRITE COMPONENTS
	def writeHead(self):
		"""
		Writes the ARFF File Header

		@returns	None
		"""

		head = ""
		head += "@relation " + self.relation
		self.addToARFF(head)

	def writeFeatureList(self):
		"""
		Writes the List of Features in the ARFF File.

		@returns	None
		"""

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
		"""
		Writes all Vectors as Instances into the ARFF File

		@returns	None
		"""

		self.addToARFF("@DATA")
		for vector in self.vectors:
			line = ""
			for feature in self.f_order:
				line += str(vector[feature]) + ", "
			line = line[:-2]  #delete last comma
			self.addToARFF(line)

	def writeSpacer(self):
		"""
		Creates a space between Elements in ARFF File

		@returns	None
		"""

		spacer = "\n"
		self.addToARFF(spacer)

	# MAIN PROCESSORS
	def finalize(self):
		"""
		Calls all writing methods and thereby writes the ARFF file.

		@returns	None
		"""

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

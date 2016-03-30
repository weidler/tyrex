import sys
import pprint
import math as m

import parser.Parser as p
import fea.FeatureExtractionAlgorithms as fea

class TyReX():
	"""
	Class that takes a filepath and calculates the files normed text and vector to
	then get the Text Type

	@parameters
	filename	string	the name/path of the file
	"""

	def __init__(self, filename):
		"""
		@attributes
		self.filename	string	name/path of concerned file
		self.normed		string	normed (by parser) version of the files content
		self.vector		string	vector for file content, calced by FEA
		"""

		self.filename = filename
		self.normed = self.parse(self.filename)

		self.vector = self.getVector(self.normed)

	def parse(self, filename):
		"""
		Parses the contents of a file to a normalized version. Uses the Parser Class.

		@parameters
		filename	string	filename with original text

		@variables
		parser		Parser	Parser Object

		@returns	string	the normed text
		"""

		parser = p.Parser(filename)
		return parser.convertToNormalized(parser.text)

	def getVector(self, normed_text):
		"""
		Calcs the Vector for a normed text. Uses the FEA Class.

		@parameters
		normed_text		string	a string containing a text normed by the parser

		@variables
		falg			FEA		Feature Extraction ALgorithm Object that calcs the vector

		@returns		dict	vector dictionary: {"featurename": value, ...}
		"""
		falg = fea.FEA("unknown", normed_text, "", is_file=False)
		return falg.finalize()

	def getTextType(self):
		"""
		Uses the Results of a simple logistic algorithm, that learned from over 1000 files, to calc which class is most likely.
		Returns this class.

		@variables
		epic		float	SimpleLogistRegression Value for epic class
		drama		float	SimpleLogistRegression Value for drama class
		report		float	SimpleLogistRegression Value for report class
		poetry		float	SimpleLogistRegression Value for poetry class
		classes		tuples	contains tuples with classname/regressionvalue pairs

		@returns	string	most likely classname
		"""

		# USES SimpleLogistic

		epic = -86.84 + self.vector["NE_frequency"] * -240.51 + self.vector["digit_frequency"] * 41.74 + self.vector["noun_frequency"] * -121.33 + self.vector["phrases_per_paragraph"] * 0.87 + self.vector["rhyme_average"] * -1.54 + self.vector["sentence_length_max"] * 0 + self.vector["verb_frequency"] * 147.94 + self.vector["word_length_average"] * 86.19

		drama = 60.87 + self.vector["NE_frequency"] * 29.37 + self.vector["digit_frequency"] * -171.98 + self.vector["phrases_per_paragraph"] * -1.39 + self.vector["rhyme_average"] * 1.75 + self.vector["sentence_length_avg"] * -0.25 + self.vector["sentence_length_max"] * 0.04 + self.vector["sentence_length_min"] * -0.15 + self.vector["verb_frequency"] * -194.75 + self.vector["word_length_average"] * -42.27

		report = -137.81 + self.vector["word_variance"] * -11.04 + self.vector["digit_frequency"] * 124.31 + self.vector["phrases_per_paragraph"] * -3.45 + self.vector["punctuation_frequency"] * -131.95 + self.vector["sentence_length_avg"] * -0.27 + self.vector["sentence_length_min"] * -1.77 + self.vector["verb_frequency"] * -28.28 + self.vector["word_length_average"] * 186.6

		poetry = -5.74 + self.vector["word_variance"] * 9.99 + self.vector["digit_frequency"] * -133.89 + self.vector["noun_frequency"] * 55.13 + self.vector["phrases_per_paragraph"] * 0.47 + self.vector["punctuation_frequency"] * 74.44 + self.vector["sentence_length_avg"] * 0.24 + self.vector["sentence_length_max"] * -0.02 + self.vector["sentence_length_min"] * 0.09 + self.vector["text_length"] * 0 + self.vector["word_length_average"] * -6.54

		classes = (("epic", epic), ("drama", drama), ("report", report), ("poetry", poetry))

		#pprint.pprint([c + ": " + str(v) for c, v in classes])

		return max(classes, key=lambda x: x[1])[0]

if __name__ == "__main__":
	tyrex = TyReX(sys.argv[1])
	pprint.pprint(tyrex.getTextType())

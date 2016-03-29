import sys
import pprint

import parser.Parser as p
import fea.FeatureExtractionAlgorithms as fea

class TyReX():

	def __init__(self, filename):

		self.filename = filename
		self.normed = self.parse(self.filename)

		self.vector = self.getVector(self.normed)

	def parse(self, filename):
		parser = p.Parser(filename)
		return parser.convertToNormalized(parser.text)

	def getVector(self, normed_text):
		falg = fea.FEA("unknown", normed_text, "", is_file=False)
		return falg.finalize()

	def getTextType(self):

		epic = -86.84 + self.vector["NE_frequency"] * -240.51 + self.vector["digit_frequency"] * 41.74 + self.vector["noun_frequency"] * -121.33 + self.vector["phrases_per_paragraph"] * 0.87 + self.vector["rhyme_average"] * -1.54 + self.vector["sentence_length_max"] * 0 + self.vector["verb_frequency"] * 147.94 + self.vector["word_length_average"] * 86.19

		drama = 60.87 + self.vector["NE_frequency"] * 29.37 + self.vector["digit_frequency"] * -171.98 + self.vector["phrases_per_paragraph"] * -1.39 + self.vector["rhyme_average"] * 1.75 + self.vector["sentence_length_avg"] * -0.25 + self.vector["sentence_length_max"] * 0.04 + self.vector["sentence_length_min"] * -0.15 + self.vector["verb_frequency"] * -194.75 + self.vector["word_length_average"] * -42.27

		report = -137.81 + self.vector["word_variance"] * -11.04 + self.vector["digit_frequency"] * 124.31 + self.vector["phrases_per_paragraph"] * -3.45 + self.vector["punctuation_frequency"] * -131.95 + self.vector["sentence_length_avg"] * -0.27 + self.vector["sentence_length_min"] * -1.77 + self.vector["verb_frequency"] * -28.28 + self.vector["word_length_average"] * 186.6

		poetry = -5.74 + self.vector["word_variance"] * 9.99 + self.vector["digit_frequency"] * -133.89 + self.vector["noun_frequency"] * 55.13 + self.vector["phrases_per_paragraph"] * 0.47 + self.vector["punctuation_frequency"] * 74.44 + self.vector["sentence_length_avg"] * 0.24 + self.vector["sentence_length_max"] * -0.02 + self.vector["sentence_length_min"] * 0.09 + self.vector["text_length"] * 0 + self.vector["word_length_average"] * -6.54

		classes = (("epic", epic), ("drama", drama), ("report", report), ("poetry", poetry))

		return (max(classes)[0], min(classes)[0])

if __name__ == "__main__":
	tyrex = TyReX(sys.argv[1])
	pprint.pprint(tyrex.getTextType())

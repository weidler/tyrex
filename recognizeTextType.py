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
		pass

if __name__ == "__main__":
	tyrex = TyReX(sys.argv[1])
	pprint.pprint(tyrex.vector)

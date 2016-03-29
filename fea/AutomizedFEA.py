from FeatureExtractionAlgorithms import FEA
from pathlib import Path
import sys

class AutomizedFEA():

	"""
	Automized Feature Extraction Algorithms
	---------------------------------------

	Automatically applies FEA on a whole directory with some options

	ATTRIBUTES:
		dir		-->	directory where normalized source files are stored
		path	-->	path object to that directory
		target	-->	path where feature maps will be saved
	"""

	def __init__(self, directory, target, prefix="", f_type="txt", use_json=False):
		self.dir = directory
		self.prefix = prefix
		self.target = target

		self.use_json = use_json

		self.f_type = f_type
		self.files = list(Path(self.dir).rglob(self.prefix + "*." + self.f_type))

	def process(self):

		if self.use_json:
			print("Using already calculated data...")

		amount_of_vectors = len(self.files)

		for pos, f in enumerate(self.files):
			if not self.prefix:
				class_name = f.name.split("_")[0]
			else:
				class_name = self.prefix

			fea = FEA(class_name, str(f), self.target, use_json=self.use_json)
			if fea.finalize():
				print(str(pos+1) + "/" + str(amount_of_vectors) + " processed files. (at " + f.name + ")")

if __name__ == '__main__':
	if len(sys.argv) == 3:
		afea = AutomizedFEA(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		afea = AutomizedFEA(sys.argv[1], sys.argv[2], use_json=sys.argv[3])
	elif len(sys.argv) == 5:
		afea = AutomizedFEA(sys.argv[1], sys.argv[2], use_json=sys.argv[3], prefix=sys.argv[4])
	else:
		print("USAGE: python3 AutomizedFEA.py [input] [target] [[prefix]] [[use_json]]")
		exit()

	afea.process()

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

	def __init__(self, directory, target, prefix="", f_type="txt"):
		self.dir = directory
		self.prefix = prefix
		self.target = target

		self.f_type = f_type
		self.files = list(Path(self.dir).rglob(self.prefix + "*." + self.f_type))

	def process(self):
		for f in self.files:
			if not self.prefix:
				class_name = f.name.split("_")[0]
			else:
				class_name = self.prefix

			fea = FEA(class_name, str(f), self.target)
			if fea.finalize():
				print("wrote file " + f.name + "...")

if __name__ == '__main__':
	if len(sys.argv) == 3:
		afea = AutomizedFEA(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		afea = AutomizedFEA(sys.argv[1], sys.argv[2], prefix=sys.argv[1])
	else:
		print("USAGE: python3 AutomizedFEA.py [input] [target] [[prefix]] [[input_type]]")
		exit()

	afea.process()

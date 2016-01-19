from FeatureExtractionAlgorithms import FEA
from pathlib import Path

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

	def __init__(self, class_name, directory, target, f_type="txt"):
		self.dir = directory
		self.prefix = prefix
		self.class_name = class_name
		self.target = target

		self.f_type = f_type
		self.files = list(Path(self.dir).rglob(self.prefix + "*." + self.f_type))
		print(self.files)

	def process(self):
		for f in self.files:
			fea = FEA(self.class_name, str(f), self.target)
			fea.finalize()
			print("wrote file " + f.name + "...")

if __name__ == '__main__':
	afea = AutomizedFEA("1", "data/", "feature_maps/", "normalized_")
	afea.process()

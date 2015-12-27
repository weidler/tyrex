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
	"""

	def __init__(self, directory, prefix="", f_type="txt"):
		self.dir = directory
		self.prefix = prefix
		self.f_type = f_type
		self.files = list(Path(self.dir).rglob(self.prefix + "*." + self.f_type))
		print(self.files)

if __name__ == '__main__':
	afea = AutomizedFEA("../data", "normalized_")

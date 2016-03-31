from FeatureExtractionAlgorithms import FEA
from pathlib import Path
import sys

class AutomizedFEA():

	"""
	Automatically applies FEA on a whole directory with some options

	@parameters:
	directory			string		directory for normalized files are stored
	target				string		directory where JSON files will be stored
	prefix				string		optional prefix, if passing a prefix, only files with that prefix will be used
									and the prefix is taken as classname for those files
	f_type[=txt]		string		file extention for files that are used, only files with that extension will be read
	use_json[=False]	bool		if set True, FEAs will use existing JSON files
	"""

	def __init__(self, directory, target, prefix="", f_type="txt", use_json=False):
		"""
		@attributes
		self.dir		string	directory where normalized source files are stored
		self.prefix		string	only files with that prefix will be used
		self.target		string	path where feature maps will be saved
		self.use_json	bool	use existing JSON info in FEAs
		self.f_type		string	only use files of that type
		self.files		list	all files as PosixPaths
		"""

		self.dir = directory
		self.prefix = prefix
		self.target = target

		self.use_json = use_json

		self.f_type = f_type
		self.files = list(Path(self.dir).rglob(self.prefix + "*." + self.f_type))

	def process(self):
		"""
		Processes all files in self.files by determining their classname from the filename or self.prefix
		and creating their FEA Object.

		@variables
		amount_of_vectors	int		tracks how many files where processed yet together with enumerate in for loop

		@returns	None
		"""
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

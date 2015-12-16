import re

class Parser():
	def __init__(self, files):

		if isinstance(files, list):
			self.files = files
		else:
			self.files = [files]

	# FILE PROCESSING

	def readFile(self, filename):
		with open(filename, "r") as f:
			return f.read()

	def writeNormalizedFile(self, normalized, filename):
		with open(filename, "w") as f:
			f.write(normalized)

	# DATA PROCESSING

	def convertToNormalized(self, unnormalized):
		""" TO BE OVERWRITTEN """
		return re.sub("\\n", "", unnormalized)

	# MAIN PROCESSORS

	def finalize(self):
		out = {}
		for f in self.files:
			out.update({f: self.convertToNormalized(self.readFile(f))})

		return out


if __name__ == "__main__":
	p = Parser("test.txt")
	print(p.finalize())

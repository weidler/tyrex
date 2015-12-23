import re
from pathlib import Path

class Parser():
	def __init__(self, source_dir, target_dir):
		self.files = list(Path(source_dir).rglob("*.txt"))
		if len(self.files) < 1:
			print("ATTENTION no files found")

		self.target_dir = target_dir

	# FILE PROCESSING

	def readFileAtPath(self, posix_path):
		with posix_path.open() as f:
			return f.read()

	def writeNormalizedFile(self, normalized, filename):
		posix_path = Path(self.target_dir+"normalized_"+filename)
		with posix_path.open("w") as f:
			return f.write(normalized)

	# DATA PROCESSING

	def convertToNormalized(self, unnormalized):
		""" TO BE OVERWRITTEN """
		return re.sub("\\n", "", unnormalized)

	# MAIN PROCESSORS

	def convertAll(self):
		out = {}
		for f in self.files:
			out.update({f.name: self.convertToNormalized(self.readFileAtPath(f))})

		return out

	def writeAll(self, normalized_data):
		for f in normalized_data:
			self.writeNormalizedFile(normalized_data[f], f)

	def finalize(self):
		normalized = self.convertAll()
		self.writeAll(normalized)
		print("SUCCESSFULLY converted and written " + str(len(normalized)) + " files")


if __name__ == "__main__":
	p = Parser("../raw_data/", "../data/")
	p.finalize()

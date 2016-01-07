import sys
import re
from pathlib import Path

class Parser():
	def __init__(self, source_dir, target_dir, prefix="normalized"):
		self.files = list(Path(source_dir).rglob("*.txt"))
		if len(self.files) < 1:
			print(source_dir)
			print("No files found! Exiting...")
			exit()

		self.target_dir = target_dir
		self.prefix = prefix

	# FILE PROCESSING

	def readFileAtPath(self, posix_path):
		with posix_path.open() as f:
			return f.read()

	def writeNormalizedFile(self, normalized, filename):
		posix_path = Path(self.target_dir+self.prefix+"_"+filename)
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
	if len(sys.argv) != 3:
		print("USAGE: python Parser[XY].py [source_dir] [destination_dir]")
		sys.exit()
	p = Parser(sys.argv[1], sys.argv[2])
	p.finalize()

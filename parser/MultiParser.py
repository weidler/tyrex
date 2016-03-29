import sys
import re
#import codecs
from pathlib import Path
from html2text import html2text

import Parser


class MultiParser(Parser.Parser):
	def __init__(self, source_dir, target_dir, prefix=None):
		self.files = list(Path(source_dir).rglob("**/*.*"))
		if len(self.files) < 1:
			print(source_dir)
			print("No files found! Exiting...")
			exit()

		self.target_dir = target_dir

		self.prefix = prefix
		self.fails = []

	# FILE PROCESSING

	def readFileAtPath(self, posix_path):
		print("parsing: "+posix_path.name)
		try:
			with posix_path.open(encoding="utf-8") as f:  # general encoding
				return html2text(f.read())
		except UnicodeDecodeError:
			try:
				with posix_path.open(encoding="latin-1") as f:  # german language encoding
					return html2text(f.read())
			except:
				self.fails.append(posix_path.name)
				return False
		except:
			self.fails.append(posix_path.name)
			return False

	def writeNormalizedFile(self, normalized, parent, filename):
		if not self.prefix:
			class_name = parent.name
		else:
			class_name = self.prefix

		posix_path = Path(self.target_dir+class_name+"_"+filename.split(".")[0] + ".txt")
		with posix_path.open("w") as f:
			return f.write(normalized)

	# MAIN PROCESSORS

	def convertAll(self):
		out = {}
		for f in self.files:
			out.update({f.name: (self.convertToNormalized(self.readFileAtPath(f)), f.parent)})

		return out

	def writeAll(self, normalized_data):
		failed = 0
		success = 0
		for f in normalized_data:
			if normalized_data[f][0]:
				self.writeNormalizedFile(normalized_data[f][0], normalized_data[f][1], f)
				success += 1
			else:
				failed += 1

		return (success, failed)

	def finalize(self):
		normalized = self.convertAll()
		files = self.writeAll(normalized)
		print("SUCCESSFULLY converted and written " + str(files[0]) + " files")
		print("FAILED to convert and write " + str(files[1]) + " files")
		print("\tfailed at: " + str(self.fails))

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("USAGE: python3 MultiParser[XY].py [source_dir] [destination_dir]")
		sys.exit()
	p = MultiParser(sys.argv[1], sys.argv[2])
	p.finalize()

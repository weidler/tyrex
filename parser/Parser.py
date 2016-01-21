import sys
import re
from pathlib import Path
from html2text import html2text

class Parser():
	def __init__(self, source_dir, target_dir, prefix=None):
		self.files = list(Path(source_dir).rglob("**/*.*"))
		if len(self.files) < 1:
			print(source_dir)
			print("No files found! Exiting...")
			exit()

		self.target_dir = target_dir

		self.prefix = prefix

	# FILE PROCESSING

	def readFileAtPath(self, posix_path):
		print("AT FILE: "+posix_path.name)
		with posix_path.open() as f:
			return html2text(f.read())

	def writeNormalizedFile(self, normalized, parent, filename):
		if not self.prefix:
			class_name = parent.name
		else:
			class_name = self.prefix

		posix_path = Path(self.target_dir+class_name+"_"+filename.split(".")[0] + ".txt")
		with posix_path.open("w") as f:
			return f.write(normalized)

	# DATA PROCESSING

	def convertToNormalized(self, unnormalized):
		#sentence bounds
		phrase = "<s>", "</s>"

		#punctuations
		punct = "<punct>"  #  .
		question = "<question>"  #  ?
		excl = "<exclamation>"  #  !
		susp = "<suspension>"  # ...
		comma = "<comma>"  #  ,
		colon = "<colon>"  #  :
		think = "<thinking>"  #  -

		#apostroph
		direct = ("<speech>", "</speech>")
		apo = ("<apo>", "</apo>")

		#regex
		phrase_bound = punct + "|" + question + "|" + excl
		phrase_match = "(?=((" + phrase_bound + "|^)(((.|\s)*?)(" + phrase_bound + "))))"

		#ANNOTATING...

		#tags
		out = re.sub("\.{3,}", susp, unnormalized)
		out = re.sub("\.", punct, out)
		out = re.sub("\?", question, out)
		out = re.sub("\!", excl, out)
		out = re.sub("\,", comma, out)
		out = re.sub("\:", colon, out)
		out = re.sub(" \- ", think, out)

		out = "".join([phrase[0] + match[2] + phrase[1] for match in re.findall(phrase_match, out)])  #sentence bounds
		out = out.replace("<s>\n", "\n<s>")  #linebreak before, not after sentence start
		#out = re.sub("[^\s]<", lambda match: match[0] + " " + match[1], out)  #have all elements seperated by space

		return out

	# MAIN PROCESSORS

	def convertAll(self):
		out = {}
		for f in self.files:
			out.update({f.name: (self.convertToNormalized(self.readFileAtPath(f)), f.parent)})

		return out

	def writeAll(self, normalized_data):
		for f in normalized_data:
			self.writeNormalizedFile(normalized_data[f][0], normalized_data[f][1], f)

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

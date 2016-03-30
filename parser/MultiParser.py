import sys
import re
#import codecs
from pathlib import Path
from html2text import html2text

import Parser


class MultiParser(Parser.Parser):
	"""
	SubClass of Parser that works with multiple files and writes results in new files into given directory

	@parameters
	source_dir		string	path to directory that contains unnormalized files
	target_dir		string	path to directory where normalized files will be saved
	prefix[=None]	string	optional prefix, if not None all created files will have this prefix,
							else parent directory name will be used as prefix
	"""
	def __init__(self, source_dir, target_dir, prefix=None):
		"""
		@attributes
		self.files			list	List of PosixPath Objects, representing all files that will be converted
		self.target_dir		string	path to directory where normalized files will be saved
		self.prefix			string	optional prefix, if not None all created files will have this prefix,
									else parent directory name will be used as prefix
		self.fails			list	List of all filenames (strings) of those files, that couldnt be succesfully read
		"""

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
		"""
		Reads a file at a given path. Looks for utf-8/latin-1 encoding. Converts HTML Markup to Text.
		Class counts failed attempts to read.

		@parameters
		posix_path		string	the concerned filepath at which the method should read

		@returns		string	html-free content of filepath
						bool	FALSE if encoding unknown or file not found
		"""

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
		"""
		Writes a normalized text into a file at the target directory

		@parameters
		normalized		string		normalized text
		parent			PosixPath	PosixPathObject of the Parent directory of the original file
		filename		string		name of original file

		@variables
		class_name		string		prefix for filename, usually the classname
		posix_path		PosixPath	PosixPathObject where new file will be saved

		@returns		bool		True if successfull
		"""

		if not self.prefix:
			class_name = parent.name
		else:
			class_name = self.prefix

		posix_path = Path(self.target_dir+class_name+"_"+filename.split(".")[0] + ".txt")
		with posix_path.open("w") as f:
			return f.write(normalized)

	# MAIN PROCESSORS

	def convertAll(self):
		"""
		Converts all files.

		@returns	dict	dictionary containing original filenames with normalized texts and parent directory PosixPath
		"""

		out = {}
		for f in self.files:
			out.update({f.name: (self.convertToNormalized(self.readFileAtPath(f)), f.parent)})

		return out

	def writeAll(self, normalized_data):
		"""
		Writes all succesfully read and converted texts into files using the writeNormalizedFile() Method.

		@parameters
		normalized_data		dict	dict as created by method convertAll()

		@variables
		success				int		number of succesfully written files
		failed				int 	number of unsuccessfully written files

		@returns			tuples	contains number of successes and fails wile writing
		"""

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
		"""
		Method processes all functions for given class parameters

		@returns	None
		"""

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

import sys
import json
import re
from pathlib import Path
#from tyrex_lib import checkFileExistance

class FEA():

	"""
	Feature Extraction Algorithms
	-----------------------------

	ATTRIBUTES:
		source	-->	string representation of the normalized text
		data	-->	dict object of already calculated data and destination of newly calculated data
	"""

	def __init__(self, source, map_dir, use_json=False):

		m = re.search(".*\/(.*)\..*", source)
		self.filename = m.group(1)
		self.map_dir = map_dir

		try:
			self.source = self.readFile(source)
		except IOError:
			print("SOURCE FILE does not exist. Please provide valid path name.")
			exit()

		if use_json:
			self.data = json.loads(self.readFile(self.map_dir + source.split("."[0])))
		else:
			self.data = {}

	# PREPROCESSORS
	def readFile(self, filename):
		with open(filename) as f:
			return f.read()

	def writeFeatureMaps(self):
		path = Path(self.map_dir + self.filename + ".json")
		path.touch(exist_ok=True)

		#checkFileExistance(path)

		with path.open("w") as f:
			f.write(json.dumps(self.data))

	# EXTRACTION ALGORITHMS
	def calcExample(self):
		"""
			Structure calc* methods like this. Calculate based on source string and RETURN the value that
			is meant to be written into the final output
		"""

		four_letter_words = re.findall("[A-Z]+[a-z]{3}", self.source)
		out = len(four_letter_words)

		return out

	def calcExample2(self):
		"""
			Test the precalced data from json_data
		"""

		mo = re.match(".*([A-Z][^0-9]*)\s.*", self.source)
		try:
			word = mo.group(1)
			print(word)
		except:
			word = ""
		return len(word)

	def calcTextLength(self):
		"""
		Calculates the length of the text and ignores XMl-tags.
		"""
		#S.L.
		text = re.match((.*?)[<.*?>], self.source)
		splittedText = [el.split() for el in text]
		return len(splittedText)

	def calcSentenceLengthAvg(self):
		"""
		Calculates the average of number of words in all sentences.
		"""
		#(S.L.)
		sentences = re.findall("(.*?)[\.|\!|\?]", self.source)
		NumOfPhrases = 0
		allPhrases = 0
		for sentence in sentences:
			NumOfPhrases += 1
			allPhrases += len(sentence.split(" "))

		averagePhrase = allPhrases/float(NumOfPhrases)

		return averagePhrase

	def calcSentenceLengthMax(self):
		"""
		Calculates the longest sentence and gives back the number of words in this sentence.
		"""
		#(S.L./T.W.)
		sentences = re.findall("(.*?)[\.|\!|\?]", self.source)
		return max(map(len, [i.split(" ") for i in sentences]))

	def calcSentenceLengthMin(self):
		"""
		Calculates the shortest sentence and gives back the number of words in this sentence.
		"""
		#(S.L./T.W.)
		sentences = re.findall("(.*?)[\.|\!|\?]", self.source)
		return min(map(len, [i.split(" ") for i in sentences]))

	def calcRhyme1(self):
		"""
		Counts all occurence of endings and returns the number of rhymes/count of lines
		"""
		#S.L.
		lines = re.findall("(.*?)[\\n]", self.source)
		endings_dict = {}
		for line in lines:
			lastchars = line[-1][-1:-3]
			if lastchars in endings_dict.keys():
				endings_dict[lastchars] += 1
			else:
				endings_dict[lastchars] = 1

		rhymes = 0
		for key in vers_dict:
			if vers_dict[key] >= 2:		#counts all endings that occures min 2 times
				rhymes += vers_dict[key]

		return rhymes/len(lines) #durschnittlicher Reimwert

	def calcRhyme2(self):
		"""
		Takes rhyme schemes and checks a text with them, giving back ???
		"""
		#S.L.
		lines = re.findall("(.*?)[\\n]", self.source)
		endings_list = ["" for i in len(lines)]
		c=0			#counter
		for line in lines:
			lastchars = line[-1][-1:-3]
			endings_list[c] = lastchars
			c +=1

		rhyme_schemes = [[a,a,b,b],[a,b,a,b],[a,b,b,a],[a,a,b,c,c,b],[a,b,a,((b,c,b)|(c,b,c))],[a,b,c,a,b,c]]
		# Paarreim, Kreuzreim, umarmender Reim, Schweifreim, Kettenreim, verschränkter Reim, (Binnenreim?[...a...a...,...b...,...b...])

		# vergleichen übereinstimmung

	def calcTerminologicalCongruence(self):
		# TODO
		pass

	def calcDigitFrequency(self):
		# TODO (by Lydia)
		count = 0
		for char in self.source:
			if char in "1234567890":
				count+=1
		return len(self.source)/count

	def calcPunctuationFrequency(self):
		# TODO (by Lydia)
		pass

	def calcHashtagFrequency(self):
		# TODO (by Lydia)
		pass

	def calcNEFrequency(self):
		# TODO
		pass

	# MAIN PROCESSORS
	def finalize(self):
		if "example" not in self.data.keys():
			self.data.update({"example": self.calcExample()})
			print("calculated example")
		if "example2" not in self.data.keys():
			self.data.update({"example2": self.calcExample2()})
			print("calculated example2")
		if "sentence_length_avg" not in self.data.keys():
			self.data.update({"sentence_length_avg": self.calcSentenceLengthAvg()})
			print("calculated sentence_length_avg")
		if "sentence_length_max" not in self.data.keys():
			self.data.update({"sentence_length_max": self.calcSentenceLengthMax()})
			print("calculated sentence_length_max")

		self.writeFeatureMaps()


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("USAGE: python FeatureExtractionAlgorithms.py [filename] [map_dir]\n")
		sys.exit()
	fea = FEA(sys.argv[1], sys.argv[2])
	fea.finalize()

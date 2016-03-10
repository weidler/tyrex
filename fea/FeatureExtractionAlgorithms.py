import sys
import json
import re
import pprint
import treetaggerwrapper as tt
from pathlib import Path
from collections import Counter
#from tyrex_lib import checkFileExistance

class FEA():

	"""
	Feature Extraction Algorithms
	-----------------------------

	ATTRIBUTES:
		source	-->	string representation of the normalized text
		data	-->	dict object of already calculated data and destination of newly calculated data
	"""

	def __init__(self, class_name, source, map_dir, use_json=False):

		print("\n----------NEW---------------")

		# get the filename of the input file
		m = re.search(".*\/(.*)\..*", source)
		if m:
			self.filename = m.group(1)
		else:
			self.filename = source

		# target directory of vector json files
		self.map_dir = map_dir

		# read source file if existing, else stop
		try:
			self.source = self.readFile(source)
		except IOError:
			print("SOURCE FILE does not exist. Please provide valid path name.")
			exit()

		# if use_json flag is true, use existing data
		if use_json:
			self.data = json.loads(self.readFile(self.map_dir + source.split("."[0])))
		else:
			self.data = {}

		# add class name to this vector
		self.data.update({"class": class_name})

		self.treetagged = self.applyTreeTagger(self.source)

		#print("____________________")
		#print(source)
		print("Calculating Vector for: " + self.filename)
		#print(self.map_dir)
		#print("____________________")

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

	def applyTreeTagger(self, text):
		tagger = tt.TreeTagger(TAGLANG="de")
		tagged_list = tt.make_tags(tagger.tag_text(self.cleanSource(text)))
		print(tagged_list)
		return tagged_list

	def cleanSource(self, source):
		return re.sub("<.*?>", "", source)

	# EXTRACTION ALGORITHMS
	def calcTextLength(self):
		"""
		Calculates the length of the text and ignores XMl-tags.
		"""
		#(S.L.)
		text = re.sub("<.*?>", "", self.source)
		return len(text.split())

	def calcSentenceLengthAvg(self):
		"""
		Calculates the average of number of words in all sentences.
		"""
		#(S.L.)
		sentences = [group[0] for group in re.findall("<s>((.|\s)*?)<\/s>", self.source)]
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
		sentences = [group[0] for group in re.findall("<s>((.|\s)*?)<\/s>", self.source)]
		return max(map(len, [i.split(" ") for i in sentences]))

	def calcSentenceLengthMin(self):
		"""
		Calculates the shortest sentence and gives back the number of words in this sentence.
		"""
		#(S.L./T.W.)
		sentences = [group[0] for group in re.findall("<s>((.|\s)*?)<\/s>", self.source)]
		return min(map(len, [i.split(" ") for i in sentences]))

	def calcRhyme1(self):
		"""
		Counts all occurence of endings and returns the number of rhymes/count of lines. From 0->1; 0 means no rhymes, 1 means everything rhymes.
		"""
		#(S.L.)
		## muss noch angepasst werden an: unreine Reime, wenn "" auftaucht
		lines = re.findall("(.*?)(<.*?>)*[\\n]", self.source)
		endings_dict = {}
		for line in lines:
			act_line = re.sub("<.*?>", "", line)
			lastword = act_line.split()[-1]
			lastchar = lastword[-1]
			if lastchar != " ":
				lastchars = lastword[-3:]
				if lastchars in endings_dict.keys():
					endings_dict[lastchars] += 1
				else:
					endings_dict[lastchars] = 1
		rhymes = 0
		for k in endings_dict:
			if endings_dict[k] >= 2:		#counts all endings that occures min 2 times
				rhymes += endings_dict[k]

		return float(rhymes)/len(lines)  #durschnittlicher Reimwert, 0 means no rhymes, 1 means everything rhymes

	def calcRhyme2(self):
		#TODO
		"""
		Takes rhyme schemes and checks a text with them, giving back ???
		"""
		#S.L.
		lines = re.findall("(.*?)[\\n]", self.source)
		endings_list = ["" for i in len(lines)]
		c = 0			#counter
		for line in lines:
			lastchars = line[-1][-1:-3]
			endings_list[c] = lastchars
			c += 1

		rhyme_schemes = [[a,a,b,b],[a,b,a,b],[a,b,b,a],[a,a,b,c,c,b],[a,b,a,((b,c,b)|(c,b,c))],[a,b,c,a,b,c]]
		# Paarreim, Kreuzreim, umarmender Reim, Schweifreim, Kettenreim, verschränkter Reim, (Binnenreim?[...a...a...,...b...,...b...])

		# vergleichen übereinstimmung

	def calcTerminologicalCongruence(self):
		"""Zählt die 'mostCommonWords' """
		# S.L.
		words = self.source.split()
		mostCommonWords = Counter(words).most_common() 	# list with tuples
		return mostCommonWords

	def calcPhrasesPerParagraph(self):
		splitfile = self.source.splitlines()
		while '' in splitfile:
			splitfile.remove('')
		count = 0
		for line in splitfile:
			count += len(re.findall('<s>', line))
		return float(count)/len(splitfile)

	def calcDigitFrequency(self):
		numbs = len(re.findall("\d+", self.source))
		return float(numbs)/len(self.source.split(" "))

	def calcPunctuationFrequency(self):
		text_length = len(re.sub('<punct>|<exclamation>|<question>|<colon>|<semicolon>|<suspension>|<comma>|<thinking>', "i", self.source))
		puncts = len(re.findall('<punct>|<exclamation>|<question>|<colon>|<semicolon>|<suspension>|<comma>|<thinking>', self.source))
		return float(puncts)/text_length

	def calcHashtagFrequency(self):
		count = 0  #count per word
		for char in self.source.split():
			if re.match(r'#[.]*', char):
				count += 1
		return float(count)/len(self.source)

	def calcWordLengthAvg(self):
		clean_text = re.sub('<.*?>', "", self.source)
		char = 0
		for word in clean_text.split():
			char += len(word)
		return float(char)/len(clean_text)

	def calcWordVariance(self):
		clean_text = re.sub('<.*?>', "", self.source)
		return len(set(clean_text.split()))/len(clean_text.split())

	def calcNEFrequency(self):
		# TODO
		pass

	# MAIN PROCESSORS
	def finalize(self):
		if "sentence_length_avg" not in self.data.keys():
			self.data.update({"sentence_length_avg": self.calcSentenceLengthAvg()})
		if "sentence_length_max" not in self.data.keys():
			self.data.update({"sentence_length_max": self.calcSentenceLengthMax()})
		if "sentence_length_min" not in self.data.keys():
			self.data.update({"sentence_length_min": self.calcSentenceLengthMin()})
		if "text_length" not in self.data.keys():
			self.data.update({"text_length": self.calcTextLength()})
		if "phrases_per_paragraph" not in self.data.keys():
			self.data.update({"phrases_per_paragraph": self.calcPhrasesPerParagraph()})
		if "digit_frequency" not in self.data.keys():
			self.data.update({"digit_frequency": self.calcDigitFrequency()})
		if "punctuation_frequency" not in self.data.keys():
			self.data.update({"punctuation_frequency": self.calcPunctuationFrequency()})
		#if "hashtag_frequency" not in self.data.keys():
		#	self.data.update({"hashtag_frequency": self.calcHashtagFrequency()})
		#if "rhyme_average" not in self.data.keys():
		#	self.data.update({"rhyme_average": self.calcRhyme1()})
		if "word_length_average" not in self.data.keys():
			self.data.update({"word_length_average": self.calcWordLengthAvg()})
		if "word_variance" not in self.data.keys():
			self.data.update({"word_variance": self.calcWordVariance()})

		self.writeFeatureMaps()

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("USAGE: python FeatureExtractionAlgorithms.py [class] [filename] [map_dir]\n")
		sys.exit()
	fea = FEA(sys.argv[1], sys.argv[2], sys.argv[3])
	fea.finalize()

import sys
import json
import re
import pprint
import treetaggerwrapper as tt
from pathlib import Path
from collections import Counter
#from tyrex_lib import checkFileExistance

# -*- coding: utf-8 -*-

class FEA():

	"""
	Feature Extraction Algorithms
	-----------------------------

	ATTRIBUTES:
		source	-->	string representation of the normalized text
		data	-->	dict object of already calculated data and destination of newly calculated data
	"""

	def __init__(self, class_name, source, map_dir, use_json=False, is_file=True):
		# recognising file or textstring
		if is_file:
			# get the filename of the input file
			m = re.search(".*\/(.*)\..*", source)
			if m:
				self.filename = m.group(1)
			else:
				self.filename = source

			# read source file if existing, else stop
			try:
				self.source = self.readFile(source)
			except IOError:
				print("SOURCE FILE does not exist. Please provide valid path name.")
				exit()
		else:
			self.filename = ""
			self.source = source

		# target directory of vector json files
		self.map_dir = map_dir

		# if use_json flag is true, use existing data

		if use_json:
			try:
				self.data = json.loads(self.readFile(self.map_dir + re.match("(.*[/\\\]|.*?)(.*)\..+", source).group(2) + ".json"))
			except:
				self.data = {}
		else:
			self.data = {}

		# if class_name is unknown, return data for recognition instead of writing learning vector file
		if class_name != "unknown":
			# add class name to this vector
			self.data.update({"class": class_name})
			self.calc_class = True
		else:
			self.calc_class = False

		self.treetagged = ""

		#print("____________________")
		#print(source)
		if self.filename:
			print("Calculating Vector for: " + (self.filename))
		#print(self.map_dir)
		#print("____________________")

	# PREPROCESSORS
	def readFile(self, filename):
		with open(filename) as f:
			return f.read()

	def writeFeatureMaps(self):
		path = Path(self.map_dir + self.filename + ".json")
		path.touch(exist_ok=True)

		with path.open("w") as f:
			f.write(json.dumps(self.data))

	def applyTreeTagger(self, text):
		if self.treetagged == "":
			tagger = tt.TreeTagger(TAGLANG="de")
			tagged_list = tt.make_tags(tagger.tag_text(self.cleanSource(text)))
			return tagged_list
		else:
			return self.treetagged

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
		Counts all occurence of endings and returns the average rhyme value (rhymes/lines).
		Returns float number From 0->1.0;
		0 means no rhymes, 1 means everything rhymes. From 0.5 up it's likely to be real rhymes.
		"""
		#S.L.
		lines = re.findall("(.*)\n", self.source) 	# takes every line
		endings_dict = {}
		l = 0  #counter for non-empty lines
		for line in lines:
			act_line = re.sub("<.*?>", "", line)     #deletes tags

			if act_line != "":
				l += 1
				lastword = act_line.split()[-1]          #takes last word
				lastword.replace("\s", "").replace("'", "").replace("-", "")  #deletes whitespace, ' and -

				if len(lastword) >= 3:		#checks if lastword is long enough
					lastchars = lastword[-3:]
				elif len(lastword) < 3 and len(lastword) >= 2:
					lastchars = lastword[-2:]
				else:
					lastchars = lastword
				lastchars = re.sub("[0-9]*", "", lastchars)  #deletes lastchars with numbers

				if lastchars != "":
					if lastchars in endings_dict.keys():
						endings_dict[lastchars] += 1                    #counts ending plus 1
					else:
						endings_dict[lastchars] = 1                     #creates new key-value

		rhymes = 0
		for k in endings_dict:
			if endings_dict[k] >= 2:		                   #counts all endings that occures min 2 times
				rhymes += endings_dict[k]

		return (float(rhymes)/l)  #returns average rhyme value; 0-1, from 0.5 up it's likely to be real rhymes. 1 means, everything rhymes.

	def calcRhyme2(self):
		#TODO
		"""
		Takes rhyme schemes and checks a text with them. Giving back 1 if it has a Reimschema, 0 else
		"""
		#S.L.
		lines = re.findall("(.*?)(<.*?>)*[\\n]", self.source)
		endings_list = ["" for i in len(lines)]
		c = 0
		for line in lines:
			act_line = re.sub("<.*?>", "", line)     #nimmt Tags raus
			lastword = act_line.split()[-1]          #nimmt letztes Wort
			lastchars = lastword[-3:]
			lastchars.replace(" ", "").replace(Chr(34), "")  #löscht Leerzeichen und Anführungszeichen
			endings_list[c] = lastchars

			c += 1
		pass
		# nimmt immer 4 Zeilen und überprüft - ob 0 & 2 und 1 & 3 - ob 0 & 1 und 2 & 3 - 0&3 und 1&2 übereinstimmen
		# nimmt 6 Zeilen und überprüft - ob 0&1 und 3&4 und 2&5 - ob 0&2 und (1&3&5| (1&4 und 3&5)) - 0&3 und 1&4 und 2&5 übereinstimmen
		# rhyme_schemes = [[a, a, b, b],[a, b, a,b],[a,b,b,a],[a,a,b,c,c,b],[a,b,a,((b,c,b)|(c,b,c))],[a,b,c,a,b,c]]
		# Paarreim, Kreuzreim, umarmender Reim, Schweifreim, Kettenreim, verschränkter Reim, (Binnenreim?[...a...a...,...b...,...b...])

	def calcMostCommonWords(self):
		"""Zaehlt die 'mostCommonWords' """
		# S.L.
		words = self.source.split()
		mostCommonWords = Counter(words).most_common() 	# list with tuples
		return mostCommonWords

	def calcTerminologicalCongruence(self):
		# TODO Tonio
		pass

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

	def calcWordLengthAvg(self):
		clean_text = re.sub('<.*?>', "", self.source)
		char = 0
		for word in clean_text.split():
			char += len(word)
		return float(char)/len(clean_text)

	def calcWordVariance(self):
		# TODO Lemmata als Basis Tonio
		lemmata = [l[2] for l in self.treetagged]
		#print(set(lemmata))
		return len(set(lemmata))/len(lemmata)

	def calcNEFrequency(self):
		count = 0
		for i in self.treetagged:
			if i[1] == 'NE':
				count += 1
		return float(count)/len(self.treetagged)

	def calcVerbFrequency(self):
		count = 0
		for i in self.treetagged:
			if i[1] == 'VAFIN' or 'VAIMP' or 'VVFIN' or 'VVIMP' or 'VMFIN':
				count += 1
		return float(count)/len(self.treetagged)

	def calcNounFrequency(self):
		count = 0
		for i in self.treetagged:
			if i[1] == 'NN':
				count += 1
		return float(count)/len(self.treetagged)

	# MAIN PROCESSORS
	def finalize(self):

		# if feature needs treetagger insert "self.treetagged = self.applyTreeTagger(self.source)" before update
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
		if "rhyme_average" not in self.data.keys():
			self.data.update({"rhyme_average": self.calcRhyme1()})
		if "word_length_average" not in self.data.keys():
			self.data.update({"word_length_average": self.calcWordLengthAvg()})
		if "word_variance" not in self.data.keys():
			self.treetagged = self.applyTreeTagger(self.source)
			self.data.update({"word_variance": self.calcWordVariance()})
		if "NEFrequency" not in self.data.keys():
			self.treetagged = self.applyTreeTagger(self.source)
			self.data.update({"NE_frequency": self.calcNEFrequency()})
		if "verbFrequency" not in self.data.keys():
			self.treetagged = self.applyTreeTagger(self.source)
			self.data.update({"verb_frequency": self.calcVerbFrequency()})
		if "nounFrequency" not in self.data.keys():
			self.treetagged = self.applyTreeTagger(self.source)
			self.data.update({"noun_frequency": self.calcNounFrequency()})

		#pprint.pprint([i[1] for i in self.treetagged])

		if self.calc_class:
			self.writeFeatureMaps()
			return True
		else:
			return self.data

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("USAGE: python FeatureExtractionAlgorithms.py [class] [filename] [map_dir]\n")
		sys.exit()
	fea = FEA(sys.argv[1], sys.argv[2], sys.argv[3])
	print(fea.finalize())

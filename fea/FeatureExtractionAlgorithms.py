import sys
import json
import re
import os
from pathlib import Path
#from Collections import Counter
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
		m = re.search(".*\/(.*)\..*", source)
		if m:
			self.filename = m.group(1)
		else:
			self.filename = source

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

		self.data.update({"class": class_name})

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

	# EXTRACTION ALGORITHMS
	def calcTextLength(self):
		"""
		Calculates the length of the text and ignores XMl-tags.
		"""
		#S.L.
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
		#S.L.
		## muss noch angepasst werden an: unreine Reime, wenn "" auftaucht
		lines = re.findall("(.*?)[\.|\!|\?|\,|\;|\:|\-]*[\\n]", self.source)    # parser "" und '' umgewandelt? # anpassen
		endings_dict = {}
		for line in lines:
			lastword = line.split()[-1]
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
		
	def calcPhrasesPerParagraph(self):
		splitfile = self.source.splitlines()
		while '' in splitfile:
			splitfile.remove('')
		count = 0
		for line in splitfile:
			if re.match(r'.*<s>.*', line):
				count +=1	
		return float(count)/len(source)

	def calcDigitFrequency(self):
		count = 0 #count per word
		for char in self.source.split():
			if re.match(r'.*\d+', char):
				count += 1
		return float(count)/len(self.source)
		
	def calcPunctuationFrequency(self):
		count = 0 #count per word
		for char in self.source:
			if re.match(r'.*[<punct>|<exclamation>|<question>|<colon>|<semicolon>|<suspension>|<comma>|<thinking>].*', char): 
				count += 1
		return float(count)/len(self.source)



		# S.L.
		# aussortieren von Füllwörtern, Zeichen etc fehlt
		# lemmatisieren
		words = self.source.split()
		mostCommonWords = Counter(words).most_common() 	# list with tuples
		return mostCommonWords


	def calcHashtagFrequency(self):
		count = 0 #count per word
		for char in self.source.split():
			if re.match(r'#[.]*', char):
				count += 1
		return float(count)/len(self.source)

	def calcNEFrequency(self):
		# TODO
		pass

	# MAIN PROCESSORS
	def finalize(self):
		if "sentence_length_avg" not in self.data.keys():
			self.data.update({"sentence_length_avg": self.calcSentenceLengthAvg()})
			#print("calculated sentence_length_avg")
		if "sentence_length_max" not in self.data.keys():
			self.data.update({"sentence_length_max": self.calcSentenceLengthMax()})
			#print("calculated sentence_length_max")
		if "sentence_length_min" not in self.data.keys():
			self.data.update({"sentence_length_min": self.calcSentenceLengthMin()})
			#print("calculated sentence_length_min")
		if "text_length" not in self.data.keys():
			self.data.update({"text_length": self.calcTextLength()})
			#print("calculated text_length")
		if "phrases_per_paragraph" not in self.data.keys():
			self.data.update({"phrases_per_paragraph": self.calcPhrasesPerParagraph()})
			#print("calculated phrases_per_paragraph")
		if "digit_frequency" not in self.data.keys():
			self.data.update({"digit_frequency": self.calcDigitFrequency()})
			#print("calculated digit_frequency")
		if "punctuation_frequency" not in self.data.keys():
			self.data.update({"punctuation_frequency": self.calcPunctuationFrequency()})
			#print("calculated punctuation_frequency")
		if "hashtag_frequency" not in self.data.keys():
			self.data.update({"hashtag_frequency": self.calcHashtagFrequency()})
			#print("calculated hashtag_frequency")
		#if "rhyme_average" not in self.data.keys():
		#	self.data.update({"rhyme_average": self.calcRhyme1()})
		#	print("calculated rhyme_average")

		self.writeFeatureMaps()

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("USAGE: python FeatureExtractionAlgorithms.py [class] [filename] [map_dir]\n")
		sys.exit()
	fea = FEA(sys.argv[1], sys.argv[2], sys.argv[3])
	fea.finalize()

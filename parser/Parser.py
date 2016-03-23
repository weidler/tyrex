import re
from html2text import *

class Parser():

	def __init__(self, filename):
		self.filename = filename
		self.text = self.readFileAtPath(self.filename)

	def readFileAtPath(self, posix_path):
		try:
			with open(posix_path, encoding="utf-8") as f:  # general encoding
				return html2text(f.read())
		except UnicodeDecodeError:
			try:
				with open(posix_path, encoding="latin-1") as f:  # german language encoding
					return html2text(f.read())
			except:
				print("DECODE ERROR")
				return False
		except IOError:
			print("FILE NOT FOUND")
			return False
		except Exception as e:
			print("UNKNOWN ERROR\n" + e)
			return False

	def convertToNormalized(self, unnormalized):
		#sentence bounds

		#return unnormalized  # skip

		phrase = "<s>", "</s>"

		#punctuations
		punct = "<punct>"  #  .
		question = "<question>"  #  ?
		excl = "<exclamation>"  #  !
		susp = "<suspension>"  # ...
		comma = "<comma>"  #  ,
		colon = "<colon>"  #  :
		semicolon = "<semicolon>"  #  ;
		think = "<thinking>"  #  -

		#apostroph
		#direct = ("<speech>", "</speech>")
		#apo = ("<apo>", "</apo>")

		#regex
		phrase_bound = punct + "|" + question + "|" + excl + "|" + "\n{2,}"
		phrase_match = "(?=((" + phrase_bound + "|^)(((.|\s)+?)(" + phrase_bound + "))))"

		#ANNOTATING...

		#tags
		out = re.sub("\.{3,}", susp, unnormalized)
		out = re.sub("\.", punct, out)
		out = re.sub("\?", question, out)
		out = re.sub("\!", excl, out)
		out = re.sub("\,", comma, out)
		out = re.sub("\:", colon, out)
		out = re.sub("\;", semicolon, out)
		out = re.sub("\s- ", think, out)

		out = re.sub("[\*\_]|\#{1,} ", "", out)  # remove markdown
		out = re.sub("\[(.*?|\s*?)\]|\||-{2,}|\t|\/", "", out)  # remove unnecessary characters
		out = re.sub("(\n|^)\s+\n", "\n\n", out)  # remove lines only containing whitespaces
		out = re.sub("\n +", "\n", out)  # remove whitespaces preceding any lines
		out = re.sub("^\s+", "", out)  # remove initial whitespaces
		out = re.sub(" {2,}", " ", out)  # reduce multi space
		out = out.replace("\\", "")

		phrases = re.findall(phrase_match, out)
		clean_phrases = [phrases[i][2] for i in range(len(phrases)) if phrases[i][3] != phrases[i-1][3]]

		out = "".join([phrase[0] + match + phrase[1] for match in clean_phrases])  #sentence bounds

		# order the linebreaks and sentence bounds
		while re.search("[\n\r]\</s\>", out) or re.search("\<s\>[\n\r]", out):
			out = re.sub("\n\<\/s\>", "</s>\n", out)
			out = re.sub("\<s\>[ \t]*\n", "\n<s>", out)

		out = re.sub("<s><\/s>", "", out)

		#out = re.sub("[^\s]<", lambda match: match[0] + " " + match[1], out)  #have all elements seperated by space
		return out

if __name__ == "__main__":
	print("NO WAY")

# in this file, functions will be provided that are used over multiple components of the program

from pathlib import Path

def checkFileExistance(filename):
	while Path(filename).exists():
		answer = input("This file already exists, do you want to overwrite? (Y/n) ")
		if answer in ["Y", "y"]:
			with open(filename, "w") as f: f.write("")
			break
		elif answer in ["N", "n"]:
			filename = input("New path: ")
	return filename

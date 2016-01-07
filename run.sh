#!/bin/bash
# USAGE: run.sh raw_data data [prefix] [filename]
# OPTIONS:		-m	Multiple Files

RAW_DATA=$1
DATA=$2
PREFIX=$3
NORMED_FILE=$3

# PARSER
python3 parser/Parser.py $RAW_DATA $DATA

# FEA
python3 fea/FeatureExtractionAlgorithms.py $NORMED_FILE

# Multiple FEA
# python3 fea/AutomizedFEA.py $PREFIX

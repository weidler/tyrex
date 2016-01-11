#!/bin/bash
# USAGE: run.sh raw_data data map_dir [prefix] [filename]
# OPTIONS:		-m	Multiple Files

RAW_DATA=$1
DATA=$2
MAP_DIR=$3
PREFIX=$4
NORMED_FILE=$4

# PARSER
python3 parser/Parser.py $RAW_DATA $DATA

# FEA
python3 fea/FeatureExtractionAlgorithms.py $NORMED_FILE $MAP_DIR

# Multiple FEA
# python3 fea/AutomizedFEA.py $PREFIX

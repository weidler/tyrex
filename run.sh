#!/bin/bash
# USAGE: run.sh raw_data data map_dir arff_filename [prefix]

RAW_DATA=$1
DATA=$2
MAP_DIR=$3
PREFIX=$4
ARFF_FILE=$5
CLASS="1"

# PARSER
python3 parser/Parser.py $RAW_DATA $DATA;

# Multiple FEA
python3 fea/AutomizedFEA.py $DATA $MAP_DIR;

# BUILD ARFF
python3 ARFFBuilder.py $MAP_DIR $ARFF_FILE;

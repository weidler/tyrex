#!/bin/bash
# USAGE: run.sh raw_data data map_dir arff_filename

RAW_DATA=$1
DATA=$2
MAP_DIR=$3
ARFF_FILE=$4

# CLEAN DIRECTORIES
rm $2*
rm $3*

# PARSER
python3 parser/Parser.py $RAW_DATA $DATA;

# Multiple FEA
python3 fea/AutomizedFEA.py $DATA $MAP_DIR;

# BUILD ARFF
python3 ARFFBuilder.py $MAP_DIR $ARFF_FILE;

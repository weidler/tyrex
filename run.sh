#!/bin/bash
# USAGE: run.sh raw_data data map_dir arff_filename

RAW_DATA=$1
DATA=$2
MAP_DIR=$3
ARFF_FILE=$4

# CLEAN DIRECTORIES
# rm $2*
# rm $3*

# PARSER STEP 1: Create all normed files
python3 parser/Parser.py $RAW_DATA $DATA;

# Multiple FEA STEP 2: Take all normed files and apply FEA on them and save results as JSON maps
python3 fea/AutomizedFEA.py $DATA $MAP_DIR;

# BUILD ARFF
python3 ARFFBuilder.py $MAP_DIR $ARFF_FILE;

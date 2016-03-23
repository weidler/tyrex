#!/bin/bash

usage() {
	cat <<EOF

	TyReX learning Script. Creates an ARFF File with vectors
	learned on raw data.

	Usage: $0 -s DIR -d DIR -m DIR -f FILE [options]

	ARGUMENTS:

		-s DIR		Directory that contains raw data
		-d DIR		Directory that should be filled with parsed
					data (or already consists of)
		-m DIR		Directory that should be filled with
		 			feature maps (or already consists of)
		-f FILE 	Filename of the output ARFF File

	OPTIONS:

		-h 			This help message
		-r			Clear the data (-d) and feature map (-m) directories first
		-j			Use existing JSON DATA

EOF
}

# required checks
has_s=false
has_d=false
has_m=false
has_f=false
required=false

# flags
USE_JSON=false

while getopts :s:d:m:f:rjh opt; do
	case $opt in
		h)
			usage
			exit 1
			required=true;
			;;
		s)
			RAW_DATA=$OPTARG
			has_s=true
			;;
		d)
			DATA=$OPTARG
			has_d=true
			;;
		m)
			MAP_DIR=$OPTARG
			has_m=true
			;;
		f)
			ARFF_FILE=$OPTARG
			has_f=true
			;;

		# OPTIONAL
		r)
			echo "Removing old files..."
			rm $DATA*
			rm $MAP_DIR*
			;;

		j)
			USE_JSON=true
			;;

		\?)
			echo "Invalid option: -$OPTARG" >&2
			echo "'learn.sh -h' for help"
			exit 1
  			;;
		:)
	      	echo "Option -$OPTARG requires an argument." >&2
			echo "'learn.sh -h' for help"
	      	exit 1
		  	;;
	esac
done

# CHECK IF ALL REQUIRED ARGUMENTS ARE GIVEN
if $has_f && $has_s && $has_d && $has_m; then
	required=true
fi

if ! $required; then
	echo "Missing options"
	exit
fi

# DO THE TYREX STUFF!!!
# PARSER
python3 parser/MultiParser.py $RAW_DATA $DATA;

# Multiple FEA
if $USE_JSON; then
	python3 fea/AutomizedFEA.py $DATA $MAP_DIR True;
else
	python3 fea/AutomizedFEA.py $DATA $MAP_DIR;
fi

# BUILD ARFF
python3 ARFFBuilder.py $MAP_DIR $ARFF_FILE;

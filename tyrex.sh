usage() {
	cat <<EOF

	TyReX Script to get the text type of a file

	Usage: $0 FILE [options]

	ARGUMENTS:

		FILE		File, that should be evaluated

	OPTIONS:

		-h 			This help message
		-p			Show propability for that solution

EOF
}

SHOW_PROP=false

while getopts hp o; do
	case $o in
		h)
			usage
			exit 1
			;;
		p)
			SHOW_PROP=true
			;;
	esac
done

python3 recognizeTextType.py $1

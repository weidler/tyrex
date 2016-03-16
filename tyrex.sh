usage() {
	cat <<EOF

	TyReX Script to get the text type of a file

	Usage: $0 FILE

	ARGUMENTS:

		FILE		File, that should be evaluated

	OPTIONS:

		-h 			This help message
		-p			Show probability for that solution

EOF
}

while getopts h o; do
	case $o in
		h)
			usage
			exit 1
			;;
		p)
			;;
	esac
done

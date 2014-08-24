#!/usr/bin/bash

if [[ $# -eq 3 ]]; then
	echo -n "" > $2
	echo -n "" > $3
else
	echo "Please specify the required valid arguments as :: <input file|directory> <output file> <log file>"
	exit 1
fi

INPUT=$1 
OUTPUT=$2
LOGFILE=$3

if [[ -d $INPUT ]]; then
	for input in $(find $INPUT -name '*' ); 
	do
		if [[ -f $input ]];then
			echo -n "" > head_vib.temp
			echo $input >> $LOGFILE
			python $ssf2conll/src/run_dependencies.py $input head_vib.temp $LOGFILE
			python $ssf2conll/src/ssfToConll.py --input-file head_vib.temp --output-file $OUTPUT --log-file $LOGFILE
		fi
	done
else
	python $ssf2conll/src/run_dependencies.py $INPUT head_vib.temp $LOGFILE
	python $ssf2conll/src/ssfToConll.py --input-file head_vib.temp --output-file $OUTPUT --log-file $LOGFILE
fi

if [[ -f head_vib.temp ]];then
	rm head_vib.temp
fi

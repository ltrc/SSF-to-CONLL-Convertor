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
#headPath="/home/riyaz/Tools/ssf2conllconverter/ssf2conll_convertor/dependencies/headcomputation-1.8"
#casePath="/home/riyaz/Tools/ssf2conllconverter/ssf2conll_convertor/dependencies/vibhakticomputation-2.3.2"

if [[ -d $INPUT ]]; then
	for file in $INPUT/*
	do
	echo -n "" > head_vib.temp
	echo $file >> $LOGFILE
	python run_dependencies.py $file head_vib.temp $LOGFILE
	#perl $headPath/headcomputation.pl --path=$headPath -i $file > temp.head
	#perl $casePath/vibhakticomputation.pl --path=$casePath -i temp.head > temp.vib
	python ssfToConll.py --input-file head_vib.temp --output-file $OUTPUT --log-file $LOGFILE
	done
else
	python run_dependencies.py $INPUT head_vib.temp $LOGFILE
	#perl $headPath/headcomputation.pl --path=$headPath -i $INPUT > temp.head
	#perl $casePath/vibhakticomputation.pl --path=$casePath -i temp.head > temp.vib
	python ssfToConll.py --input-file head_vib.temp --output-file $OUTPUT --log-file $LOGFILE
fi

if [[ -f head_vib.temp ]];then
	rm head_vib.temp
fi

%SPEC_FILE%
#
# Generated Dashboard Specification file 
#
# This file gives the specifications to run the system. It contains:
#DO NOT change the naming convention of any of the sections.


%GLOBAL%
#
# Global variables 
#

# Root directory of the system
<ENV>$mt_iiit=/usr/share/Dashboard
#<ENV>$setu=/home/setu/sampark
<ENV>$setu=/home/setu/ilmtmodules/modules/headcomputation/headcomputation-1.8/setu
<ENV>$src=$setu/src
<ENV>$bin=$setu/bin
<ENV>$data_bin=$setu/data_bin
<ENV>$data_src=$setu/data_src
<ENV>$val_data=$setu/val_data

# Other variables used in the generation of executable
# type=int, char, char*
<VAR>$slang=tel
<VAR>$tlang=hin
<VAR>$stlang=tel_hin

# API for PERL,C language
<API lang=perl>$mt_iiit/lib/shakti_tree_api.pl
<API lang=perl>$mt_iiit/lib/feature_filter.pl
<API lang=C>$mt_iiit/c_api_v1/c_api_v1.h
# READER,PRINTER function for language PERL
<READER lang=perl>read
<PRINTER lang=perl>print_tree_file

# READER,PRINTER function for language C
<INCLUDE lang=C>stdio.h
<INCLUDE lang=C>stdlib.h
<READER lang=C>read_ssf_from_file
<PRINTER lang=C>print_tree_to_file

# Output directory for storing temporaries (relative path to current dir)
#<OUTPUT_DIR>OUTPUT.tmp
#<OUTPUT_DIR>$val_data/system/$stlang
<OUTPUT_DIR>/home/setu/module_inout/prune.tmp

# Run in SPEED or DEBUG or USER mode
<MODE>DEBUG
#<MODE>SPEED


%SYSTEM%

# Each module should have a unique identifying name (i.e. unique value for the second column)

# -----------------------------------------------
# Source Language Analyzer Modules (SL)
# -----------------------------------------------

# Prunning 
1	headcomputation		$setu/bin/sl/headcomputation/headcomputation.sh	dep=<START>	intype=1	lang=sh


#!/usr/bin/perl

use Getopt::Long;
GetOptions("help!"=>\$help,"path=s"=>\$vibh_home,"input=s"=>\$input,"output=s",\$output);
print "Unprocessed by Getopt::Long\n" if $ARGV[0];
foreach (@ARGV) {
	print "$_\n";
	exit(0);
}

if($help eq 1)
{
	print "Vibhakti Computation  - Vibhakti Computation Version 1.3\n(14th July 2007 last modified on 19th Sep 2008)\n\n";
	print "usage : ./run-vibh.pl --path=/home/vibhakticomputation-1.3 [-i inputfile|--input=\"input_file\"] [-o outputfile|--output=\"output_file\"] \n";
	print "\tIf the output file is not mentioned then the output will be printed to STDOUT\n";
	exit(0);
}

if($vibh_home eq "")
{
	print "Please Specify the Path as defined in --help\n";
	exit(0);

}

my $src=$vibh_home . "/src";
my $output_tmp=$vibh_home . "/OUTPUT.tmp";
require "$vibh_home/API/shakti_tree_api.pl";
require "$vibh_home/API/feature_filter.pl";
require "$src/ComputeTAM.pl";
require "$src/vibhakti_compute.pl";

if ($input eq "")
{
  $input="/dev/stdin";
}


&read_story($input);

$numBody = &get_bodycount();
for(my($bodyNum)=1;$bodyNum<=$numBody;$bodyNum++)
{

	$body = &get_body($bodyNum,$body);

# Count the number of Paragraphs in the story
	my($numPara) = &get_paracount($body);

#print STDERR "Paras : $numPara\n";

# Iterate through paragraphs in the story
	for(my($i)=1;$i<=$numPara;$i++)
	{

		my($para);
		# Read Paragraph
		$para = &get_para($i);


		# Count the number of sentences in this paragraph
		my($numSent) = &get_sentcount($para);
		# Iterate through sentences in the paragraph
		for(my($j)=1;$j<=$numSent;$j++)
		{

			# Read the sentence which is in SSF format
			my($sent) = &get_sent($para,$j);

			#Copy Vibhakti Info
			&ComputeVibhakti($sent,$vibh_home);

			#Compute TAM
			&ComputeTAM($sent,$vibh_home,$slang);
		}
	}
}

if($output eq "" )
{
	&printstory();
}

else
{
	&printstory_file("$output");
}

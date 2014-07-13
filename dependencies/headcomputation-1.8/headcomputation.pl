#!/usr/bin/perl

use Getopt::Long;
GetOptions("help!"=>\$help,"path=s"=>\$head_home,"input=s"=>\$input,"output=s",\$output);
print "Unprocessed by Getopt::Long\n" if $ARGV[0];
foreach (@ARGV) {
	print "$_\n";
	exit(0);
}

if($help eq 1)
{
	print "Head Computation  - Head Computation Version 1.8\n(30th May 2009)\n\n";
	print "usage : ./run-headCompute.pl --path=/home/headComputation-1.8 [-i inputfile|--input=\"input_file\"] [-o outputfile|--output=\"output_file\"] \n";
	print "\tIf the output file is not mentioned then the output will be printed to STDOUT\n";
	exit(0);
}

if($head_home eq "")
{
	print "Please Specify the Path as defined in --help\n";
	exit(0);

}


my $src=$head_home . "/src";
require "$head_home/API/shakti_tree_api.pl";
require "$head_home/API/feature_filter.pl";
require "$src/copy_np_head.pl";
require "$src/copy_vg_head.pl";
require "$src/single_quote_changeName-0.1.pl";


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
	#	print STDERR "\n $i no.of sent $numSent";

		#print STDERR "Para Number $i, Num Sentences $numSent\n";

		#print $numSent."\n";

		# Iterate through sentences in the paragraph
		for(my($j)=1;$j<=$numSent;$j++)
		{

			#print " ... Processing sent $j\n";

			# Read the sentence which is in SSF format
			my($sent) = &get_sent($para,$j);
			#print STDERR "$sent";
		#	print "check--\n";
		#	&print_tree($sent);
			# Get the nodes of the sentence (words in our case)


			#Copy NP head
		#	&AddID($sent);
			&make_chunk_name($sent);
			&copy_np_head($sent,$head_home);
			#Copy NP VG head
			&copy_vg_head($sent,$head_home);

		}
	}
}

if($output eq "")
{
	&printstory();
}

if($output ne "")
{
	&printstory_file("$output");
}


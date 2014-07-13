##!/usr/bin/perl

# For the details please see get_head.pl
sub copy_np_head
{
	my $sent=@_[0];
	my $vibh_home=@_[1];
	my $src=$vibh_home . "/src";

	require "$vibh_home/API/shakti_tree_api.pl";
	require "$vibh_home/API/feature_filter.pl";
	require "$src/get_head_np.pl";
	&copy_head_np("NP",$sent,$vibh_home);
	
	&copy_head_np("JJP",$sent,$vibh_home);
	&copy_head_np("CCP",$sent,$vibh_home);
	&copy_head_np("RBP",$sent,$vibh_home);
	&copy_head_np("BLK",$sent,$vibh_home);
	&copy_head_np("NEGP",$sent,$vibh_home);
	&copy_head_np("FRAGP",$sent,$vibh_home);
	&copy_head_np("NULL__CCP",$sent,$vibh_home);
	&copy_head_np("NULL__NP",$sent,$vibh_home);
	#&print_tree();
}	#End of Sub
1;

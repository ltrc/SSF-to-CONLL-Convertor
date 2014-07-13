#!/usr/bin/perl

#for details please check get_head.pl
sub copy_vg_head
{
	my $sent=@_[0];
	my $vibh_home = @_[1];
	my $src=$vibh_home . "/src";
	require "$vibh_home/API/shakti_tree_api.pl";
	require "$vibh_home/API/feature_filter.pl";
	require "$src/get_head_vg.pl";


	&copy_head_vg("VGF",$sent,$vibh_home);
	&copy_head_vg("VGNF",$sent,$vibh_home);
	&copy_head_vg("VGINF",$sent,$vibh_home);
	&copy_head_vg("VGNN",$sent,$vibh_home);
	&copy_head_vg("NULL__VGNN",$sent,$vibh_home);
	&copy_head_vg("NULL__VGF",$sent,$vibh_home);
	&copy_head_vg("NULL__VGNF",$sent,$vibh_home);
}
1;


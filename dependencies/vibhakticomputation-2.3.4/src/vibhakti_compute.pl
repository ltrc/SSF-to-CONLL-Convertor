#!/usr/bin/perl
#use strict;
#use GDBM_File;
#the module prunes multiple feature structure (NN, NNP, PRP at present), it also removes the parsarg node in the NP and adds it to its noun fs.
#$&compute_vibhakti;
sub ComputeVibhakti
{
	my $sent=@_[0];
	my $vibh_home = @_[1];

	#my $delete;	#keeps count of all the deleted node, helps in locating node obtained before deletion.

	#get all the noun nodes in the tree, the noun will be case marked '1' if a vibhakti is present, else case is '0'

	#my @all_leaves = &get_leaves();
	#&read(@_[0]);	
	my @all_children_NP =&get_nodes(3,"NP",$sent); #gets all the NP nodes
	my @all_children_RBP =&get_nodes(3,"RBP",$sent); #gets all the RBP nodes
        my @all_children = (@all_children_NP , @all_children_RBP); #contains all the NP and RBP nodes
        my @all_children = sort { $a <=> $b } @all_children;
	
	foreach $node(@all_children)
	{

		my @node_leaves=&get_leaves_child($node,$sent); #gets leaf nodes of NP or RBP node
		
 	               
		$position="";
		$nhead=0;
		$f4=&get_field($node,4,$sent); # gets feature structure
		my $string_fs = &read_FS($f4, $sent);
		
		#gets head and vibhakti values 
		
		my @head_value = &get_values("head", $string_fs, $sent); 
		my @vibh_value=&get_values("vib", $string_fs, $sent);
		$vibh_chunk=$vibh_value[0]; 
		#iterates through each leaf node and gets postag, word, fs
		
		foreach $NP_child(@node_leaves)
		{
			my $pos = &get_field($NP_child,3,$sent);
			my $word = &get_field($NP_child,2,$sent);
			my $fs = &get_field($NP_child,4,$sent);
			my $str_fs=&read_FS($fs,$sent);
			my @name_value=&get_values("name",$str_fs,$sent); 
			if($pos eq "NN" or $pos eq "NNP" or $pos eq "PRP")
			{
				$nhead=1;
				$flag=0;
				$prev_RB=0;
				$flag_NN=1
			}
			if($pos eq "RB")
			{
				$flag=1;
				$prev_RB = 1;
				$flag_NN=0
			        
			}
			
			if($head_value[0] eq $name_value[0])
			{
				$num=$NP_child-$node; #gives position of the leaf with respect to the node
				
				# modifies the value of vpos(position) in a chunk

				if($position ne "")
				{$position=$position."_"."vib$num";} 
				if($position eq "")
				{$position="vib$num";}

			}
			
			
			#Adds the RP vibhakti to vpos
			
			if($pos eq "RP")
			{      
				if($position ne "")
				{
					$position=$position."_"."RP";
				}
				else
				{
					next;
				}
			}
			
			
			if($pos eq "PSP" or $pos eq "NST" and $nhead==1)
			{       
				#Adds position of vibhakti in vpos(position) value

				if($position ne "")
				{
					$num=$NP_child-$node;
					$position=$position."_".$num;
				}
				
				else
				{
					$position=$NP_child-$node;
				}
				my $val_fs=&get_field($NP_child, 4,$sent);

				$FSreference = &read_FS($val_fs,$sent); #reads feature structure of the leaf
				my @cur_vibhakti = &get_values("lex",$FSreference); #fetches the lexical value of vibhakti
				my @cur_vib_vib = &get_values("vib",$FSreference); 
				
				#adds the lexical value of vibhakti to vibh_chunk

				if($vibh_chunk ne "")
				{
					$vibh_chunk=$vibh_chunk . "_" . $cur_vibhakti[0];
				}
				else
				{
					$vibh_chunk="0_".$cur_vibhakti[0];
				}
					push(@remove,$NP_child);

			}
			
		}
		if($vibh_chunk)
			{
				my @vibh_chunk_arr=();
				push @vibh_chunk_arr,$vibh_chunk; #pushes the value of vibh_chunk in vibh_chunk_arr 

				my $head_node=&get_field($node,4,$sent); 
				my $FSreference1 = &read_FS($head_node,$sent); #gets FS value
				&update_attr_val("vib", \@vibh_chunk_arr,$FSreference1,$sent); #updates value of attribute vib
				
				# Modifies the value of fs by adding new attribute vpos that will be in output.
				
				my $string=&make_string($FSreference1,$sent);
				my ($x,$y)=split(/>/,$string);
				my $new_head_fs=$x." vpos=\"$position\">"; 
				&modify_field($node,4,$new_head_fs,$sent); 

				undef $head_word;
				undef $new_string;
			}
	}
        #Deletes the leaves containing vibhakti.
	$delete=0;
	foreach (@remove)
	{
		&delete_node($_-$delete,$sent);
		$delete++;
	}
	delete @remove[0..$#remove];
}
1;


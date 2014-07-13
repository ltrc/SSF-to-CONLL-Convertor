#!/usr/bin/perl

sub copy_head_np
{
	my ($pos_tag)=$_[0];	#array which contains all the POS tags
	my ($sent)=$_[1];	#array in which each line of input is stored
	my $vibh_home = $_[2];	#stores the path 
	my %hash=();
	if($pos_tag =~ /^NP/)
	{
		$match = "NN"; #Modified in version 1.4
			       #For NST
	}
	if($pos_tag =~ /^V/ )
	{
		$match = "V";
	}
	if($pos_tag =~ /^JJP/ )
	{
		$match = "J";
	}
	if($pos_tag =~ /^CCP/ )
	{
		$match = "CC";
	}
	if($pos_tag =~ /^RBP/ )
	{
		$match = "RB";
	}
	my @np_nodes = &get_nodes(3,$pos_tag,$sent);#gives the nodes at which each pos_tag tag matches(index of chunk start)
	
	for($i=$#np_nodes;$i>=0;$i--)
	{	
		my (@childs)=&get_children($np_nodes[$i],$sent);#gives the nodes(index) at which childs(words in a chunk) are found
		$j = $#childs;
		while($j >= 0)
		{
			#$f1=node id in decreasing order
			#$f2=tokens(words) in dec order
			#$f3=word tags
			#$f4=feature structure
#			print "$childs[$j]"."\n";				"--"."@sent"."\n";
			my($f0,$f1,$f2,$f3,$f4)=&get_fields($childs[$j],$sent);
			$word=$f2;
#			print "--".$f4,"---\n";
			$f4=~s/\//&sl/;
			my ($x,$f4)=split(/</,$f4);
			my ($f4,$x)=split(/>/,$f4);
			$f4=~s/</&angO/;
			$f4=~s/>/&angC/;
			$f4="<".$f4.">";
#			print "3 start head>>".$f4."<<\n";
			my $fs_ref = &read_FS($f4);
#			print "3 end head\n";
                        my @name_val = &get_values("name", $fs_ref);
			
#print "$word"."\n";
			if($f3 eq "PRP") ##to make sure that the pronouns are identified correctly
			{
				$f3 = "NN";
			}

			if($f3 eq "WQ") ##to make sure that the pronouns are identified correctly
			{
				$f3 = "NN";
			}

			if($f3=~/^$match/)
			{
				if($hash{$f2} eq "")
				{
					$hash{$word}=1;
				}
				elsif($hash{$f2} ne "")
				{
					$hash{$word}=$hash{$word}+1;
				}
				$id=$hash{$word};
				my ($x,$y)=split(/>/,$f4);
				$x =~ s/ name=[^ >]+//;
				if($id==1)
				{
					$att_val="$word";
				}
				elsif($id!=1)
				{
					$att_val="$word"."_"."$id";
				}
				
				#$new_fs = $x." head=\"$name_val[0]\">";
				$new_fs = $x." head=$name_val[0]>";
				#my $new_head_fs=$x." name=\"$att_val\">";
				#&modify_field($childs[$j],4,$new_head_fs,$sent);
				last;
			}
			elsif($j == 0)
			{
				
				my($f0,$f1,$f2,$f3,$f4)=&get_fields($childs[$#childs],$sent);
				#-----------------modifications to handle PRP and PSP case------------------
				$change=$#childs;	

			$f4=~s/\//&sl/;
			my ($x,$f4)=split(/</,$f4);
			my ($f4,$x)=split(/>/,$f4);
			$f4=~s/</&angO/;
			$f4=~s/>/&angC/;
			$f4="<".$f4.">";
				while(1)
				{
					if($f3 eq "PSP" or $f3 eq "PRP")
					{
						$change=$change-1;
						if($childs[$change] eq "") 	##Modifications per Version 1.3
						{				##To handle NP chunks with single PSP
							$change=$change+1;	##
							last;			##
						}
						($f0,$f1,$f2,$f3,$f4)=&get_fields($childs[$change],$sent);
					}
					else
					{
						last;
					}
				}

				
				$new_fs = $f4;
				$word=$f2;
				my $fs_ref = &read_FS($f4);
                                my @name_val = &get_values("name", $fs_ref);

				if($hash{$f2} eq "")
				{
					$hash{$word}=1;
				}
				elsif($hash{$f2} ne "")
				{
					$hash{$word}=$hash{$word}+1;
				}
				$id=$hash{$word};
				#--------------------------------------------------------------------------------
				my ($x,$y)=split(/>/,$f4);
				$x =~ s/ name=[^ >]+//;
				if($id==1)
				{
					$att_val="$word";
				}
				elsif($id!=1)
				{
					$att_val="$word"."_"."$id";
				}
				#$new_fs = $x." head=\"$name_val[0]\">";
				$new_fs = $x." head=$name_val[0]>";
				#my $new_head_fs=$x." name=\"$att_val\">";
				#&modify_field($childs[$change],4,$new_head_fs,$sent);
			}
			$j--;
		}
		($f0,$f1,$f2,$f3,$f4) = &get_fields($np_nodes[$i],$sent);
		if($f4 eq '')
		{
			##print "1check ---$new_fs\n";
			&modify_field($np_nodes[$i],4,$new_fs,$sent);

			($f0,$f1,$f2,$f3,$f4) = &get_fields($np_nodes[$i],$sent);
			$fs_ptr = &read_FS($f4,$sent);
			#print "---x--$x\n";
			#&add_attr_val("name",$head_att_val,$fs_ptr,$sent);
			($f0,$f1,$f2,$f3,$f4) = &get_fields($np_nodes[$i],$sent);

			#print "2check ---$f4\n";
			
		}
		else
		{
			$fs_ptr = &read_FS($f4,$sent);
			$new_fs_ptr = &read_FS($new_fs,$sent);
			&merge($fs_ptr,$new_fs_ptr,$sent);
			$fs_string = &make_string($fs_ptr);
			&modify_field($np_nodes[$i],4,$fs_string,$sent);
			($f0,$f1,$f2,$f3,$f4) = &get_fields($np_nodes[$i],$sent);
			$fs_ptr = &read_FS($f4,$sent);
			#&add_attr_val("name",$head_att_val,$fs_ptr,$sent);

#&modify_field($np_nodes[$i], 4, $head_att_val,$sent);
		}
	}
	#print "hiii--\n"
	#&print_tree();
	#print "hiii\n";
}
1;

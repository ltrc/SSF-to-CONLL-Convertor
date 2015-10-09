#!/usr/bin/perl


#&AddID($ARGV[0]);
sub copy_head_vg
{
	my($pos_tag) = $_[0];	#array which contains all the POS tags
	my($sent) = $_[1];	#array in which each line of input is stored
	my $vibh_home = $_[2];	#stores the path 
	require "$vibh_home/API/shakti_tree_api.pl";
	require "$vibh_home/API/feature_filter.pl";

	my %hash=();
	if($pos_tag =~ /^NP/)
	{
		$match = "N";
	}
	if($pos_tag =~ /^V/ )
	{
		$match = "VM";
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
	
	@np_nodes = &get_nodes(3,$pos_tag,$sent);
	for($i=$#np_nodes; $i>=0; $i--)
	{
		my(@childs) = &get_children($np_nodes[$i],$sent);
		$j = 0;
		while($j <= $#childs)
		{
			#$f1=node id in decreasing order
			#$f2=tokens(words) in dec order
			#$f3=word tags
			#$f4=feature structure
			my($f0,$f1,$f2,$f3,$f4) = &get_fields($childs[$j],$sent);
			$word=$f2;
			$f4=~s/\//&sl/;
			my ($x,$f4)=split(/</,$f4);
			my ($f4,$x)=split(/>/,$f4);
			$f4=~s/</&angO/;
			$f4=~s/>/&angC/;
			$f4="<".$f4.">";
			#if($f3 =~ /^$match/) 
			if($f3 eq $match) 
			{
				$new_fs = $f4;

				my $fs_ref = &read_FS($f4);	#feature structure is sent to function where all the categories are dealt
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
                                #&modify_field($childs[$j],4,$new_fs,$sent);
				last;
			}
			elsif($j == 0)
			{
				my($f0,$f1,$f2,$f3,$f4) = &get_fields($childs[$#childs],$sent);
				$word=$f2;
			$f4=~s/\//&sl/;
			my ($x,$f4)=split(/</,$f4);
			my ($f4,$x)=split(/>/,$f4);
			$f4=~s/</&angO/;
			$f4=~s/>/&angC/;
			$f4="<".$f4.">";

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
                                #&modify_field($childs[$#childs],4,$new_fs,$sent);
			}
			$j++;
		}
		($f0,$f1,$f2,$f3,$f4) = &get_fields($np_nodes[$i],$sent);
		if($f4 eq '')
		{
			&modify_field($np_nodes[$i],4,$new_fs,$sent);
		}
		else
		{
			$fs_ptr = &read_FS($f4,$sent);
			$new_fs_ptr = &read_FS($new_fs,$sent);
			&merge($fs_ptr,$new_fs_ptr,$sent);
			$fs_string = &make_string($fs_ptr,$sent);
			&modify_field($np_nodes[$i],4,$fs_string,$sent);
		}
	}
}
1;

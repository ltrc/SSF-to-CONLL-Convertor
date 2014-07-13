#!/usr/bin/perl

#use strict;
sub make_chunk_name()
{
	my($i, @leaves, $new_fs, @tree, $line, $string, $file, @lines, @string2, $string_ref1, $string1, $string_name);

	$input = $_[0];
	my %hash_index;
	my %hash_chunk;
	my @final_tree;
#&read_story($input);
	my @tree = &get_children(0, $input);
	my $ssf_string = &get_field($tree[0], 3, $input);
	if($ssf_string eq "SSF")
	{
		@final_tree = &get_children(1, $input);
	}
	else
	{
		@final_tree = @tree;
	}
	my $k, $index=0, $count=0, $index_chunk=0;
	@tree = &get_children($s,$input);
	foreach $i(@final_tree)
	{
		$string = &get_field($i, 4,$input);
		@leaves = &get_children($i,$input);
		my $string_fs = &read_FS($string, $input);

		foreach $m(@leaves)
		{
			$string1 = &get_field($m, 4,$input);
			$string_fs1 = &read_FS($string1, $input);


			$new_fs = &make_string($string_fs1, $input);
			&modify_field($m, 4, $new_fs, $input);
		}
	}

	foreach $i(@final_tree)
	{
		my $count_chunk=0;
		$index_chunk++;
		$string = &get_field($i, 4, $input);
		$string_fs = &read_FS($string, $input);

		my @old_value_name = &get_values("name", $string_fs, $input);
		#print @old_value_name,"\n";
		if($old_value_name[0]=~/\'/ or $old_drel[0]=~/\"/)
		{
			$old_value_name[0]=~s/\'//g;
			$old_value_name[0]=~s/\"//g;
		}

		my @chunk = &get_field($i, 3, $input);
		for ($ite1=1; $ite1<$index_chunk; $ite1++)
		{
			my $actual_chunk_name = $hash_chunk{$ite1};
			my @chunk_name_split = split(/__/, $actual_chunk_name);
			if($chunk_name_split[0] eq $chunk[0])
			{
				$count_chunk++;
			}
		}
		my @chunk1;
		if($count_chunk == 0)
		{
			$hash_chunk{$index_chunk} = "$chunk[0]"."__1";
			$chunk1[0] = $chunk[0];
		}
		else
		{
			$new_count_chunk = $count_chunk+1;
			$chunk1[0] = "$chunk[0]"."$new_count_chunk";
			$hash_chunk{$index_chunk} = "$chunk[0]"."__$new_count_chunk";
		}
		foreach $m_drel(@final_tree)
		{
			my $string_child = &get_field($m_drel, 4, $input);
			my $string_fs_child = &read_FS($string_child, $input);

			my @old_drel = &get_values("drel", $string_fs_child, $input);
			my @old_dmrel = &get_values("dmrel", $string_fs_child, $input);
			my @old_reftype = &get_values("reftype", $string_fs_child, $input);
			my @old_coref = &get_values("coref", $string_fs_child, $input);
			#my @old_attr = &get_attributes($string_fs_child, $input);

			if($old_drel[0]=~/\'/ or $old_drel[0]=~/\"/)
			{
				$old_drel[0]=~s/\'//g;
				$old_drel[0]=~s/\"//g;
			}

			if($old_dmrel[0]=~/\'/ or $old_dmrel[0]=~/\"/)
			{
				$old_dmrel[0]=~s/\'//g;
				$old_dmrel[0]=~s/\"//g;
			}

			if($old_reftype[0]=~/\'/ or $old_reftype[0]=~/\"/)
			{
				$old_reftype[0]=~s/\'//g;
				$old_reftype[0]=~s/\"//g;
			}

			if($old_coref[0]=~/\'/ or $old_coref[0]=~/\"/)
			{
				$old_coref[0]=~s/\'//g;
				$old_coref[0]=~s/\"//g;
			}

			my @old_drel_name = split(/:/, $old_drel[0]);
			my @old_dmrel_name = split(/:/, $old_dmrel[0]);
			my @old_reftype_name = split(/:/, $old_reftype[0]);
			my @old_coref_name = split(/:/, $old_coref[0]);

			if(($old_drel_name[1] eq $old_value_name[0]) && ($old_drel_name[1] ne ""))
			{
				my @new_drel;
				$new_drel[0] = "$old_drel_name[0]:$chunk1[0]";

				&del_attr_val("drel", $string_fs_child, $input);
#				&add_attr_val("drel", \@new_drel, $string_fs_child, $input);
			}

			if(($old_dmrel_name[1] eq $old_value_name[0]) && ($old_dmrel_name[1] ne ""))
			{
				my @new_dmrel;
				$new_dmrel[0] = "$old_dmrel_name[0]:$chunk1[0]";

				&del_attr_val("dmrel", $string_fs_child, $input);
#				&add_attr_val("dmrel", \@new_dmrel, $string_fs_child, $input);
			}

			if(($old_reftype_name[1] eq $old_value_name[0]) && ($old_reftype_name[1] ne ""))
			{
				my @new_reftype;
				$new_reftype[0] = "$old_reftype_name[0]:$chunk1[0]";

				&del_attr_val("reftype", $string_fs_child, $input);
#				&add_attr_val("reftype", \@new_reftype, $string_fs_child, $input);
			}

			if(($old_coref_name[0] eq $old_value_name[0]) && ($old_coref_name[0] ne ""))
			{
				my @new_coref;
				$new_coref[0] = $chunk1[0];

				&del_attr_val("coref", $string_fs_child, $input);
#				&add_attr_val("coref", \@new_coref, $string_fs_child, $input);
			}

#			my $name_attribute_chunk = &make_string($string_fs_child, $input);
#			&modify_field($m_drel, 4, $name_attribute_chunk, $input);
		}
		
		&del_attr_val("name", $string_fs, $input);
#		&add_attr_val("name", \@chunk1, $string_fs, $input);

#		my $name_fs_chunk = &make_string($string_fs, $input);
#		&modify_field($i, 4, $name_fs_chunk, $input);

		my $string1 = &get_field($i, 4, $input);
		my $attr = &read_FS($string1, $input);
		#my @attribute_array = &get_attributes($attr, $input);

		#$count=@attribute_array;
		#print $count, "\n";
	}

	foreach $i(@final_tree)
	{
		$string = &get_field($i, 4, $input);
		@leaves = &get_children($i, $input);

		foreach $m(@leaves)
		{
			$count=0;
			$index++;
			$string2 = &get_field($m, 4, $input);
			$string_fs2 = &read_FS($string2, $input);
			my @token = &get_field($m, 2, $input);
			for ($ite=1; $ite<$index; $ite++)
			{
				my $actual_name = $hash_index{$ite};
				my @name_split = split(/__/, $actual_name);
				if($name_split[0] eq $token[0])
				{
					$count++;
				}
			}
			if($count == 0)
			{
				my @token1;
				$token1[0] = $token[0];
				&del_attr_val("name", $string_fs2, $input);
				&add_attr_val("name", \@token1, $string_fs2, $input);
				my $name_fs = &make_string($string_fs2, $input);
				&modify_field($m, 4, $name_fs,$input);
				$hash_index{$index} = "$token[0]"."__1";
			}
			else
			{
				$new_count = $count+1;
				my @new_token = "$token[0]"."$new_count";
				&del_attr_val("name", $string_fs2, $input);
				&add_attr_val("name", \@new_token, $string_fs2,$input);
				my $name_fs = &make_string($string_fs2,$input);
				&modify_field($m, 4, $name_fs, $input);
				$hash_index{$index} = "$token[0]"."__$new_count";
			}

		}
	}
}

1;

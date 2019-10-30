#!/usr/bin/env perl
#

#
# Generate linker script to only expose symbols of the public API
#

@funcs = ();
my $last_line = "";
while (<>) {
    chomp;

    if (/^(\S+.*\s+\**)?(serdes_\S+)\s*\(/) {
	$sym = $2;
	# Ignore functions marked as unused since they wont generate
	# any symbols and the Solaris linker warns about that.
	if ("$last_line.$_" !~ /(SERDES_UNUSED|__attribute__\(\(unused\)\))/) {
	    push(@funcs, $sym);
	}
	$last_line = "";

    } else {
	$last_line = $_;
    }
}


print "# Automatically generated by lds-gen.pl - DO NOT EDIT\n";
print "{\n global:\n";
if (scalar @funcs == 0) {
    print "    *;\n";
} else {
    foreach my $f (sort @funcs) {
        print "    $f;\n";
    }

    print " local:\n    *;\n";
}

print "};\n";


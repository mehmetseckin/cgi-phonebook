#!/usr/bin/perl
use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my $filename = "files/phone_book.txt";
my (%names, %phones, %addresses);
my %_GET = get_HTTP_GET_data();
my %_POST = get_HTTP_POST_data();
fetch_phonebook_info(\%names, \%phones, \%addresses, $filename);
get_header();
print hr;
if(defined $_POST{"submit"}) {
	list_search($_POST{"search"}, $filename);
	get_footer();
}
if(defined $_GET{"id"} && $_GET{"id"} =~ /^\d+$/) {
	print <<EOF;
	<table style="border: 1px solid; text-align: left;">
		<tr>
			<th>Name</th>
			<th>Phone Number</th>
			<th>Address</th>
		</tr>
		<tr>
			<td width="240px">$names[$_GET{"id"}]</td>
			<td width="240px">$phones[$_GET{"id"}]</td>
			<td>$addresses[$_GET{"id"}]</td>
		</tr>
	</table>
	<p>You can now close this page or go <span style="color: blue; text-decoration: underline;" id="back" onclick="javascript:window.history.back();">back</span></p>
EOF
get_footer();
}
# if code reaches here, that means "id" is not specified. Provide a link list to the user.
list_all($filename);
get_footer();
sub list_all { # params: filename
	my $filename = shift;
	my @vals;
	open FILE, $filename or die $!;
	print "<ul>";
	while (<FILE>) {
		next if($_ =~ /^#/ || $_ =~ /^\s*$/); # skip if comment or blank line...
		@vals = split(/\|/, $_);
		print "<a href=\"?id=".@vals[0]."\">";
		print "<li>".@vals[1]."</li>";
		print "</a>";
	}
	print "</ul>";
}
sub list_search { # params: search_query, filename
	my $query = shift;
	my $filename = shift;
	open FILE, $filename or die $!;
	print "<ul>";
	while (<FILE>) {
		next if($_ =~ /^#/ || $_ =~ /^\s*$/); # skip if comment or blank line...
		@vals = split(/\|/, $_);
		if(@vals[1] =~ /$query/i) {
			print "<a href=\"?id=".@vals[0]."\">";
			print "<li>".@vals[1]."</li>";
			print "</a>";
		}
	}
	print "</ul>";
}
sub fetch_phonebook_info { # params: three hashreferences for names, phones and addresses, filename of the phonebook file.
	my %names = shift; my %phones = shift; my %addresses = shift; my $filename = shift;
	my @vals;
	open FILE, $filename or die $!;
	while (<FILE>) {
		chomp($_);	
		next if($_ =~ /^#/ || $_ =~ /^\s*$/); # skip if comment or blank line...
		@vals = split(/\|/, $_);
		$names["@vals[0]"] = @vals[1];
		$phones["@vals[0]"] = @vals[2];
		$addresses["@vals[0]"] = @vals[3];
	}
	close(FILE);
}
sub get_HTTP_GET_data {  # Decode the url of this script and return a hash of HTTP_GET variables.
	local ($buffer, @pairs, $pair, $name, $value, %FORM);
    $ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
    if ($ENV{'REQUEST_METHOD'} eq "GET")
    {
	$buffer = $ENV{'QUERY_STRING'};
    }
    @pairs = split(/&/, $buffer);
    foreach $pair (@pairs)
    {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%(..)/pack("C", hex($1))/eg;
	$FORM{$name} = $value;
    }
	return %FORM;
}
sub get_HTTP_POST_data { # Get all the HTTP POST variables and return a hash of them
	local %data;
	foreach my $p (param()) {
		$data{$p} = param($p);
	}
	return %data;
}
sub get_header { # Print page headers and menu and stuff
	print header;
	print start_html("Phonebook v1");
	print h1("Phonebook v1");
	print '<div style="float: right; display: inline;"><a href="phonebook.cgi">Home</a></div><form name="search_form" method="POST" action=""><input type="text" name="search" value="Search..."><input type="submit" name="submit" value=">"></form><div style="clear:both;"></div>';
}
sub get_footer { # Print footer.
	print hr;
	print "<center>&copy; <a href=\"http://mehmetseckin.com\">Mehmet Seckin</a>, 2012, All rights reserved.</center>";
	print end_html();
	exit;
}

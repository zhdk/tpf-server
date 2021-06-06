// Server side implementation of UDP client-server model
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define DEFAULTPORT 4460
#define MAXLINE 1024
#define NADDR 3

// Driver code
int main(int argc,  char*  argv[]) {
    int port = DEFAULTPORT;
    int sockfd;
    char buffer[MAXLINE];
    char addrstr[INET_ADDRSTRLEN];
    struct sockaddr_in servaddr;
    struct sockaddr_in addr[NADDR];
    struct sockaddr_in *from = NULL;
    struct sockaddr_in *client1 = NULL;
    struct sockaddr_in *client2 = NULL;
    struct sockaddr_in *to = NULL;

    if (argc > 1) port = atoi (argv[1]);
    if (port < 1024 || port >= 65536) {
        fprintf (stderr, "Invalid port specified\n");
        exit(EXIT_FAILURE);
    }

    // Creating socket file descriptor
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        fprintf (stderr, "Socket creation failed\n");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    for (int i = 0; i < NADDR; i++) {
        memset(&addr[i], 0, sizeof(addr[i]));
    }

    servaddr.sin_family    = AF_INET; // IPv4
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    if ( bind(sockfd, (const struct sockaddr *)&servaddr,
            sizeof(servaddr)) < 0 )
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    int len, n;
    int p = 0;
    len = sizeof(from);  //len is value/resuslt
    from = &addr[p];
    while(1) {
        n = recvfrom(sockfd, (char *)buffer, MAXLINE,
                    MSG_WAITALL, ( struct sockaddr *) from,
                    &len);
        buffer[n] = '\0';
        if (client1 && client2) {
            if (from->sin_addr.s_addr == client1->sin_addr.s_addr && from->sin_port == client1->sin_port) {
                to = client2;
            } else
            if (from->sin_addr.s_addr == client2->sin_addr.s_addr && from->sin_port == client2->sin_port) {
                to = client1;
            } else {
                // rotate by one
                p = (p - 1 + NADDR) % NADDR;
                client1 = &addr[p];
                client2 = &addr[(p+1)%NADDR];
                from = &addr[(p+2)%NADDR];
                to = client2;
            }
            sendto(sockfd, (const char *)buffer, n,
                MSG_CONFIRM, (const struct sockaddr *) to, len);
        }
        if (!client1 ) {
            client1 = from;
            from = &addr[p+1];
        }
        else if (!client2) {
            client2 = from;
            from = &addr[p+2];
        }
    }
    return 0;
}

// Server side implementation of UDP client-server model
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define DEFAULTPORT 4460
#define MAXLINE 65536
#define TOKENMARK "_TOKEN "

struct link {
    struct sockaddr_in addr;
    struct link *peer;
    struct link *next;
};
typedef struct link *link_p;

struct token {
    char code[20];
    link_p client;
    struct token *next;
};
typedef struct token *token_p;

void addlink (link_p *link_head, link_p client1, link_p client2);

void addtoken (token_p *token_head, link_p *link_head, char *code, link_p client);

bool has_same_address(link_p client1, link_p client2);

link_p link_head = NULL;
token_p token_head = NULL;

int main(int argc,  char*  argv[]) {
    int port = DEFAULTPORT;
    int sockfd;
    char data[MAXLINE];
    char addrstr[INET_ADDRSTRLEN];
    struct sockaddr_in servaddr;
    struct sockaddr_in fromaddr;
    link_p incoming;

    if (argc > 1) port = atoi (argv[1]);
    if (port < 1024 || port >= 65536) {
        fprintf (stderr, "Invalid port specified\n");
        exit(EXIT_FAILURE);
    }

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        fprintf (stderr, "Socket creation failed\n");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    memset(&fromaddr, 0, sizeof(servaddr));

    servaddr.sin_family    = AF_INET; // IPv4
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    if ( bind(sockfd, (const struct sockaddr *)&servaddr,
            sizeof(servaddr)) < 0 )
    {
        fprintf(stderr, "bind failed\n");
        exit(EXIT_FAILURE);
    }

    int len, n;
    len = sizeof(fromaddr);  //len is value/resuslt
    incoming = (struct link *)malloc (sizeof(struct link));
    incoming->peer = NULL;
    incoming->next = NULL;
    while(1) {
        n = recvfrom(sockfd, (char *)data, MAXLINE,
                    MSG_WAITALL, (struct sockaddr *) &fromaddr, &len);
        incoming->addr = fromaddr;
        data[n] = '\0';
        if (strncmp(data, TOKENMARK, 7) == 0) {
            if (data[n-1] == '\n') data[n-1] = '\0';
            char code[20];
            strncpy (code, data+7, 19);
            code[19] = '\0';
            addtoken (&token_head, &link_head, code, incoming);
            incoming = (struct link *)malloc (sizeof(struct link));
            continue;
        }

        if (link_head) {
            link_p p = link_head;
            if (has_same_address(p, incoming)) {
                sendto(sockfd, (const char *)data, n,
                    MSG_CONFIRM, (const struct sockaddr *) &p->peer->addr, len);
                continue;
            }
            do {
                p = p->next;
                if (has_same_address(p, incoming)) {
                    sendto(sockfd, (const char *)data, n,
                        MSG_CONFIRM, (const struct sockaddr *) &p->peer->addr, len);
                    break;
                }
            } while (p->next != NULL);
        }
    }
    return 0;
}

void addtoken (token_p *token_head, link_p *link_head, char *code, link_p client)
{
    token_p p, new;
    new = (struct token *)malloc (sizeof(struct token));
    if (!new) {
        fprintf (stderr, "malloc for token failed.\n");
        exit(EXIT_FAILURE);
    }
    strcpy(new->code, code);
    new->client = client;
    new->next = NULL;

    if (!*token_head) {
        *token_head = new;
    } else {
        p = *token_head;
        // append to linked list
        while (p->next != NULL) {
            p = p->next;
        }
        p->next = new;
        // find match
        p = *token_head;
        do {
            if (strcmp(p->code, new->code) == 0) {
                addlink(link_head, p->client, new->client);
                break;
            }
            p = p->next;
        } while (p->next != NULL);

    }
}

bool has_same_address(link_p client1, link_p client2) {
    if (client1->addr.sin_addr.s_addr == client2->addr.sin_addr.s_addr &&
        client1->addr.sin_port == client2->addr.sin_port) {
        return true;
    } else {
        return false;
    }
}

void addlink (link_p *link_head, link_p client1, link_p client2) {
    client1->peer = client2;
    client2->peer = client1;
    if (!*link_head) {
        *link_head = client1;
        (*link_head)->next = client2;
    } else {
        link_p p;
        p = *link_head;
        while (p->next != NULL) {
            p = p->next;
        }
        p->next = client1;
        p = p->next;
        p->next = client2;
    }
}

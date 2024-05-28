#pragma once

#include <stdint.h>
#include <stdbool.h>

//We commonly use bit fields to represent protocol states
//                 64 32 16  8  4  2  1
// ASP_NO_STATE      0  0  0  0  0  0  0
// ASP_IDLE          0  0  0  0  0  0  1
// ASP_CONNECTED     0  0  0  0  0  1  0
// ASP_SEND_DATA          0  0  0  0  1  0  0
// ASP_CLOSED        0  0  0  1  0  0  0
// ASP_ERROR         0  0  1  0  0  0  0
// ASP_PENDING       0  1  0  0  0  0  0
// ASP_ACK           1  0  0  0  0  0  0


//ECHO PROTOCOL INFORMATION
//Protocol States
typedef uint8_t         asp_mtype_t;
#define ASP_INITIAL_STATE ASP_IDLE
#define ASP_NO_STATE     0x00
#define ASP_IDLE         0x01
#define ASP_CONNECTED    0x02
#define ASP_SEND_DATA    0x04       // Server sends an audio chunk
#define ASP_CLOSED       0x08
#define ASP_ERROR        0x10
#define ASP_PENDING      0x20
#define ASP_ACK          0x40
#define ASP_DONE         0x60       // Server is done sending data


#define ASP_STATE_SZ     sizeof(uint8_t)

//ACK IS TO ACKNOWLEDGE SO WE CAN COMBINE AND CHECK FOR ITS
//PRESENCE
#define ASP_CONN_ACK              ASP_CONNECTED         | ASP_ACK
#define ASP_SEND_DATA_ACK         ASP_SEND_DATA         | ASP_ACK       // Client acknowledgement when data has been received
#define ASP_CLOSED_ACK            ASP_CLOSED            | ASP_ACK
#define ASP_SEND_DATA_PENDING     ASP_SEND_DATA         | ASP_PENDING
#define ASP_SEND_DATA_ACK_PENDING ASP_SEND_DATA_PENDING | ASP_ACK
#define ASP_DONE_ACK              ASP_SEND_DATA         | ASP_ACK       // Client acknowledgement when the server is done sending data 
#define IS_ACK(x)        ((x & ASP_ACK) == ASP_ACK)
#define SET_ACK(x)       (x | ASP_ACK)
#define CLEAR_ACK(x)     (x & !ASP_ACK)
#define IS_PENDING(x)    ((x & ASP_PENDING) == ASP_PENDING)
#define SET_PENDING(x)   (x | ASP_PENDING)
#define CLEAR_PENDING(x) (x & !ASP_PENDING)

typedef struct echo_pdu{
    asp_mtype_t mtype;
    uint8_t    mlen;
    char       msg[256];
}echo_pdu_t;

asp_mtype_t  advance_state_client(asp_mtype_t current_state);
asp_mtype_t  advance_state_server(asp_mtype_t current_state);
bool validate_next_server_client(asp_mtype_t current_state, asp_mtype_t proposed_next_state);
bool validate_next_server_state(asp_mtype_t current_state, asp_mtype_t proposed_next_state);
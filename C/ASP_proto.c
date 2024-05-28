#include <stdbool.h>
#include "echo_proto.h"

bool validate_next_client_state(asp_mtype_t current_state, asp_mtype_t proposed_next_state){
    asp_mtype_t allowed_next_state = advance_state_client(current_state);

    if ((allowed_next_state & proposed_next_state) != 0)
        return true;
    return false;
}
asp_mtype_t  advance_state_client(asp_mtype_t current_state){
    switch(current_state){
        case ASP_IDLE:
            return ASP_CONNECTED;        
        case ASP_CONNECTED:
            return ASP_ECHO;
        case ASP_ECHO:
            return ASP_ECHO_PENDING;
        case ASP_ECHO_PENDING:
            return ASP_ECHO_ACK_PENDING;
        case ASP_ECHO_ACK_PENDING:
            return ASP_ECHO_ACK;
        case ASP_ECHO_ACK:
            return ASP_ECHO | ASP_CLOSED;     
        case ASP_CLOSED:
            return ASP_CLOSED;   
        case ASP_ERROR:    
            return ASP_ERROR;
        default:
            return ASP_ERROR;     
    }
}

bool validate_next_server_state(asp_mtype_t current_state, asp_mtype_t proposed_next_state){
    asp_mtype_t allowed_next_state = advance_state_server(current_state);

    if ((allowed_next_state & proposed_next_state) != 0)
        return true;
    return false;
}
asp_mtype_t  advance_state_server(asp_mtype_t current_state){
    switch(current_state){
        case ASP_IDLE:    
        case ASP_CONNECTED:
            return ASP_SEND_DATA;
        case ASP_SEND_DATA:
            return ASP_SEND_DATA_PENDING;
        case ASP_SEND_DATA_PENDING:
            return ASP_SEND_DATA | ASP_DONE;  
        case ASP_CLOSED:
            return ASP_CLOSED;   
        case ASP_ERROR:    
            return ASP_ERROR;
        default:
            return ASP_ERROR;     
    }
}

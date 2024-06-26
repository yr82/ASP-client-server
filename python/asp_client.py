
import string
from typing import Dict
import json
from asp_quic import ASPQuicConnection, QuicStreamEvent
import pdu
import random


# Simulate chunks of data in a stream using strings of random length
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_random_string_array(chunk_len):
    return [generate_random_string(chunk_len) for _ in range(random.randint(20, 30))]

# chunk_size = random.randint(5, 10)
chunk_size = 5 # Streaming protocols usually have fixed chunk size 


async def asp_client_proto(scope:Dict, conn:ASPQuicConnection):
    
    # This is actually the servers logic (sending party)

    # Create an array of data that needs to be streamed 
    # data_stream = ["Hello", "this", "is", "a", "test", "stream"]
    data_stream = generate_random_string_array(chunk_size)
   
    # Initialize stream id 
    stream_id = None

    # Iterate through the data that needs to be streamed

    for i in range(len(data_stream)):

        print(f"[svr] sent message {i}:", data_stream[i])
        
        # Create a pdu for each the current message
        if i != (len(data_stream) - 1):
            dgram_out = pdu.Datagram(pdu.MSG_TYPE_DATA, data_stream[i], i, False)
        else:
            dgram_out = pdu.Datagram(pdu.MSG_TYPE_DATA, data_stream[i], i, True)

        # Convert the pdu into bytes to be streamed
        rsp_msg = dgram_out.to_bytes()

        if stream_id is None:
            # Open a new stream
            stream_id = conn.new_stream()
            rsp_event = QuicStreamEvent(stream_id, rsp_msg, False)
            await conn.send(rsp_event)
        else:
            # Use the existing stream
            rsp_event = QuicStreamEvent(stream_id, rsp_msg, False)
            await conn.send(rsp_event)

    print(f"[svr] is done sending all messages")

    # Wait for the final acknowledgment message from the client
    final_msg: QuicStreamEvent = await conn.receive()
    final_dgram_in = pdu.Datagram.from_bytes(final_msg.data)
    print("[svr] received final ack: ", final_dgram_in.msg)

    


        
         
         
                   
              



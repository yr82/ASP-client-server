
import string
from typing import Dict
import json
from asp_quic import ASPQuicConnection, QuicStreamEvent
import pdu
import random

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_random_string_array():
    return [generate_random_string(random.randint(5, 10)) for _ in range(random.randint(5, 10))]


async def asp_client_proto(scope:Dict, conn:ASPQuicConnection):
    
    # #START CLIENT HERE
    # print('[cli] starting client')


    # # Store the messages received in a buffer 
    # msgs_received = []

    # # Simulate the time in the client
    # for i in range(60):
    #     print('[cli] The current time at the client is: ', i)

    #     # Receive a message from the server
    #     message:QuicStreamEvent = await conn.receive()
    #     dgram_resp = pdu.Datagram.from_bytes(message.data)

    #      # If it is not the end of the stream
    #     if not dgram_resp.is_done:
    #         if dgram_resp.seq_num <= i:
    #             print(f'[cli] got message {dgram_resp.seq_num}:' , dgram_resp.msg)
    #     else:
    #         print(f'[cli] got message {dgram_resp.seq_num}:' , dgram_resp.msg)
    #         print("stream ended")

    #         # Send final ack to the server
    #         datagram = pdu.Datagram(pdu.MSG_TYPE_DATA_ACK, "Final client ack")
    #         new_stream_id = conn.new_stream()
    #         qs = QuicStreamEvent(new_stream_id, datagram.to_bytes(), False)
    #         await conn.send(qs)


    # #END CLIENT HERE

    # Create an array of data that needs to be streamed 
    # data_stream = ["Hello", "this", "is", "a", "test", "stream"]
    data_stream = generate_random_string_array()
   
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


        
         
         
                   
              



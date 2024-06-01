
from typing import Dict
import json
from asp_quic import ASPQuicConnection, QuicStreamEvent
import pdu


async def asp_client_proto(scope:Dict, conn:ASPQuicConnection):
    
    #START CLIENT HERE
    print('[cli] starting client')

    # datagram = pdu.Datagram(pdu.MSG_TYPE_DATA, "This is a test message")
    
    # new_stream_id = conn.new_stream()

    # qs = QuicStreamEvent(new_stream_id, datagram.to_bytes(), False)
    # await conn.send(qs)
    # message:QuicStreamEvent = await conn.receive()
    # dgram_resp = pdu.Datagram.from_bytes(message.data)
    # print('[cli] got message: ', dgram_resp.msg)
    # print('[cli] msg as json: ', dgram_resp.to_json())
    

    # Store the messages received in a buffer 
    msgs_received = []

    # Simulate the time in the client
    for i in range(60):
        print('[cli] The current time at the client is: ', i)

        # Receive a message from the server
        message:QuicStreamEvent = await conn.receive()
        dgram_resp = pdu.Datagram.from_bytes(message.data)

         # If it is not the end of the stream
        if not dgram_resp.is_done:
            if dgram_resp.seq_num <= i:
                print(f'[cli] got message {dgram_resp.seq_num}:' , dgram_resp.msg)
        else:
            print(f'[cli] got message {dgram_resp.seq_num}:' , dgram_resp.msg)
            print("stream ended")

            # Send final ack to the server
            datagram = pdu.Datagram(pdu.MSG_TYPE_DATA_ACK, "Final client ack")
            new_stream_id = conn.new_stream()
            qs = QuicStreamEvent(new_stream_id, datagram.to_bytes(), False)
            await conn.send(qs)


    #END CLIENT HERE


        
         
         
                   
              



import asyncio
from typing import Coroutine,Dict
import json
from asp_quic import ASPQuicConnection, QuicStreamEvent
import pdu
import random





async def asp_server_proto(scope:Dict, conn:ASPQuicConnection):
        
    # This is actually the logic for the client (receiving party)
    
    # #START CLIENT HERE
    print('[cli] starting client')


    # Store the messages received and streamed in a buffer 
    msgs_received = []
    msgs_streamed = []
    is_done = False

    # Initialize timer
    i = 0

    # Simulate the time in the client
    while True:
        print('[cli] The current time at the client is: ', i)

        # Check if it is time to stream the last message from the buffer yet
        for msg in msgs_received:
            if(msgs_streamed != []) and (msgs_streamed[-1].end < i) and (msg.start >= i):
                    # Stream the first message from the buffer that fits the current time stamp
                    print(f'[cli] got message {msg.seq_num}:' , msg.msg)
                    msgs_streamed.append(msg)
                    msgs_received.remove(msg)
                    break
            elif msg.start < i:
                    # Its too late to stream this message, we need to drop it
                    msgs_received.remove(msg)
        

        # If we are still expecting messages
        if not is_done:
            # Receive a message from the server
            message:QuicStreamEvent = await conn.receive()
            
            dgram_resp = pdu.Datagram.from_bytes(message.data)

            # If it is not the end of the stream
            if not dgram_resp.is_done:
                if msgs_streamed == []:
                    # We are streaming the first message
                    print(f'[cli] got message {dgram_resp.seq_num}:' , dgram_resp.msg)
                    msgs_streamed.append(dgram_resp)
                    
                else:
                    # We are running behind - do not do anything and add to the buffer
                    msgs_received.append(dgram_resp)
                    
                    
            else:
                # We have received all messages
                is_done = True
                msgs_received.append(dgram_resp)


        # We are done and have no more messages left to stream

        if (msgs_received == []) and is_done:
                
            print("Stream Ended")

            # Send final ack to the server
            datagram = pdu.Datagram(pdu.MSG_TYPE_DATA_ACK, "Final client ack")
            #new_stream_id = conn.new_stream()
            # Use the same stream id 
            qs = QuicStreamEvent(message.stream_id, datagram.to_bytes(), False)
            await conn.send(qs)

            # Close the stream
            conn.close()

            # Exit while loop
            break

        # Increment time
        i += 1



    #END CLIENT HERE









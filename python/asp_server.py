import asyncio
from typing import Coroutine,Dict
import json
from asp_quic import ASPQuicConnection, QuicStreamEvent
import pdu
import random





async def asp_server_proto(scope:Dict, conn:ASPQuicConnection):
        
        # message:QuicStreamEvent = await conn.receive()
        
        # dgram_in = pdu.Datagram.from_bytes(message.data)
        # print("[svr] received message: ", dgram_in.msg)
        
        # stream_id = message.stream_id
        
        # dgram_out = dgram_in
        # dgram_out.mtype |= pdu.MSG_TYPE_DATA_ACK
        # dgram_out.msg = "SVR-ACK: " + dgram_out.msg
        # rsp_msg = dgram_out.to_bytes()
        # rsp_vent = QuicStreamEvent(stream_id, rsp_msg, False)
        # await conn.send(rsp_vent)

        # Create an array of data that needs to be streamed 
        data_stream = ["Hello", "this", "is", "a", "test", "stream"]

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
                rsp_event = await conn.new_stream(rsp_msg)
                stream_id = rsp_event.stream_id
            else:
                # Use the existing stream
                rsp_event = QuicStreamEvent(stream_id, rsp_msg, False)
                await conn.send(rsp_event)

        print(f"[svr] is done sending all messages")

        # Wait for the final acknowledgment message from the client
        final_msg: QuicStreamEvent = await conn.receive()
        final_dgram_in = pdu.Datagram.from_bytes(final_msg.data)
        print("[svr] received final ack: ", final_dgram_in.msg)









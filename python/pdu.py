
import json

MSG_TYPE_DATA = 0x00
MSG_TYPE_ACK  = 0x01
MSG_TYPE_DATA_ACK = MSG_TYPE_DATA | MSG_TYPE_ACK

class Datagram:
    def __init__(self, mtype: int, msg: str, seq_num: int = 0, is_done: bool = False, sz:int = 0, start:int = 0, end:int = 0):
        self.mtype = mtype
        self.msg = msg
        self.sz = len(self.msg)
        self.seq_num = seq_num
        self.is_done = is_done
        self.start = self.seq_num * self.sz
        self.end = self.start + (self.sz - 1)
        
    def to_json(self):
        return json.dumps(self.__dict__)    
    
    @staticmethod
    def from_json(json_str):
        return Datagram(**json.loads(json_str))
    
    def to_bytes(self):
        return json.dumps(self.__dict__).encode('utf-8')
    
    @staticmethod
    def from_bytes(json_bytes): 
        return Datagram(**json.loads(json_bytes.decode('utf-8')))    
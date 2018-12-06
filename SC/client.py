import socket
import struct
import logging
import Common
import platform
from ClientSide import ClientSide
LOG = logging.getLogger('Client')
LOG.setLevel(logging.DEBUG)
_log = logging.StreamHandler()
_log.setLevel(logging.DEBUG)
_log.setFormatter(logging.Formatter("<%(name)s>[@%(lineno)3d]%(levelname)8s->%(message)s"))
LOG.addHandler(_log)


class Client(Common.SendRecv):
    def __init__(self,HOST:str,PORT:int):
        self.ADDRESS = (HOST,PORT)
        self.con = socket.socket()
        self._connect()

    def buildClientInfo(self):
        return {
            'Version': '0.0.1a',
            'Name': 'Client',
            'Author': 'Jerry',
            "Platform":{
                "System":platform.platform(),
                "Bit":platform.architecture()
            }
        }

    def handle(self):
        self.startConnection()
        self.send(Common.DataBuilder.disconnect())

    def startConnection(self):
        self.send(Common.DataBuilder.connect())
        DFlag, DType, Data = self.recv()
        if DFlag == Common.DCode.Flag.CONNECT:
            self.send(Common.DataBuilder.hello({'NAME':"Jerry","MSG":"Hello From Client","INFO":self.buildClientInfo()}))
            DFlag, DType, Data = self.recv()
            if DFlag == Common.DCode.Flag.HELLO:
                if DType == Common.DCode.DType.JSON:
                    LOG.info("GET Sess ID is<|%s" % (Data['SESS']))
                    LOG.info("GET Message is<|%s" % (Data['MSG']))
                    LOG.info("Server Info is<|%s" % (Data['INFO']))
                    _cs = ClientSide(self.con,Data['SESS'])
                    _cs.handle()
        self.send(Common.DataBuilder.disconnect())

    def _connect(self):
        try:
            self.con.connect(self.ADDRESS)
            LOG.info("Connected |> {0}:{1}".format(*self.ADDRESS))
        except ConnectionRefusedError:
            LOG.error("Connect Refused from {0}:{1}".format(*self.ADDRESS))
            return None

    def _close(self):
        if (self.con != None):
            self.con.shutdown(2)
            self.con.close()
            LOG.info("Disonnect from {0}:{1}".format(*self.ADDRESS))
            self.con = None
        else:
            LOG.warning("Already Closed")
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        LOG.debug("Exiting")
        if (self.con != None):
            self.con.shutdown(2)
            self.con.close()
            self.con = None
        else:
            pass

    def __del__(self):
        LOG.info("Exiting")

if __name__ == "__main__":
    C = Client('127.0.0.1',9999)
    C.handle()


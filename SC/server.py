import socketserver
import struct
import logging
import Common
import platform
from ServerSide import ServerSide

LOG = logging.getLogger('Server')
LOG.setLevel(logging.DEBUG)
_log = logging.StreamHandler()
_log.setLevel(logging.INFO)
_log.setFormatter(logging.Formatter("<%(name)s>[@%(lineno)3d]%(levelname)8s->%(message)s"))
LOG.addHandler(_log)

class ServerHandler(socketserver.BaseRequestHandler,Common.SendRecv):

    def buildServerInfo(self):
        return {
            'Version':'0.0.1a',
            'Name': "Server",
            'Author': 'Jerry',
            "Platform": {
                "System": platform.platform(),
                "Bit": platform.architecture()
            }
        }

    def createSessId(self):
        return 1

    def handle(self):
        self.con = self.request
        LOG.info("Connected <| {0}:{1}".format(*self.client_address))
        while True:
            DFlag,DType,Data=self.recv()
            if DFlag == Common.DCode.Flag.DISCONNECT or DFlag == None:
                self.send(Common.DataBuilder.disconnect())
                break
            elif DFlag == Common.DCode.Flag.CONNECT:
                self.startConnection()
            else:
                self.send(Common.DataBuilder.disconnect())

    def startConnection(self):
        self.send(Common.DataBuilder.connect())
        DFlag, DType, Data = self.recv()
        if DFlag == Common.DCode.Flag.HELLO:
            LOG.info("Client Name is<|%s" % (Data['NAME']))
            LOG.info("GET Message is<|%s" % (Data['MSG']))
            LOG.info("Client INFO is<|%s" % (Data['INFO']))
            SESSID = self.createSessId()
            self.send(Common.DataBuilder.hello({'SESS': SESSID, "MSG": "HELLO FROM SERVER", "INFO": self.buildServerInfo()}))
            _ss = ServerSide(self.con,SESSID)
            _ss.handle()
        self.send(Common.DataBuilder.disconnect())

    def finish(self):
        LOG.info("Disconnected With {0}:{1}".format(*self.client_address))
        pass

if __name__ == "__main__":
    Address = ('0.0.0.0',9999)
    server = socketserver.ThreadingTCPServer(Address, ServerHandler)
    LOG.info("Listening {0}:{1}".format(*Address))
    server.serve_forever()
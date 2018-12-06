import logging
import Common

LOG = logging.getLogger('CltSde')
LOG.setLevel(logging.DEBUG)
_log = logging.StreamHandler()
_log.setLevel(logging.INFO)
_log.setFormatter(logging.Formatter("<%(name)s>[@%(lineno)3d]%(levelname)8s->%(message)s"))
LOG.addHandler(_log)



class ClientSide(Common.SendRecv):
    def __init__(self,con,SESSID):
        self.con = con
        self.SESSID = SESSID
    @staticmethod
    def buildModuleInfo():
        return {
            'Name':"Client Base Handler",
            'Version':"0.0.1a",
            "Author": "Jerry"
        }
    def handle(self):
        self.send(Common.DataBuilder.build(Common.DCode.Flag.REPORT,{"Module":self.buildModuleInfo()}))
        DFlag, DType, Data = self.recv()
        if DFlag == Common.DCode.Flag.REPORT:
            LOG.info("Connection Estabished")
            return True

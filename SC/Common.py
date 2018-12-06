import struct
import json
import logging

LOG = logging.getLogger('Common')
LOG.setLevel(logging.DEBUG)
_log = logging.StreamHandler()
_log.setLevel(logging.DEBUG)
_log.setFormatter(logging.Formatter("<%(name)s>[@%(lineno)3d]%(levelname)8s->%(message)s"))
LOG.addHandler(_log)


class SendRecv:
    con = None

    def send(self,data:bytes):
        """
        发送方法
        :param: data: :`bytes`: will be send
        :return: :class:`bool` Send Status
        """
        if(self.con == None):
            LOG.warning("Connected Before Send")
        if(type(data)!=bytes):
            LOG.warning("Send Unsupport Type : {}, Should Be Bytes".format(type(data)))
        length = len(data)
        head = struct.pack('i',length)
        LOG.debug("Send Head |>%s" % head)
        LOG.info("Send Bytes|>{:10d} B".format(length))
        try:
            self.con.send(head)
            self.con.send(data)
            return True
        except ConnectionAbortedError:
            LOG.error("Connection Aborted")
            return None
        except ConnectionResetError:
            LOG.error("Connection Reseted")
            return None

    def recv(self):
        """
        接收方法
        :return: :class:`tuple` DFlag,DType,Data
        """
        if(self.con == None):
            LOG.warning("Connected Before Recv")
        try:
            head = self.con.recv(4)
            LOG.debug("Recv Head <|%s"%head)
            length = struct.unpack("i", head)[0]
        except ConnectionResetError:
            LOG.error("Connection Reseted")
            return None, None, None
        except struct.error:
            LOG.error("Head Data Not Valid <|%s"%head)
            return None, None, None
        LOG.info("Recv Bytes<|{:10d} B".format(length))
        return DataParser(self.con.recv(length))


class DCode:
    # Status
    class Status:
        IDLE = b"\xA0"
        BUSY = b"\xA1"

    # Flag
    class Flag:
        QUERY = b"\x00"
        REPORT = b"\x09"
        ERROR = b"\x0A"
        RETRY = b"\x0B"
        CONNECT = b"\x0C"
        HELLO = b"\x0D"
        DISCONNECT = b"\x0E"
        RAW = b"\x0F"
        UNSUPPORTED = b"\x0F"

    FlagString = {
        b"\x00": 'QUERY',
        b"\x09": 'REPORT',
        b"\x0A": 'ERROR',
        b"\x0B": 'RETRY',
        b"\x0C": 'CONNECT',
        b"\x0D": 'HELLO',
        b"\x0E": 'DISCONNECT',
        b"\x0F": 'RAW/UnSupported'
    }

    # DType
    class DType:
        NONE = b"\xD0"
        STRING = b"\xD1"
        NUMBER = b"\xD2"
        FILE = b"\xDA"
        BYTES = b"\xDB"
        JSON = b"\xDD"
        RAW = b"\xDF"
        UNSUPPORTED = b"\xDF"

    DTypeString = {
        b"\xD0": 'None',
        b"\xD1": 'String',
        b"\xD2": 'Number',
        b"\xDA": 'File',
        b"\xDB": 'Bytes/Raw',
        b"\xDD": 'Json/Array',
        b"\xDF": 'Raw/UnSupported'
    }

class DataBuilder:
    @staticmethod
    def build(Flag:bytes, data:any):
        LOG.debug("Build Flag is |>%s" % (DCode.FlagString[Flag]))
        LOG.debug("Build Data is |>%s" % data)
        if(type(data) in (str,)):
            if data == "":
                dtype = DCode.DType.NONE
                data = b''
            else:
                dtype = DCode.DType.STRING
                data = data.encode(encoding='utf-8')
        elif(type(data) in (int, float)):
            dtype = DCode.DType.NUMBER
            data = struct.pack('d',data)
        elif(type(data) in (tuple, dict, list)):
            dtype = DCode.DType.JSON
            data = json.dumps(data).encode(encoding='utf-8')
        elif(type(data) in (bytes,)):
            if data == b"":
                dtype = DCode.DType.NONE
            else:
                dtype = DCode.DType.BYTES
        else:
            dtype = DCode.DType.NONE
            data = b""
        LOG.debug("Build Type is |>%s" % (DCode.DTypeString[dtype]))
        return Flag + dtype + data

    @staticmethod
    def hello(msg: any = None):
        return DataBuilder.build(DCode.Flag.HELLO, msg)

    @staticmethod
    def connect(msg: any = None):
        return DataBuilder.build(DCode.Flag.CONNECT, msg)

    @staticmethod
    def disconnect(msg: any = None):
        return DataBuilder.build(DCode.Flag.DISCONNECT, msg)

def DataParser(raw:bytes):
    Flag = raw[0:1]
    LOG.debug("Parse Flag is <|%s"%(DCode.FlagString[Flag]))
    DType = raw[1:2]
    LOG.debug('Parse Type is <|%s'%(DCode.DTypeString[DType]))
    if DType == DCode.DType.NONE:
        Data = None
    elif DType == DCode.DType.STRING:
        Data = raw[2:].decode(encoding='utf-8')
    elif DType == DCode.DType.JSON:
        _d = raw[2:].decode(encoding='utf-8')
        try:
            Data = json.loads(_d)
        except json.decoder.JSONDecodeError:
            DType = DCode.DType.UNSUPPORTED
            Data = None
            LOG.error('Parse JSON Data ERROR %s'%_d)
    elif DType == DCode.DType.NUMBER:
        Data = struct.unpack('d',raw[2:10])[0]
    else:
        LOG.warning('UnSupport Data %s'%raw)
        DType = DCode.DType.UNSUPPORTED
        Data = raw[2:]
    LOG.debug("Parse Data is <|%s"%Data)
    return Flag, DType, Data
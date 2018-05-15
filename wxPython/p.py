import wx
import base64
import re
from urllib.parse import unquote

class Parser:
    def __init__(self, Link):
        self.Link=Link
        self.detect()
        self.server=""
        self.port=""
        self.password=""
        self.method=""
        self.protocol=""
        self.obfs=""
        self.param={}
    def detect(self):
        if self.Link.startswith("ssr://"):
            self.type="SSR"
        elif self.Link.startswith("ss://"):
            self.type="SS"
        else:
            self.type=None
    def parse(self):
        if self.type=="SSR":
            return self.ssr_parse()
        elif self.type=="SS":
            return self.ss_parse()
        else:
            return False
    def ssr_parse(self):
        _link = self.Link.split("://",2)
        link = _link[1]
        link=link+"="*(len(link)%4)
        _part= base64.urlsafe_b64decode(link)
        _part= bytes.decode(_part)
        parts= _part.split("/?")
        server_part = parts[0].split(":",6)
        self.server=server_part[0]
        self.port=server_part[1]
        self.protocol=server_part[2]
        self.method=server_part[3]
        self.obfs=server_part[4]
        _password=server_part[5]
        _password=_password+"="*(len(_password)%4)
        self.password=bytes.decode(base64.b64decode(_password))
        param_part = re.findall("(.+?)=(.*?)&",parts[1])
        for _k,_v in param_part:
            if _v=="":
                continue
            _v=_v+"="*(len(_v)%4)
            _v=bytes.decode(base64.b64decode(_v))
            self.param[_k]=_v
    def ss_parse(self):
        _link = self.Link.split("://",2)
        _l    = _link[1]
        _p    = _l.split("#",2)
        if len(_p) > 1:
            self.param['remarks']=unquote(_p[1])
        else:
            self.param['remarks']=''
        link  = _p[0]
        _part=link.split("@",2)
        if len(_part)>1:
            server_part=_part[1].split(":",2)
            self.server=server_part[0]
            self.port=server_part[1]
            _ppart=_part[0]
            _ppart=_ppart+"="*(len(_ppart)%4)
            _ppart= bytes.decode(base64.urlsafe_b64decode(_ppart))
            param_part = _ppart.split(":")
            self.method=param_part[0]
            self.password=param_part[1]
        elif len(_part)==1:
            _spart=_part[0]
            _spart=_spart+"="*(len(_spart)%4)
            _spart= bytes.decode(base64.urlsafe_b64decode(_spart))
            _part = _spart.split("@")
            param_part=_part[0].split(":")
            self.method=param_part[0]
            self.password=param_part[1]
            server_part=_part[1].split(":")
            self.server=server_part[0]
            self.port=server_part[1]

class Pj(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"SS/SSR链接解析", pos = wx.DefaultPosition, size = wx.Size( 512,384 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self._ = wx.StaticText( self, wx.ID_ANY, u"SS/SSR链接", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer1.Add( self._, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.Link = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 350,-1 ), wx.TE_PROCESS_ENTER|wx.TE_RICH2 )
        gbSizer1.Add( self.Link, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.Parse = wx.Button( self, wx.ID_ANY, u"解析", wx.DefaultPosition, wx.Size( 45,-1 ), 0 )
        gbSizer1.Add( self.Parse, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"SS/SSR链接信息" ), wx.VERTICAL )
        fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self._Server = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"服务器", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._Server, 0, wx.ALL, 5 )
        self.Server = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.Server, 0, wx.ALL, 5 )
        self._Port = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"端口", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._Port, 0, wx.ALL, 5 )
        self.Port = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.Port, 0, wx.ALL, 5 )
        self._Password = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"密码", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._Password, 0, wx.ALL, 5 )
        self.Password = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.Password, 0, wx.ALL, 5 )
        self._Method = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"加密方法", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._Method, 0, wx.ALL, 5 )
        self.Method = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.Method, 0, wx.ALL, 5 )
        self._Protocol = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"协议", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._Protocol, 0, wx.ALL, 5 )
        self.Protocol = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.Protocol, 0, wx.ALL, 5 )
        self._ProtoParam = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"协议参数", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._ProtoParam, 0, wx.ALL, 5 )
        self.ProtoParam = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.ProtoParam, 0, wx.ALL, 5 )
        self._Obfs = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"混淆", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._Obfs, 0, wx.ALL, 5 )
        self.Obfs = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.Obfs, 0, wx.ALL, 5 )
        self._ObfsParam = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"混淆参数", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._ObfsParam, 0, wx.ALL, 5 )
        self.ObfsParam = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.ObfsParam, 0, wx.ALL, 5 )
        self._Group = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"节点组", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._Group, 0, wx.ALL, 5 )
        self.Group = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.Group, 0, wx.ALL, 5 )
        self._Nick = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"节点名称", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        fgSizer3.Add( self._Nick, 0, wx.ALL, 5 )
        self.Nick = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), wx.NO_BORDER|wx.TE_READONLY )
        fgSizer3.Add( self.Nick, 0, wx.ALL, 5 )
        sbSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
        gbSizer1.Add( sbSizer1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )
        self.SetSizer( gbSizer1 )
        self.Layout()
        self.Centre( wx.BOTH )
        self.InitUI()
    def InitUI(self):
        self.Parse.Bind(wx.EVT_BUTTON,self.OnButtonClicked)
        self.Link.Bind(wx.EVT_TEXT_ENTER,self.OnButtonClicked)
        self.Link.Bind(wx.EVT_TEXT,self.clearColor)
        self.Show(True)
    def clearColor(self,e):
        self.Link.SetBackgroundColour(wx.Colour(255,255,255))
    def OnButtonClicked(self,e):
        link = self.Link.GetLineText(0).strip()
        if link=="":
            self.Link.SetOwnBackgroundColour(wx.Colour( 255, 0, 0 ))
        p = Parser(link)
        try:
            p.parse()
        except:
            self.Link.SetOwnBackgroundColour(wx.Colour( 255, 0, 0 ))
        if p.type != None:
            self.Server.SetLabelText(p.server)
            self.Port.SetLabelText(p.port)
            self.Method.SetLabelText(p.method)
            self.Password.SetLabelText(p.password)
            self.Protocol.SetLabelText(p.protocol)
            self.Obfs.SetLabelText(p.obfs)
            self.Server.SetLabelText(p.server)
            if "remarks" in p.param:
                self.Nick.SetLabelText(p.param["remarks"])
            else:
                self.Nick.SetLabelText("")
            if "obfsparam" in p.param:
                self.ObfsParam.SetLabelText(p.param["obfsparam"])
            else:
                self.ObfsParam.SetLabelText("")
            if "protoparam" in p.param:
                self.ProtoParam.SetLabelText(p.param["protoparam"])
            else:
                self.ProtoParam.SetLabelText("")
            if "group" in p.param:
                self.Group.SetLabelText(p.param["group"])
            else:
                self.Group.SetLabelText("")
        else:
            self.Link.SetOwnBackgroundColour(wx.Colour( 255, 0, 0 ))
a=wx.App()
Pj(None)
a.MainLoop()

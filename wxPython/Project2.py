# -*- coding: utf-8 -*- 

import wx
import wx.xrc
import wx.grid
import os
import xlrd
import xlwt

class SpecialDlg ( wx.Dialog ):
    def __init__( self, parent , option):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 250,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        gbSizer3 = wx.GridBagSizer( 0, 0 )
        gbSizer3.SetFlexibleDirection( wx.BOTH )
        gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self._staticText4 = wx.StaticText( self, wx.ID_ANY, u"请设置必要参数", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._staticText4.Wrap( -1 )
        self._staticText4.SetFont( wx.Font( 12, 70, 90, 90, False, "宋体" ) )
        gbSizer3.Add( self._staticText4, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self._Confirm = wx.Button( self, wx.ID_ANY, u"确认", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer3.Add( self._Confirm, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self.options = []
        for i in option:
            self.options.append(wx.CheckBox( self, wx.ID_ANY, i, wx.DefaultPosition, wx.DefaultSize, 0 ))
        y=1
        for _o in self.options:
            gbSizer3.Add( _o, wx.GBPosition( y, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
            y+=1
        self.SetSizer( gbSizer3 )
        self.Layout()
        self.Centre( wx.BOTH )
        self.InitUI()
    def InitUI(self):
        self.Bind(wx.EVT_CHECKBOX,self.onChecked)
        self.Show(True)
    def onChecked(self,event):
        cb = event.GetEventObject()
        print ([cb.GetLabel()],' is clicked',cb.GetValue())
    def __del__( self ):
        pass
    


class Status:
    def __init__(self,Label,Start,Progress,Error):
        self.L = Label
        self.S = Start
        self.P = Progress
        self.E = Error
    def Warning(self,Text):
        self.L.SetLabelText(Text)
        self.L.SetBackgroundColour(wx.YELLOW)
        self.E.Append(Text)
    def Error(self,Text):
        self.L.SetLabelText(Text)
        self.L.SetBackgroundColour(wx.RED)
        self.E.Append(Text)
    def Info(self,Text):
        self.L.SetLabelText(Text)
        self.L.SetBackgroundColour(wx.WHITE)
    def SetProgress(self,now,total):
        self.P.SetValue(now)
        self.P.SetRange(total)

class XLS:
    """自定义xls的一些方法"""
    def __init__(self, file_name):
        file_name = str(file_name)
        self.book = xlwt.Workbook(encoding='utf-8')
        self.sheet = None
        while os.path.isfile(file_name+'.xls'):
            file_name+='_1'
        self.fn=file_name+'.xls'
    def init_sheet(self,sheet_name):
        self.sheet = self.book.add_sheet(sheet_name,cell_overwrite_ok=True)
        notify=["习题内容","习题类型","习题答案","备注","选项1","选项2","选项3","选项4","选项5","选项6"]
        for i in range(len(notify)):
            self.sheet.write(0,i,notify[i])
        self.save()
    def write_xls(self,title,typ,options,daan,beizu=None):
        if self.sheet==None:
            self.init_sheet("临时表")
        _r = len(self.sheet.rows)
        self.sheet.write(_r,0,title)
        self.sheet.write(_r,1,typ)
        _ans = ''
        if beizu!=None:
            self.sheet.write(beizu,_r,3)
        for _i in daan:
            _ans+=_i.replace("A","1").replace("B","2").replace("C","3").replace("D","4").replace("E","5").replace("F","6")
            _ans+=','
        self.sheet.write(_r,2,_ans[:-1])
        _x = 4
        for _o in options:
            self.sheet.write(_r,_x,_o)
            _x+=1
    def save(self):
        self.book.save(self.fn)

def Read_Accounts(fn):
    if os.path.isfile(fn):
        try:
            data = xlrd.open_workbook(fn)
            table = data.sheets()[0]
            accounts=[]
            row = 1
            while(row<table.nrows):
                u=table.row_values(row)[0]
                if type(u)==float:
                    u=str(int(u))
                p=table.row_values(row)[1]
                if type(p)==float:
                    p=str(int(p))
                accounts.append({"u":u,"p":p})
                row += 1
        except:
            return False
        else:
            return accounts

class GridData(wx.grid.GridTableBase):
    _cols = ['账号','密码']
    _data = []
    _highlighted = set()

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetValue(self, row, col, val):
        self._data[row][col] = val

    def AppendValue(self, vals):
        self._data.append(vals)

    def GetAttr(self, row, col, kind):
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(wx.GREEN if row in self._highlighted else wx.WHITE)
        return attr

    def set_value(self, row, col, val):
        self._highlighted.add(row)
        self.SetValue(row, col, val)

class Frame ( wx.Frame ):
    
    DownloadModel = None

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u'爬虫  --By Jerryyan', pos = wx.DefaultPosition, size = wx.Size( 600,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        gSizerM = wx.GridSizer( 1, 2, 0, 0 )
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self._OpenFile = wx.StaticText( self, wx.ID_ANY, u"打开文件", wx.DefaultPosition, wx.Size( 140,40 ), 0 )
        self._OpenFile.Wrap( -1 )
        self._OpenFile.SetFont( wx.Font( 11, 70, 90, 90, False, "宋体" ) )
        gbSizer1.Add( self._OpenFile, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.OpenFile = wx.Button( self, wx.ID_ANY, u"...浏览", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer1.Add( self.OpenFile, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 220,220 ), 0 )
        # Grid
        self.data = GridData()
        self.m_grid1.SetTable( self.data )
        # Columns
        self.m_grid1.SetColLabelSize( 20 )
        # Rows
        self.m_grid1.SetRowLabelSize( 20 )
        # Cell Defaults
        self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        gbSizer1.Add( self.m_grid1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
        gSizerM.Add( gbSizer1, 1, wx.EXPAND, 5 )
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self._Model = wx.StaticText( self, wx.ID_ANY, u"加载模块", wx.DefaultPosition, wx.Size( 140,40 ), 0 )
        self._Model.Wrap( -1 )
        self._Model.SetFont( wx.Font( 12, 70, 90, 90, False, "宋体" ) )
        gbSizer2.Add( self._Model, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.Model = wx.Button( self, wx.ID_ANY, u"..浏览", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer2.Add( self.Model, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.Start = wx.Button( self, wx.ID_ANY, u"开始", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Start.Enable( False )
        gbSizer2.Add( self.Start, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.Progress = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 280,-1 ), wx.GA_HORIZONTAL )
        self.Progress.SetValue( 0 ) 
        gbSizer2.Add( self.Progress, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
        self.StatusText = wx.StaticText( self, wx.ID_ANY, u"就绪", wx.DefaultPosition, wx.Size( 280,-1 ), 0 )
        self.StatusText.Wrap( -1 )
        gbSizer2.Add( self.StatusText, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
        gSizerM.Add( gbSizer2, 1, wx.EXPAND, 5 )
        _ErrorChoices = []
        self._Error = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 280,-1 ), _ErrorChoices, 0 )
        gbSizer2.Add( self._Error, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
        self.SetSizer( gSizerM )
        self.Layout()
        self.Centre( wx.BOTH )
        self.InitUI()

    def InitUI(self):
        self.STATUS = Status(self.StatusText,self.Start,self.Progress,self._Error)
        self.Model.Bind(wx.EVT_BUTTON,self.LoadModule)
        self.OpenFile.Bind(wx.EVT_BUTTON,self.LoadAccount)
        self.Start.Bind(wx.EVT_BUTTON,self.StartJob)
        self.Show(True)

    def LoadAccount(self,event):
        dlg = wx.FileDialog(self, "打开账号密码文件...",os.getcwd(),wildcard = "Excel files(*.xlsx)|*.xlsx|Excel 2003 files(*.xls)|*.xls|All files(*.*)|*.*" )
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
        dlg.Destroy()
        d = Read_Accounts(filename)
        if d:
            for _d in d:
                self.data.AppendValue([_d['u'],_d['p']])
        else:
            self._Error.Append("错误：加载%s文件失败"%(filename))
        self.m_grid1.SetTable( self.data )
        self.m_grid1.ForceRefresh()

    def LoadModule(self,event):
        dlg = wx.FileDialog(self, "打开模块文件...",os.getcwd(),wildcard = "Python Model files(*.py)|*.py|All files(*.*)|*.*" )
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]: #如果没有文件名后缀
                filename = filename + '.py'
            try:
                _Model = __import__(os.path.relpath(filename)[:-3])
                self.DownloadModel = _Model.Model(self.STATUS,XLS)
                self._Model.SetLabelText(self.DownloadModel.Name)
                self.Start.Enable()
            except:
                self._Error.Append("错误：加载%s模块失败"%(filename))
        dlg.Destroy()
    
    def StartJob(self,event):
        for i in self.data._data:
            a,b = self.DownloadModel.login(i[0],i[1])
            if a:
                self.DownloadModel.start(b)
                self._Error.Append("%s：成功"%(i[0]))
            else:
                self.STATUS.Error("%s登陆失败：%s"%s(i[0],b))
    def __del__( self ):
        pass
    
# print(Read_Accounts("1.xlsx"))
a=wx.App()
Frame(None)
# SpecialDlg(None,['1\t2','2\t2','3\t3'])
a.MainLoop()
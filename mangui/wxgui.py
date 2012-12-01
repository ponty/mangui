from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import parser
import subprocess
import sys
import wx
from entrypoint2 import entrypoint


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)


class Repository(wx.Frame):
    def __init__(self, parent, id, title, mandoc):
        self.command = mandoc['command']
        wx.Frame.__init__(self, parent, id, title, size=(600, 400))

        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)

        self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
        self.list = CheckListCtrl(rightPanel)
        self.list.InsertColumn(0, 'flag', width=140)
        self.list.InsertColumn(1, 'short flag')
        self.list.InsertColumn(2, 'help')

        for i in mandoc['options']:
            flags = i[0]
            flags.sort(key=len, reverse=True)
            index = self.list.InsertStringItem(sys.maxint, flags[0])
            self.list.SetStringItem(index, 1, flags[1] if len(flags) > 1 else '')
            self.list.SetStringItem(index, 2, i[1])

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        sel = wx.Button(leftPanel, -1, 'Select All', size=(100, -1))
        des = wx.Button(leftPanel, -1, 'Deselect All', size=(100, -1))
        apply = wx.Button(leftPanel, -1, 'Run', size=(100, -1))
        self.cb_close = wx.CheckBox(leftPanel, -1, 'Close', size=(100, -1))
        self.cb_close.SetToolTip(wx.ToolTip("close GUI after running the command"))
        self.cb_term = wx.CheckBox(leftPanel, -1, 'new terminal', size=(100, -1))
        self.cb_term.SetToolTip(wx.ToolTip("run command in new terminal"))
        bt_exit = wx.Button(leftPanel, -1, 'Exit', size=(100, -1))

        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=sel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=des.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnApply, id=apply.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnExit, id=bt_exit.GetId())

        vbox2.Add(sel, 0, wx.TOP, 5)
        vbox2.Add(des)
        vbox2.Add(apply)
        vbox2.Add(self.cb_close)
        vbox2.Add(self.cb_term)
        vbox2.Add(bt_exit)

        leftPanel.SetSizer(vbox2)

        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add((-1, 10))
        vbox.Add(self.log, 0.5, wx.EXPAND)
        vbox.Add((-1, 10))

        rightPanel.SetSizer(vbox)

        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

        self.list.OnCheckItem = self.OnCheckItem

        cmd = self.cmd()
        self.log.SetValue(cmd)

    def OnSelectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i)

    def OnDeselectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i, False)

    def OnApply(self, event):
#        print os.getcwd()
        cmd = self.log.GetValue()
        term = 'xterm'
        if self.cb_term.IsChecked():
            cmd = '%s -hold -e "%s"' % (term, cmd)
#        os.system( cmd )
        subprocess.Popen(cmd, shell=1)
        if self.cb_close.IsChecked():
            exit(0)

    def OnExit(self, event):
        exit(0)

    def cmd(self):
        count = self.list.GetItemCount()
        cmd = self.command + ' '
        for row in range(count):
            item = self.list.GetItem(itemId=row, col=0)
            if self.list.IsChecked(row):
                cmd += item.GetText() + ' '
        return cmd

    def OnCheckItem(self, index, flag):
        cmd = self.cmd()
        self.log.SetValue(cmd)


@entrypoint
def main(command):
    mandoc = parser.command_info(command)

    app = wx.App()
    Repository(None, -1, 'mangui', mandoc)
    app.MainLoop()


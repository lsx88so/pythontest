#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import wx
from appgui import mainFrame

# 创建 mainWin 类并传入 my_win.MyFrame1
class mainWin(mainFrame):
   # 实现 Button 控件的响应函数 showMessage
   def showMessage(self, event):
       pass
if __name__ == '__main__':
    # 下面是使用 wxPython 的固定用法
    app = wx.App()
    main_win = mainWin(None)
    main_win.Show()
    app.MainLoop()
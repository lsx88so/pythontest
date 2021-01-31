# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jan 15 2021)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import wx.richtext

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"UniversalTools", pos = wx.DefaultPosition, size = wx.Size( 1280,800 ), style = wx.CLOSE_BOX|wx.MINIMIZE|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        mainbSizer = wx.BoxSizer( wx.VERTICAL )

        self.main_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.xdr_panel = wx.Panel( self.main_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        xdr_fgSizer_a = wx.FlexGridSizer( 3, 1, 0, 0 )
        xdr_fgSizer_a.AddGrowableCol( 0 )
        xdr_fgSizer_a.AddGrowableRow( 2 )
        xdr_fgSizer_a.SetFlexibleDirection( wx.BOTH )
        xdr_fgSizer_a.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.xdr_textCtrl_input = wx.TextCtrl( self.xdr_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,200 ), wx.HSCROLL|wx.TE_DONTWRAP|wx.TE_MULTILINE )
        xdr_fgSizer_a.Add( self.xdr_textCtrl_input, 0, wx.EXPAND, 5 )

        xdr_fgSizer_a1 = wx.FlexGridSizer( 1, 0, 0, 0 )
        xdr_fgSizer_a1.AddGrowableCol( 6 )
        xdr_fgSizer_a1.SetFlexibleDirection( wx.BOTH )
        xdr_fgSizer_a1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.xdr_staticText_1 = wx.StaticText( self.xdr_panel, wx.ID_ANY, u"话单类型：", wx.DefaultPosition, wx.Size( 70,-1 ), 0 )
        self.xdr_staticText_1.Wrap( -1 )

        xdr_fgSizer_a1.Add( self.xdr_staticText_1, 0, wx.ALIGN_CENTER, 5 )

        xdr_comboBox_xdrtypeChoices = []
        self.xdr_comboBox_xdrtype = wx.ComboBox( self.xdr_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, xdr_comboBox_xdrtypeChoices, wx.CB_READONLY|wx.CB_SORT )
        xdr_fgSizer_a1.Add( self.xdr_comboBox_xdrtype, 0, wx.ALIGN_CENTER, 5 )

        self.xdr_checkBox_autodetect = wx.CheckBox( self.xdr_panel, wx.ID_ANY, u"自动检测", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.xdr_checkBox_autodetect.SetValue(True)
        xdr_fgSizer_a1.Add( self.xdr_checkBox_autodetect, 0, wx.ALIGN_CENTER, 5 )

        self.xdr_checkBox_oneline = wx.CheckBox( self.xdr_panel, wx.ID_ANY, u"单行模式", wx.DefaultPosition, wx.DefaultSize, 0 )
        xdr_fgSizer_a1.Add( self.xdr_checkBox_oneline, 0, wx.ALIGN_CENTER, 5 )

        self.xdr_button_start = wx.Button( self.xdr_panel, wx.ID_ANY, u"解析", wx.DefaultPosition, wx.DefaultSize, 0 )
        xdr_fgSizer_a1.Add( self.xdr_button_start, 0, wx.ALL, 5 )

        self.xdr_button_viewdef = wx.Button( self.xdr_panel, wx.ID_ANY, u"查看定义", wx.DefaultPosition, wx.DefaultSize, 0 )
        xdr_fgSizer_a1.Add( self.xdr_button_viewdef, 0, wx.ALL, 5 )


        xdr_fgSizer_a1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.xdr_staticText_2 = wx.StaticText( self.xdr_panel, wx.ID_ANY, u"搜索：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.xdr_staticText_2.Wrap( -1 )

        xdr_fgSizer_a1.Add( self.xdr_staticText_2, 0, wx.ALIGN_CENTER, 5 )

        self.xdr_textCtrl_search = wx.TextCtrl( self.xdr_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        xdr_fgSizer_a1.Add( self.xdr_textCtrl_search, 0, wx.BOTTOM|wx.TOP, 5 )


        xdr_fgSizer_a.Add( xdr_fgSizer_a1, 0, wx.EXPAND, 5 )

        self.xdr_grid_result = wx.grid.Grid( self.xdr_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )

        # Grid
        self.xdr_grid_result.CreateGrid( 5, 5 )
        self.xdr_grid_result.EnableEditing( True )
        self.xdr_grid_result.EnableGridLines( True )
        self.xdr_grid_result.EnableDragGridSize( False )
        self.xdr_grid_result.SetMargins( 0, 0 )

        # Columns
        self.xdr_grid_result.EnableDragColMove( False )
        self.xdr_grid_result.EnableDragColSize( True )
        self.xdr_grid_result.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.xdr_grid_result.EnableDragRowSize( True )
        self.xdr_grid_result.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.xdr_grid_result.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        xdr_fgSizer_a.Add( self.xdr_grid_result, 9, wx.EXPAND, 5 )


        self.xdr_panel.SetSizer( xdr_fgSizer_a )
        self.xdr_panel.Layout()
        xdr_fgSizer_a.Fit( self.xdr_panel )
        self.main_notebook.AddPage( self.xdr_panel, u"XDR解析", False )
        self.sdl_panel = wx.Panel( self.main_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sdl_fgSizer_a = wx.FlexGridSizer( 2, 1, 0, 0 )
        sdl_fgSizer_a.AddGrowableCol( 0 )
        sdl_fgSizer_a.AddGrowableRow( 1 )
        sdl_fgSizer_a.SetFlexibleDirection( wx.BOTH )
        sdl_fgSizer_a.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        sdl_fgSizer_a1 = wx.FlexGridSizer( 1, 0, 0, 0 )
        sdl_fgSizer_a1.AddGrowableCol( 8 )
        sdl_fgSizer_a1.SetFlexibleDirection( wx.BOTH )
        sdl_fgSizer_a1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.sdl_button_loaddef = wx.Button( self.sdl_panel, wx.ID_ANY, u"加载SDL定义", wx.DefaultPosition, wx.DefaultSize, 0 )
        sdl_fgSizer_a1.Add( self.sdl_button_loaddef, 0, wx.ALIGN_CENTER, 5 )

        self.sdl_button_deldef = wx.Button( self.sdl_panel, wx.ID_ANY, u"删除定义", wx.DefaultPosition, wx.DefaultSize, 0 )
        sdl_fgSizer_a1.Add( self.sdl_button_deldef, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )

        self.sdl_staticText_1 = wx.StaticText( self.sdl_panel, wx.ID_ANY, u"选取定义：", wx.DefaultPosition, wx.Size( 70,-1 ), 0 )
        self.sdl_staticText_1.Wrap( -1 )

        sdl_fgSizer_a1.Add( self.sdl_staticText_1, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )

        sdl_comboBox_sdldefChoices = []
        self.sdl_comboBox_sdldef = wx.ComboBox( self.sdl_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, sdl_comboBox_sdldefChoices, wx.CB_READONLY|wx.CB_SORT )
        sdl_fgSizer_a1.Add( self.sdl_comboBox_sdldef, 0, wx.ALIGN_CENTER, 5 )

        self.sdl_button_start = wx.Button( self.sdl_panel, wx.ID_ANY, u"解析", wx.DefaultPosition, wx.DefaultSize, 0 )
        sdl_fgSizer_a1.Add( self.sdl_button_start, 0, wx.ALIGN_CENTER, 5 )

        self.sdl_staticText_2 = wx.StaticText( self.sdl_panel, wx.ID_ANY, u"显示方式：", wx.DefaultPosition, wx.Size( 70,-1 ), 0 )
        self.sdl_staticText_2.Wrap( -1 )

        sdl_fgSizer_a1.Add( self.sdl_staticText_2, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )

        sdl_comboBox_echoChoices = [ u"Good", u"JSON", u"GOOD", u"SJSON" ]
        self.sdl_comboBox_echo = wx.ComboBox( self.sdl_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, sdl_comboBox_echoChoices, wx.CB_READONLY )
        self.sdl_comboBox_echo.SetSelection( 0 )
        sdl_fgSizer_a1.Add( self.sdl_comboBox_echo, 0, wx.ALIGN_CENTER, 5 )

        self.sdl_button_modify = wx.Button( self.sdl_panel, wx.ID_ANY, u"修改", wx.DefaultPosition, wx.DefaultSize, 0 )
        sdl_fgSizer_a1.Add( self.sdl_button_modify, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )


        sdl_fgSizer_a1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.sdl_staticText_3 = wx.StaticText( self.sdl_panel, wx.ID_ANY, u"搜索：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sdl_staticText_3.Wrap( -1 )

        sdl_fgSizer_a1.Add( self.sdl_staticText_3, 0, wx.ALIGN_CENTER, 5 )

        self.sdl_textCtrl_search = wx.TextCtrl( self.sdl_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        sdl_fgSizer_a1.Add( self.sdl_textCtrl_search, 0, wx.ALL, 5 )

        self.sdl_button_search = wx.Button( self.sdl_panel, wx.ID_ANY, u"搜索", wx.DefaultPosition, wx.DefaultSize, 0 )
        sdl_fgSizer_a1.Add( self.sdl_button_search, 0, wx.ALL, 5 )


        sdl_fgSizer_a.Add( sdl_fgSizer_a1, 1, wx.EXPAND, 5 )

        sdl_fgSizer_a2 = wx.FlexGridSizer( 2, 0, 0, 0 )
        sdl_fgSizer_a2.AddGrowableCol( 0 )
        sdl_fgSizer_a2.AddGrowableCol( 1 )
        sdl_fgSizer_a2.AddGrowableRow( 1 )
        sdl_fgSizer_a2.SetFlexibleDirection( wx.BOTH )
        sdl_fgSizer_a2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.sdl_staticText_4 = wx.StaticText( self.sdl_panel, wx.ID_ANY, u"输入：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sdl_staticText_4.Wrap( -1 )

        sdl_fgSizer_a2.Add( self.sdl_staticText_4, 0, wx.ALL, 5 )

        self.sdl_staticText_5 = wx.StaticText( self.sdl_panel, wx.ID_ANY, u"输出：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sdl_staticText_5.Wrap( -1 )

        sdl_fgSizer_a2.Add( self.sdl_staticText_5, 0, wx.ALL, 5 )

        self.sdl_textCtrl_input = wx.TextCtrl( self.sdl_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CHARWRAP|wx.TE_MULTILINE )
        sdl_fgSizer_a2.Add( self.sdl_textCtrl_input, 1, wx.ALL|wx.EXPAND, 5 )

        self.sdl_textCtrl_out = wx.TextCtrl( self.sdl_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
        sdl_fgSizer_a2.Add( self.sdl_textCtrl_out, 1, wx.ALL|wx.EXPAND, 5 )


        sdl_fgSizer_a.Add( sdl_fgSizer_a2, 1, wx.EXPAND, 5 )


        self.sdl_panel.SetSizer( sdl_fgSizer_a )
        self.sdl_panel.Layout()
        sdl_fgSizer_a.Fit( self.sdl_panel )
        self.main_notebook.AddPage( self.sdl_panel, u"SDL解析", False )
        self.asn_panel = wx.Panel( self.main_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        asn_fgSizer_a = wx.FlexGridSizer( 2, 1, 0, 0 )
        asn_fgSizer_a.AddGrowableCol( 0 )
        asn_fgSizer_a.AddGrowableRow( 1 )
        asn_fgSizer_a.SetFlexibleDirection( wx.BOTH )
        asn_fgSizer_a.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        asn_fgSizer_a1 = wx.FlexGridSizer( 1, 0, 0, 0 )
        asn_fgSizer_a1.AddGrowableCol( 11 )
        asn_fgSizer_a1.SetFlexibleDirection( wx.BOTH )
        asn_fgSizer_a1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.asn_button_open = wx.Button( self.asn_panel, wx.ID_ANY, u"加载文件", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_open, 0, wx.ALL, 5 )

        self.asn_button_close = wx.Button( self.asn_panel, wx.ID_ANY, u"关闭文件", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_close, 0, wx.ALL, 5 )

        self.asn_staticText_1 = wx.StaticText( self.asn_panel, wx.ID_ANY, u"文件头：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.asn_staticText_1.Wrap( -1 )

        asn_fgSizer_a1.Add( self.asn_staticText_1, 0, wx.ALIGN_CENTER, 5 )

        self.asn_textCtrl_fileheader = wx.TextCtrl( self.asn_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
        asn_fgSizer_a1.Add( self.asn_textCtrl_fileheader, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )

        self.asn_staticText_2 = wx.StaticText( self.asn_panel, wx.ID_ANY, u"记录头：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.asn_staticText_2.Wrap( -1 )

        asn_fgSizer_a1.Add( self.asn_staticText_2, 0, wx.ALIGN_CENTER, 5 )

        self.asn_textCtrl_recordheader = wx.TextCtrl( self.asn_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
        asn_fgSizer_a1.Add( self.asn_textCtrl_recordheader, 0, wx.ALIGN_CENTER, 5 )

        self.asn_button_start = wx.Button( self.asn_panel, wx.ID_ANY, u"解析", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_start, 0, wx.ALL, 5 )

        self.asn_button_export = wx.Button( self.asn_panel, wx.ID_ANY, u"导出", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_export, 0, wx.ALL, 5 )

        self.asn_button_save = wx.Button( self.asn_panel, wx.ID_ANY, u"保存文件", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_save, 0, wx.ALL, 5 )

        self.asn_button_add = wx.Button( self.asn_panel, wx.ID_ANY, u"增加", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_add, 0, wx.ALL, 5 )

        self.asn_button_modify = wx.Button( self.asn_panel, wx.ID_ANY, u"修改", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_modify, 0, wx.ALL, 5 )

        self.asn_button_del = wx.Button( self.asn_panel, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_del, 0, wx.ALL, 5 )


        asn_fgSizer_a1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.asn_staticText_2 = wx.StaticText( self.asn_panel, wx.ID_ANY, u"搜索：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.asn_staticText_2.Wrap( -1 )

        asn_fgSizer_a1.Add( self.asn_staticText_2, 0, wx.ALIGN_CENTER, 5 )

        self.asn_textCtrl_search = wx.TextCtrl( self.asn_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_textCtrl_search, 0, wx.ALIGN_CENTER, 5 )

        self.asn_button_search = wx.Button( self.asn_panel, wx.ID_ANY, u"搜索", wx.DefaultPosition, wx.DefaultSize, 0 )
        asn_fgSizer_a1.Add( self.asn_button_search, 0, wx.ALL, 5 )


        asn_fgSizer_a.Add( asn_fgSizer_a1, 1, wx.EXPAND, 5 )

        asn_fgSizer_a2 = wx.FlexGridSizer( 1, 2, 0, 0 )
        asn_fgSizer_a2.AddGrowableCol( 1 )
        asn_fgSizer_a2.AddGrowableRow( 0 )
        asn_fgSizer_a2.SetFlexibleDirection( wx.BOTH )
        asn_fgSizer_a2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.asn_treeCtrl_result = wx.TreeCtrl( self.asn_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 350,-1 ), wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT|wx.TR_NO_LINES )
        asn_fgSizer_a2.Add( self.asn_treeCtrl_result, 0, wx.EXPAND|wx.RIGHT, 5 )

        asn_fgSizer_a2_1 = wx.FlexGridSizer( 2, 1, 0, 0 )
        asn_fgSizer_a2_1.AddGrowableCol( 0 )
        asn_fgSizer_a2_1.AddGrowableRow( 1 )
        asn_fgSizer_a2_1.SetFlexibleDirection( wx.BOTH )
        asn_fgSizer_a2_1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        asn_fgSizer_a2_1_1 = wx.FlexGridSizer( 1, 2, 0, 0 )
        asn_fgSizer_a2_1_1.AddGrowableCol( 0 )
        asn_fgSizer_a2_1_1.AddGrowableCol( 1 )
        asn_fgSizer_a2_1_1.SetFlexibleDirection( wx.BOTH )
        asn_fgSizer_a2_1_1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.asn_richText_hex = wx.richtext.RichTextCtrl( self.asn_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 550,550 ), 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        asn_fgSizer_a2_1_1.Add( self.asn_richText_hex, 3, wx.EXPAND |wx.ALL, 5 )

        self.asn_richText_ascii = wx.richtext.RichTextCtrl( self.asn_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        asn_fgSizer_a2_1_1.Add( self.asn_richText_ascii, 1, wx.EXPAND |wx.ALL, 5 )


        asn_fgSizer_a2_1.Add( asn_fgSizer_a2_1_1, 0, wx.EXPAND, 5 )

        self.asn_textCtrl_info = wx.TextCtrl( self.asn_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
        asn_fgSizer_a2_1.Add( self.asn_textCtrl_info, 0, wx.ALL|wx.EXPAND, 5 )


        asn_fgSizer_a2.Add( asn_fgSizer_a2_1, 1, wx.EXPAND, 5 )


        asn_fgSizer_a.Add( asn_fgSizer_a2, 1, wx.EXPAND, 5 )


        self.asn_panel.SetSizer( asn_fgSizer_a )
        self.asn_panel.Layout()
        asn_fgSizer_a.Fit( self.asn_panel )
        self.main_notebook.AddPage( self.asn_panel, u"ASN.1解析", False )
        self.tool_panel = wx.Panel( self.main_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.main_notebook.AddPage( self.tool_panel, u"工具", False )
        self.setting_panel = wx.Panel( self.main_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.main_notebook.AddPage( self.setting_panel, u"设置", False )

        mainbSizer.Add( self.main_notebook, 1, wx.EXPAND, 5 )


        self.SetSizer( mainbSizer )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.xdr_comboBox_xdrtype.Bind( wx.EVT_COMBOBOX, self.xdr_comboBox_xdrtypeOnCombobox )
        self.xdr_checkBox_autodetect.Bind( wx.EVT_CHECKBOX, self.xdr_checkBox_autodetectOnCheckBox )
        self.xdr_checkBox_oneline.Bind( wx.EVT_CHECKBOX, self.xdr_checkBox_onelineOnCheckBox )
        self.xdr_button_start.Bind( wx.EVT_BUTTON, self.xdr_button_startOnButtonClick )
        self.xdr_button_viewdef.Bind( wx.EVT_BUTTON, self.xdr_button_viewdefOnButtonClick )
        self.xdr_textCtrl_search.Bind( wx.EVT_TEXT, self.xdr_textCtrl_searchOnText )
        self.xdr_grid_result.Bind( wx.grid.EVT_GRID_CELL_CHANGED, self.xdr_grid_resultOnGridCellChange )
        self.sdl_button_loaddef.Bind( wx.EVT_BUTTON, self.sdl_button_loaddefOnButtonClick )
        self.sdl_button_deldef.Bind( wx.EVT_BUTTON, self.sdl_button_deldefOnButtonClick )
        self.sdl_button_start.Bind( wx.EVT_BUTTON, self.sdl_button_startOnButtonClick )
        self.sdl_comboBox_echo.Bind( wx.EVT_COMBOBOX, self.sdl_comboBox_echoOnCombobox )
        self.sdl_button_modify.Bind( wx.EVT_BUTTON, self.sdl_button_modifyOnButtonClick )
        self.sdl_button_search.Bind( wx.EVT_BUTTON, self.sdl_button_searchOnButtonClick )
        self.asn_button_open.Bind( wx.EVT_BUTTON, self.asn_button_openOnButtonClick )
        self.asn_button_close.Bind( wx.EVT_BUTTON, self.asn_button_closeOnButtonClick )
        self.asn_button_start.Bind( wx.EVT_BUTTON, self.asn_button_startOnButtonClick )
        self.asn_button_export.Bind( wx.EVT_BUTTON, self.asn_button_exportOnButtonClick )
        self.asn_button_save.Bind( wx.EVT_BUTTON, self.asn_button_saveOnButtonClick )
        self.asn_button_add.Bind( wx.EVT_BUTTON, self.asn_button_addOnButtonClick )
        self.asn_button_modify.Bind( wx.EVT_BUTTON, self.asn_button_modifyOnButtonClick )
        self.asn_button_search.Bind( wx.EVT_BUTTON, self.asn_button_searchOnButtonClick )
        self.asn_treeCtrl_result.Bind( wx.EVT_TREE_SEL_CHANGED, self.asn_treeCtrl_resultOnTreeSelChanged )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def xdr_comboBox_xdrtypeOnCombobox( self, event ):
        event.Skip()

    def xdr_checkBox_autodetectOnCheckBox( self, event ):
        event.Skip()

    def xdr_checkBox_onelineOnCheckBox( self, event ):
        event.Skip()

    def xdr_button_startOnButtonClick( self, event ):
        event.Skip()

    def xdr_button_viewdefOnButtonClick( self, event ):
        event.Skip()

    def xdr_textCtrl_searchOnText( self, event ):
        event.Skip()

    def xdr_grid_resultOnGridCellChange( self, event ):
        event.Skip()

    def sdl_button_loaddefOnButtonClick( self, event ):
        event.Skip()

    def sdl_button_deldefOnButtonClick( self, event ):
        event.Skip()

    def sdl_button_startOnButtonClick( self, event ):
        event.Skip()

    def sdl_comboBox_echoOnCombobox( self, event ):
        event.Skip()

    def sdl_button_modifyOnButtonClick( self, event ):
        event.Skip()

    def sdl_button_searchOnButtonClick( self, event ):
        event.Skip()

    def asn_button_openOnButtonClick( self, event ):
        event.Skip()

    def asn_button_closeOnButtonClick( self, event ):
        event.Skip()

    def asn_button_startOnButtonClick( self, event ):
        event.Skip()

    def asn_button_exportOnButtonClick( self, event ):
        event.Skip()

    def asn_button_saveOnButtonClick( self, event ):
        event.Skip()

    def asn_button_addOnButtonClick( self, event ):
        event.Skip()

    def asn_button_modifyOnButtonClick( self, event ):
        event.Skip()

    def asn_button_searchOnButtonClick( self, event ):
        event.Skip()

    def asn_treeCtrl_resultOnTreeSelChanged( self, event ):
        event.Skip()


###########################################################################
## Class xdr_Frame_viewdef
###########################################################################

class xdr_Frame_viewdef ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )


        self.Centre( wx.BOTH )

    def __del__( self ):
        pass



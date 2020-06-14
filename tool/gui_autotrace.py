#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import wx
import pathlib
import subprocess
import os
import json
import signal
from threading import Thread
from autotracevmd import autotracevmd

class AutoTraceFrame(wx.Frame):
    ''' MMD Motion auto-trace frame
    '''
    def __init__(self, *args, **kw):
        super(AutoTraceFrame, self).__init__(*args, **kw)

        self.thread = None
        self.Bind(wx.EVT_CLOSE, self.close_handler)
        panel = wx.Panel(self)
        self.label_selectfile = wx.StaticText(panel, wx.ID_ANY, 'input video file')
        self.txt_input_video = wx.TextCtrl(panel, wx.ID_ANY, size=(580, -1))
        self.button_selectfile = wx.Button(panel, wx.ID_ANY, 'Select')
        self.button_selectfile.Bind(wx.EVT_BUTTON, self.click_selectfile)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(self.label_selectfile, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        hsizer1.Add(self.txt_input_video, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        hsizer1.Add(self.button_selectfile, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)

        self.label_maxpeople = wx.StaticText(panel, wx.ID_ANY, 'max number of people')
        self.spin_maxpeople = wx.SpinCtrl(panel, wx.ID_ANY, "", min=1, max=100, initial=1)
        blank1 = wx.StaticText(panel, wx.ID_ANY, '')
        blank2 = wx.StaticText(panel, wx.ID_ANY, '')
        self.label_firstframe = wx.StaticText(panel, wx.ID_ANY, 'first frame to analyze')
        self.spin_firstframe = wx.SpinCtrl(panel, wx.ID_ANY, "", min=0, max=100000, initial=0)
        self.label_lastframe = wx.StaticText(panel, wx.ID_ANY, 'last frame to analyze')
        self.spin_lastframe = wx.SpinCtrl(panel, wx.ID_ANY, "", min=-1, max=100000, initial=-1)
        gsizer1 = wx.FlexGridSizer(4, 2, 2)
        gsizer1.Add(self.label_maxpeople, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer1.Add(self.spin_maxpeople, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer1.Add(blank1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer1.Add(blank2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer1.Add(self.label_firstframe, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer1.Add(self.spin_firstframe, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer1.Add(self.label_lastframe, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer1.Add(self.spin_lastframe, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)

        self.label_reversespec = wx.StaticText(panel, wx.ID_ANY, 'reverse_specific')
        self.txt_reversespec = wx.TextCtrl(panel, wx.ID_ANY, size=(580, -1))
        self.label_orderspec = wx.StaticText(panel, wx.ID_ANY, 'order_specific')
        self.txt_orderspec = wx.TextCtrl(panel, wx.ID_ANY, size=(580, -1))
        gsizer2 = wx.FlexGridSizer(2, 2, 2)
        gsizer2.Add(self.label_reversespec, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer2.Add(self.txt_reversespec, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer2.Add(self.label_orderspec, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        gsizer2.Add(self.txt_orderspec, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)

        self.check_verbose = wx.CheckBox(panel, wx.ID_ANY, 'show detailed messages')
        self.button_run = wx.Button(panel, wx.ID_ANY, 'Run')
        self.button_run.Bind(wx.EVT_BUTTON, self.click_run)
        self.txt_output = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer1, 0, wx.ALL | wx.ALIGN_LEFT)
        sizer.Add(gsizer1, 0, wx.ALL | wx.ALIGN_LEFT)
        sizer.Add(gsizer2, 0, wx.ALL | wx.ALIGN_LEFT)
        sizer.Add(self.check_verbose, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        sizer.Add(self.button_run, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(self.txt_output, 1, wx.ALL | wx.EXPAND, 2)
        panel.SetSizer(sizer)
        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("")
        sys.stdout = sys.stderr = self

    def write(self, msg):
        self.txt_output.AppendText(msg)
    
    def flush(self):
        pass

    def disable_all_buttons(self):
        self.button_selectfile.Disable()
        self.button_run.Disable()

    def enable_all_buttons(self):
        self.button_selectfile.Enable()
        self.button_run.Enable()

    def click_selectfile(self, event):
        dialog = wx.FileDialog(None, 'select input video file')
        dialog.ShowModal()
        filepath = dialog.GetPath()
        self.txt_input_video.SetValue(filepath)

    def click_run(self, event):
        video_file = self.txt_input_video.GetValue()
        if video_file is None or video_file == '':
            wx.MessageBox('select video file', 'ERROR', wx.OK | wx.ICON_ERROR, self)
            return
        video_path = pathlib.Path(video_file).resolve()
        if not video_path.is_file():
            wx.MessageBox('select valid video file', 'ERROR', wx.OK | wx.ICON_ERROR, self)
            return
        self.SetStatusText('running auto-trace')
        self.disable_all_buttons()
        self.thread = Thread(target=self.run_trace, args=(str(video_file), ))
        self.thread.setDaemon(True)
        self.thread.start()

    def run_trace(self, video_file):
        config_file = pathlib.Path('config.json')
        if config_file.is_file():
            with config_file.open() as fconf:
                conf = json.load(fconf)
        else:
            conf = {}
        conf['VIDEO_FILE'] = video_file
        if not 'output_dir' in conf:
            conf['output_dir'] = ''
        conf['first_frame'] = self.spin_firstframe.GetValue()
        conf['last_frame'] = self.spin_lastframe.GetValue()
        conf['max_people'] = self.spin_maxpeople.GetValue()
        conf['reverse_list'] = self.txt_reversespec.GetValue()
        conf['order_list'] = self.txt_orderspec.GetValue()
        if not 'order_start_frame' in conf:
            conf['order_start_frame'] = 0
        if not 'add_leg' in conf:
            conf['add_leg'] = True
        if not 'no_bg' in conf:
            conf['no_bg'] = False
        if self.check_verbose.GetValue():
            conf['log_level'] = 3
        else:
            conf['log_level'] = 1
        errmsg, result_dir = autotracevmd(conf)
        if errmsg is not None:
            wx.MessageBox(errmsg, 'ERROR', wx.OK | wx.ICON_ERROR, self)
            self.enable_all_buttons()
            self.SetStatusText('')
            return
        wx.MessageBox('auto-trace finished', 'COMPLETE', wx.OK | wx.ICON_NONE, self)
        command = 'explorer {}'.format(result_dir)
        proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, encoding='utf-8')
        while proc.poll() is None:
            msg = proc.stdout.readline()
            if msg:
                sys.stdout.write(msg)          
        self.enable_all_buttons()
        self.SetStatusText('')

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

    def OnExit(self, event):
        self.Close(True)

    def close_handler(self, event):
        if event.CanVeto() and self.thread is not None and self.thread.is_alive():
            answer = wx.MessageBox("Autotrace is not complete.\nAre you sure you want to exit?", "Exit?", wx.ICON_QUESTION | wx.YES_NO)
            if answer != wx.YES:
                event.Veto()
                return
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = AutoTraceFrame(None, title='MMD motion auto-trace', size=(800, 600))
    frame.Show()
    app.MainLoop()

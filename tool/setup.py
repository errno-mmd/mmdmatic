#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import wx
import pathlib
import subprocess
import requests
import zipfile
import shutil
import os
import json
import signal
import re
from threading import Thread
from queue import Queue, Empty
import make_checksum

def download_googledrive(id, filename):
    url = 'https://drive.google.com/uc?id={}&export=download'.format(id)
    print('downloading: ' + url)
    req = requests.get(url)
    if req.status_code != requests.codes.ok:
        errmsg = 'download error: status={}: url={}'.format(req.status_code, url)
        return errmsg
    cookies=req.cookies
    token = None
    for key, value in req.cookies.items():
        if key.startswith('download_warning'):
            token = value
    if token is None:
        return 'token not found in cookie: url={}'.format(url)
    url = 'https://drive.google.com/uc?export=download&confirm={}&id={}'.format(token, id)
    req = requests.get(url, cookies=cookies)
    if req.status_code != requests.codes.ok:
        errmsg = 'download error: status={}: url={}'.format(req.status_code, url)
        return errmsg
    with open(filename, 'wb') as f:
        f.write(req.content)
    return None

def extract_from_googledrive(id, zipname, dirname):
    errmsg = download_googledrive(id, zipname)
    if errmsg is not None:
        return errmsg
    print('extracting: ' + zipname)
    with zipfile.ZipFile(zipname) as zip:
        zip.extractall(dirname)
    os.remove(zipname)

def download_extract(url, zipname, dirname):
    print('downloading {}...'.format(url))
    req = requests.get(url, allow_redirects=True)
    if req.status_code != requests.codes.ok:
        errmsg = 'download error: status={}: url={}'.format(req.status_code, url)
        return errmsg
    with open(zipname, 'wb') as f:
        f.write(req.content)
    print('extracting {}...'.format(zipname))
    with zipfile.ZipFile(zipname) as zip:
        zip.extractall(dirname)
    os.remove(zipname)

def download_file(url, filename):
    print('downloading {}...'.format(url))
    req = requests.get(url, allow_redirects=True)
    if req.status_code != requests.codes.ok:
        errmsg = 'download error: status={}: url={}'.format(req.status_code, url)
        return errmsg
    with open(filename, 'wb') as f:
        f.write(req.content)

class SetupFrame(wx.Frame):
    ''' mmdmatic setup frame
    '''
    def __init__(self, *args, **kw):
        super(SetupFrame, self).__init__(*args, **kw)

        self.subproc = None
        self.thread = None
        self.Bind(wx.EVT_CLOSE, self.close_handler)
        panel = wx.Panel(self)
        self.button_install = wx.Button(panel, wx.ID_ANY, 'Install')
        self.button_install.Bind(wx.EVT_BUTTON, self.click_install)
        self.txt_output = wx.TextCtrl(panel, wx.ID_ANY, '', style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.button_install, 0, wx.ALL, 10)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer, 0, wx.ALL)
        sizer.Add(self.txt_output, 1, wx.ALL | wx.EXPAND, 2)
        panel.SetSizer(sizer)
        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("")
        config_file = pathlib.Path('_template/config.json')
        with config_file.open() as fconf:
            self.conf = json.load(fconf)
        sys.stdout = sys.stderr = self

    def write(self, msg):
        self.txt_output.AppendText(msg)
    
    def flush(self):
        pass

    def kill_subprocess(self):
        if self.subproc is not None:
            os.kill(self.subproc.pid, signal.SIGTERM)

    def disable_all_buttons(self):
        self.button_install.Disable()

    def enable_all_buttons(self):
        self.button_install.Enable()

    def click_install(self, event):
        self.SetStatusText('install')
        self.disable_all_buttons()
        self.thread = Thread(target=self.install_all)
        self.thread.start()

    def install_all(self):
        methods = [
            self.install_packages,
#            self.install_3dpose,
#            self.install_mannequinchallenge,
#            self.install_tfpose,
#            self.install_VMD3d
            self.install_tools
            ]
        for f in methods:
            errmsg = f()
            if errmsg is not None:
                wx.MessageBox(errmsg, 'ERROR', wx.OK | wx.ICON_ERROR, self)
                self.enable_all_buttons()
                return
        config_file = pathlib.Path('config.json')
        with config_file.open('w') as fconf:
            json.dump(self.conf, fconf, indent=4)
        self.SetStatusText('')
        wx.MessageBox('installation finished', 'COMPLETE', wx.OK | wx.ICON_NONE, self)
        self.enable_all_buttons()

    def install_packages(self):
        self.SetStatusText('installing packages')
        cmd = sys.executable
        commands = [
            '{} -u -m conda install --yes --file condapkglist.txt'.format(cmd),
            '{} -u -m conda install --yes --file torchpkglist.txt -c pytorch'.format(cmd),
            '{} -u -m pip install -r pypipkglist.txt'.format(cmd)
        ]
        for cmd in commands:
            ret = self.run_command(cmd)
            if ret != 0:
                return 'Install package error. retry later'
        return None

    def install_tools(self):
        checksum_file = 'checksum.json'
        checksum_path = pathlib.Path(checksum_file)
        with checksum_path.open() as fin:
            check_conf = json.load(fin)        
        tmppath = pathlib.Path('tmp')
        tmppath.mkdir(parents=True, exist_ok=True)
        for toolname, dllist in check_conf.items():
            self.SetStatusText('installing {}'.format(toolname))
            for zipname, dic in dllist.items():
                dirname = dic['dir']
                dirpath = pathlib.Path(dirname).resolve()
                dirpath.mkdir(parents=True, exist_ok=True)
                checksumlist = dic['checksum']
                up2date = True
                for filename, sum in checksumlist.items():
                    filepath = dirpath / filename
                    if filepath.is_file():
                        s = make_checksum.calc_checksum(str(filepath))
                        if s == sum:
                            continue
                    up2date = False
                    break
                if up2date:
                    print('Skip downloading {}: all files are up to date'.format(zipname))
                    continue
                else:
                    dirpath.mkdir(parents=True, exist_ok=True)
                    if 'url' in dic:
                        url = dic['url']
                        if re.search(r"\.zip$", zipname):
                            filepath = tmppath / zipname
                            download_extract(url, str(filepath), dirname)
                        else:
                            filepath = dirpath / zipname
                            download_file(url, str(filepath))
                    else:
                        id = dic['id']
                        if re.search(r"\.zip$", zipname):
                            filepath = tmppath / zipname
                            extract_from_googledrive(id, str(filepath), dirname)
                        else:
                            filepath = dirpath / zipname
                            download_googledrive(id, str(filepath))

    def install_3dpose(self):
        self.SetStatusText('installing 3d-pose-baseline-vmd')
        tag = 'mat1.03-3'
        pose3d_dir = './3d-pose-baseline-vmd-{}'.format(tag)
        self.conf['pose3d_dir'] = pose3d_dir
        url = 'https://github.com/errno-mmd/3d-pose-baseline-vmd/archive/{}.zip'.format(tag)
        zipname = './3d-pose-baseline-vmd-{}.zip'.format(tag)
        errmsg = download_extract(url, zipname, '.')
        if errmsg is not None:
            return errmsg

        data_dir = pose3d_dir + '/data'
        id = '1dr1LKWEA3L6cuSeljS5h-tzPqc0jyOAR'
        zipname = './h36m.zip'
        errmsg = extract_from_googledrive(id, zipname, data_dir)
        if errmsg is not None:
            return errmsg

        id = '1SNeg6OhaE99OKB8GE6RDfSl3hnjnJ-K7'
        zipname = './experiments.zip'
        errmsg = extract_from_googledrive(id, zipname, pose3d_dir)
        if errmsg is not None:
            return errmsg

        return None

    def install_mannequinchallenge(self):
        self.SetStatusText('installing mannequinchallenge-vmd')
        tag = 'ver1.03.02'
        depth_dir = './mannequinchallenge-vmd-{}'.format(tag)
        self.conf['depth_dir'] = depth_dir
        url = 'https://github.com/miu200521358/mannequinchallenge-vmd/archive/{}.zip'.format(tag)
        zipname = './mannequinchallenge-vmd-{}.zip'.format(tag)
        errmsg = download_extract(url, zipname, '.')
        if errmsg is not None:
            return errmsg

        commands = [
            'bash fetch_checkpoints.sh'.format(sys.executable)
        ]
        for cmd in commands:
            ret = self.run_command(cmd, cwd=depth_dir)
            if ret != 0:
                return 'Install mannequinchallenge error in {}'.format(cmd)
        return None

    def install_tfpose(self):
        self.SetStatusText('installing tf-pose-estimation')
        tag = 'mat1.03'
        tfpose_dir = './tf-pose-estimation-{}'.format(tag)
        self.conf['tfpose_dir'] = tfpose_dir
        url = 'https://github.com/errno-mmd/tf-pose-estimation/archive/{}.zip'.format(tag)
        zipname = './tf-pose-estimation-{}.zip'.format(tag)
        errmsg = download_extract(url, zipname, '.')
        if errmsg is not None:
            return errmsg

        url = 'https://github.com/errno-mmd/tf-pose-estimation/releases/download/mmdmatic1.02.01/pycocotools.zip'
        zipname = './pycocotools.zip'
        errmsg = download_extract(url, zipname, tfpose_dir)
        if errmsg is not None:
            return errmsg

        url = 'https://github.com/errno-mmd/tf-pose-estimation/releases/download/mmdmatic1.02.01/_pafprocess.cp37-win_amd64.pyd'
        filename = './tf-pose-estimation-{}/tf_pose/pafprocess/_pafprocess.cp37-win_amd64.pyd'.format(tag)
        print('downloading {}...'.format(url))
        req = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(req.content)
        return None

    def install_VMD3d(self):
        self.SetStatusText('installing VMD-3d-pose-baseline-multi')
        tag = 'ver1.03'
        vmd3d_dir = './VMD-3d-pose-baseline-multi-{}'.format(tag)
        self.conf['vmd3d_dir'] = vmd3d_dir
        url = 'https://github.com/miu200521358/VMD-3d-pose-baseline-multi/archive/{}.zip'.format(tag)
        zipname = './VMD-3d-pose-baseline-multi-{}.zip'.format(tag)
        errmsg = download_extract(url, zipname, '.')
        if errmsg is not None:
            return errmsg
        return None

    def recieve_message(self, proc):
        while proc.poll() is None:
            msg = proc.stdout.readline()
            if msg:
                #sys.stdout.write(msg)    
                self.txt_output.AppendText(msg)
        if proc.returncode == 0:
            wx.MessageBox('finished', 'COMPLETE', wx.OK | wx.ICON_NONE, self)
        else:
            wx.MessageBox('error', 'ERROR', wx.OK | wx.ICON_ERROR, self)
        self.enable_all_buttons()

    def run_command(self, command, **kwargs):
        sys.stdout.write(command + '\n')
        self.subproc = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1, **kwargs)
        while self.subproc.poll() is None:
            msg = self.subproc.stdout.readline()
            if msg:
                sys.stdout.write(msg)
        ret = self.subproc.returncode
        self.subproc = None
        return ret

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

    def OnExit(self, event):
        self.Close()

    def close_handler(self, event):
        if event.CanVeto() and self.thread is not None and self.thread.is_alive():
            answer = wx.MessageBox("Installation is not complete.\nExit setup?", "Exit?", wx.ICON_QUESTION | wx.YES_NO)
            if answer != wx.YES:
                event.Veto()
                return
        self.kill_subprocess()
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = SetupFrame(None, title='mmdmatic setup', size=(800, 600))
    frame.Show()
    app.MainLoop()

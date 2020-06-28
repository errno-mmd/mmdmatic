#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import pathlib
import requests
import zipfile
import json
import os
import re

def calc_checksum(filename):
    hash = hashlib.sha256()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(hash.block_size)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()

def download_file(url, filename):
    print('downloading {}...'.format(url))
    req = requests.get(url, allow_redirects=True)
    if req.status_code != requests.codes.ok:
        errmsg = 'download error: status={}: url={}'.format(req.status_code, url)
        return errmsg
    with open(filename, 'wb') as f:
        f.write(req.content)

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

def extract_zipfile(zipname, dirname):
    print('extracting {}...'.format(zipname))
    with zipfile.ZipFile(zipname) as zip:
        zip.extractall(dirname)

def get_filelist(zipname):
    with zipfile.ZipFile(zipname) as z:
        return z.namelist()

def make_checksum(template_file, output_file):
    dlcheck_path = pathlib.Path(template_file)
    with dlcheck_path.open() as fin:
        dlcheck_conf = json.load(fin)

    dirpath = pathlib.Path('./tmp').resolve()
    for toolname, dllist in dlcheck_conf.items():
        for zipname, dic in dllist.items():
            zippath = dirpath / zipname
            if 'url' in dic:
                download_file(dic['url'], str(zippath))
            else:
                download_googledrive(dic['id'], str(zippath))
            sumdic = {}
            if re.search(r"\.zip$", zipname):
                extract_zipfile(str(zippath), str(dirpath))
                for filename in get_filelist(str(zippath)):
                    filepath = dirpath / filename
                    if filepath.is_file():
                        checksum = calc_checksum(str(filepath))
                        sumdic[filename] = checksum
            else:
                checksum = calc_checksum(str(zippath))
                sumdic[zipname] = checksum
            dic['checksum'] = sumdic
    print(json.dumps(dlcheck_conf, indent=4))

    output_path = pathlib.Path(output_file)
    with output_path.open('w') as fout:
        json.dump(dlcheck_conf, fout, indent=4)


if __name__ == '__main__':
    template_file = '_template/checksum.json'
    output_file = 'checksum.json'
    make_checksum(template_file, output_file)

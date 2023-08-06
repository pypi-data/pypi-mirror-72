#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Handles all data-related features."""

from pathlib import Path
import functools
import json
import os

from munch import munchify, Munch
import requests

from omic.client import Client
from omic.global_ import GlobalClient
from omic.parallel import run_parallel 
from omic.util import strict_http_do, hit, check_args, get_cloud, \
                      download_url

__copyright__ = 'Copyright © 2020 Omic'

class DataClient(Client):
    def __init__(self, config: dict):
        self.config = config

    def create_bundle(self: object, files: list, vpath: str, mode: str, 
                      project: str, safe: bool = False) -> str:
        workload = [functools.partial(self.mount_data, rpath, vpath, mode, 
                                      project, safe) for rpath in files]
        file_ids = run_parallel(workload, batch_size=15)
        return hit('post',
                   endpoint=f'{self.config.endpoint}/data/bundle',
                   qparams={
                       'user': self.config.user, 
                       'mode': mode, 
                       'project': project
                   },
                   json_body={'data': file_ids},
                   headers={'x-api-key': self.config.key})._id

    # NOTE:  Formally `mount_data`.
    def mount(self, rpath: str, vpath: str, mode: str, project: str, 
              safe: bool = False):
        # TODO:  Add a parameter to preserve structure of rpath 
        #        (under mount key).  Right now we have flattened `vpath`s.
        qparams = {
            'user': self.config.user, 
            'mode': mode,
            'project': project,
            'cmd': 'mount',
            'repr': 'file',
            'mode': mode,
            'vpath': vpath, 
            'rpath': rpath,
            'safe': safe
        }
        print('Mount data:', rpath, '->', vpath)
        return self._hit('post',
                         endpoint=f'{self.config.endpoint}/data',
                         qparams=qparams,
                         headers={'x-api-key': self.config.key}).id

    def ls(self, **kwargs):
        args = {'mode': 'public', 'vpath': '/'} 
        args.update(kwargs)
        if 'project' not in args:
            # Fetch current project from user if none exists.
            gclient = GlobalClient(self.config)
            project = gclient.retrieve_project().project
            args.update({'project': project._id})
        check_args(args, {'_id', 'mode', 'project', 'vpath'})
        return self._hit(
            'get',
            endpoint=f'{self.config.endpoint}/data',
            qparams={'cmd': 'ls', **args}
        )

    # NOTE:  Formally `get_data`.
    def stat(self, **kwargs):
        return self._hit(
            'get',
            endpoint=f'{self.config.endpoint}/data',
            qparams={'cmd': 'stat', **kwargs}
        )

    def download(self, vpath: str, mode: str = 'public', 
                 project: str = None, download_dir: str = './'):
        files = self.ls(vpath=vpath, mode=mode, project=project)
        # TODO:  Test GCP here.
        # files = [munchify({"_id":"data-4ef94dfb-e026-41a5-9d82-f6f64d2172d3","repr":"file","mode":"private","user":"63be793a-6e1b-40cd-9f70-49dd73f470ab","name":"Homo_sapiens_assembly38.chrM.shifted_by_8000_bases.fasta.ann","mount":"gs://broad-references/hg38/v0/chrM/Homo_sapiens_assembly38.chrM.shifted_by_8000_bases.fasta.ann","vpath":"/recipe-parameters/Homo_sapiens_assembly38.chrM.shifted_by_8000_bases.fasta.ann","rpath":"gs://broad-references/hg38/v0/chrM/Homo_sapiens_assembly38.chrM.shifted_by_8000_bases.fasta.ann","_type":"data","created":"2020-04-01T01:50:09.713826"})]
        for f in files:
            try:
                # Stat the file
                s = self.stat(_id=f._id)
                # Setup local path location
                lp = s.vpath[len(vpath):]
                lp = lp[1:] if lp.startswith('/') else lp
                lp = os.path.join(download_dir, lp) 
                lp = str(Path(lp).resolve())
                ldirs, _ = os.path.split(lp)
                Path(ldirs).mkdir(parents=True, exist_ok=True)
                # Download file in parallel
                download_url(s.url, lp)
            except Exception as ex:
                print(f'Could not download {f.name}.', ex)

    def get_bundle(self, user: str, _id: str, fulfill=False, recurse=False):
        def _func():
            return requests.get(
                f'{API_BASE}/data/bundle', params={
                '_id': _id,
                'user': user,
                'fulfill': fulfill, 
                'recurse': recurse
            })
        return strict_http_do(_func)

    def get_bundle_or_data(self, user: str, _id: str, fulfill=False, 
                           recurse=False):
        data = get_data(user, _id)
        if not data:
            return get_bundle(user, _id, fulfill, recurse) 
        return data 
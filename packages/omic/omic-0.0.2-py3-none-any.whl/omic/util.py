#!/usr/bin/env python3
# -.- coding: utf-8 -.-

from urllib.parse import urlparse, quote
import time
import json
import os

from munch import munchify, Munch
import humps
import requests

from omic.const import *

__copyright__ = 'Copyright © 2020 Omic'

def retry(f, n=5, *args, **kwargs):
    """Basic exponential retry.  Throw exception after we've retried 
    sufficiently.
    """
    last_ex = None
    for i in range(n):
        try:
            response = f(*args, **kwargs)
            assert 200 <= response.status_code < 300, response.text
            return response
        except Exception as ex:
            last_ex = ex
            time.sleep(2 ** i)
    raise ValueError(f'Retry failed:  {repr(last_ex)}') 

def strict_http_do(f, n=5):
    """Ensure we retry the request and it eventually succeeds."""
    response = retry(f, n)
    if hasattr(response, 'text') and len(response.text.strip()) > 0:
        return munchify(json.loads(response.text))
    return None

# TODO:  Delete this and migrate dependencies to `client.py`.
def hit(method: str, endpoint: str, qparams: dict = {}, headers: dict = {}, 
       json_body: dict = None) -> Munch:
    """Abstraction on all HTTP methods with our API."""
    method_map = {
        'get': requests.get,
        'post': requests.post,
    }
    methodf = method_map[method.lower()]
    print('-' * 50)
    print(f'Hitting {endpoint} ({method}):')
    print('Parameters:', json.dumps(qparams, indent=4))
    print('Body:', json.dumps(json_body, indent=4))
    print('-' * 50)
    return strict_http_do(lambda: methodf(endpoint, params=qparams, 
                                          headers=headers, json=json_body))

def get_cloud(rpath):
    if rpath.strip().startswith('gs://'):
        return 'gcp'
    elif rpath.strip().startswith('s3://'):
        return 'aws'
    else:
        raise ValueError('Cloud address not recognized.')

def check_args(kwargs, args):
    kwargs_set = set(kwargs.keys())
    assert kwargs_set.issubset(args), \
        'Unsupported arguments "{}" found.'.format(args - kwargs_set)

def split_rpath(rpath):
    """Return rpath object bucket and key."""
    o = urlparse(rpath, allow_fragments=False)
    bucket, key = o.netloc, o.path[1:]
    return bucket, key

def download_url(url: str, output_file: str):
    # TODO:  
    r = requests.get(url, stream=True)
    with open(output_file, 'wb+') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    
def pythonify(obj):
    if isinstance(obj, str):
        obj = json.loads(obj)
    # return munchify(humps.decamelize(obj))
    return munchify(obj)
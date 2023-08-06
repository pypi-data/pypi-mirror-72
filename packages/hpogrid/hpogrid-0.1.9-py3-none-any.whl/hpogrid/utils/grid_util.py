import os
import json
import shutil
import subprocess

import tarfile
from pdb import set_trace

#import re
import fnmatch

try:
    from hpogrid.utils import stylus
except:
    raise ImportError('Cannot import hpogrid module. Try source setupenv first.')


def extract_inputDS(in_path='/ctrdata/', out_path='/ctrdata/'):
    tarfiles = [ f for f in os.listdir(in_path) if f.endswith('tar.gz')]
    for f in tarfiles:
        tar = tarfile.open(f, "r:gz")
        print('untaring the file {}'.format(f))
        tar.extractall(path=out_path)
        inputDS = tar.getnames()
        tar.close()


    return inputDS

def remove_inputDS(inputDS):
    for ds in inputDS:
        if os.path.isfile(ds):
            os.remove(ds)
        elif os.path.isdir(ds):
            shutil.rmtree(ds)

def show_grid_site_info(name_filter=None, gpu=True, active=True, site_type=['analysis', 'unified'],
    info = ['state', 'status', 'maxinputsize', 'maxmemory', 'maxtime']):
   grid_site_info = extract_grid_site_info(name_filter, gpu, active, site_type, info)
   print(stylus.create_table(grid_site_info, transpose=True))


def get_grid_site_list(name_filter=None, gpu=True, active=True, site_type=['analysis', 'unified']):
    grid_site_info = extract_grid_site_info(name_filter, gpu, active, site_type)
    return grid_site_info.keys()

def extract_grid_site_info(name_filter=None, gpu=True, active=True, site_type=['analysis', 'unified'],
    info = ['state', 'status', 'maxinputsize', 'maxmemory', 'maxtime']):
    '''
    retrieve some basic information of PanDA grid sites
    '''
    try:
      jsonfileLocation = os.environ['ALRB_cvmfs_repo'] + '/sw/local/etc/agis_schedconf.json'
    except:
      jsonfileLocation = '/cvmfs/atlas.cern.ch/repo/sw/local/etc/agis_schedconf.json'

    with open(jsonfileLocation,'r') as jsonfile:
      jsondata = json.load(jsonfile)

    if name_filter is None:
        name_filter = '*'

    grid_site_info = {}

    for site in jsondata:
        # filter site names (could also match jsondata[site]['panda_resource'] instead)
        if not fnmatch.fnmatch(site, name_filter):
            continue
        # filter non-active grid sites
        if active and (not jsondata[site]['state'] == 'ACTIVE'):
            continue
        # no good indicator of a GPU site yet will just judge on site name
        if gpu and (not 'GPU' in jsondata[site]['panda_resource']):
            continue
        if jsondata[site]['type'] not in site_type:
            continue
        grid_site_info[site] = {key: jsondata[site][key] for key in info}

    return grid_site_info
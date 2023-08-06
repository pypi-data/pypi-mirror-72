import os
import sys
import glob
import argparse
import json
import subprocess
from ray import tune
from pdb import set_trace
import numpy as np


try:
    from hpogrid.components.defaults import *
    from hpogrid.utils import helper    
except:
    raise ImportError('Cannot import hpogrid module. Try source setupenv first.')


kGPUSiteNGPU = {
    'ANALY_MANC_GPU_TEST': 10, #single queue, no submission parameters, 1 GPU per job
    'ANALY_QMUL_GPU_TEST': 6, #    GPUNumber=x for now is hardcoded in the dev APF JDL,number of GPUs per job limited by cgroups, K80=2*K40, so total of 6 gpu slots avalable.
    'ANALY_MWT2_GPU': 8, #single queue, no submission parameters, 1 GPU per job
    'ANALY_BNL_GPU_ARC': 12, #also shared with Jupyter users who have priority
    'ANALY_INFN-T1_GPU': 2 #single queue, no submission parameters, 1 GPU per job
}

class GridHandler():
    def __init__(self):
        # submit grid job via hpogrid executable
        if len(sys.argv) > 1:
            self.run_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('proj_name', help='the project to submit a grid job')               
        parser.add_argument('-n','--n_jobs', type=int, help='number of jobs to submit',
            default=1)
        parser.add_argument('-s','--site', help='site to submit the job to '
            '(this will override the grid config site setting)', choices=kGPUGridSiteList)
        return parser

    def run_parser(self):
        parser = self.get_parser()
        if os.path.basename(sys.argv[0]) == 'hpogrid':
            args = parser.parse_args(sys.argv[2:])
        else:
            args = parser.parse_args(sys.argv[1:])
        self.submit_job(args.proj_name, args.n_jobs, args.site)

    def submit_job(self, proj_name, n_jobs=1, site=None):

        grid_config = helper.get_grid_config(proj_name)

        options = {}

        options['containerImage'] = grid_config['container']

        options['exec'] = '"python /hpogrid/hpogrid/components/JobHandler.py {}"'.format(proj_name)

        if not grid_config['retry']:
            options['disableAutoRetry'] = ''

        extra = {'forceStaged':'', 
                 'useSandbox': '',
                 'noBuild': ''}
        options.update(extra)
        options['ctrWorkdir'] = '/hpogrid/project'
        options['ctrDatadir'] = '/hpogrid/project'

        if grid_config['inDS']:
            options['inDS'] = grid_config['inDS']

        if '{HPO_PROJECT_NAME}' in grid_config['outDS']:
            grid_config['outDS'] = grid_config['outDS'].format(HPO_PROJECT_NAME=proj_name)
        options['outDS'] = grid_config['outDS']

        if (site == None) and (grid_config['site'] not in ['None', None]):
            site = grid_config['site']

        if site is not None:
            options['site'] = site
            if 'GPU' in site:
                options['cmtConfig'] = 'nvidia-gpu'
            else:
                options['nCore'] = '8'

        # construct prun command
        command = ' '.join(["--{} {}".format(key,value) for (key,value) in options.items()])

        # options['workDir'] = project_path # does not really work
        project_path = helper.get_project_path(proj_name)

        # switch to working directory to send files to WNs
        with helper.cd(project_path):
            # submit grid jobs
            for _ in range(n_jobs):
                os.system("prun {}".format(command))

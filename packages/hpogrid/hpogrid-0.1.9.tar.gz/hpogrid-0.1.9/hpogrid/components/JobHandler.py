import os
import sys
import json
import time
import importlib
import argparse
from datetime import datetime
from pdb import set_trace

import ray
from ray import tune

try:
    from hpogrid.components import validation
    from hpogrid.components.defaults import *
    from hpogrid.utils import helper
except:
    raise ImportError('Cannot import hpogrid module. Try source setupenv first.')
    

class JobHandler():
    def __init__(self, parse=True):
        # run hyperparameter optimization for a project via hpogrid executable
        if (len(sys.argv) > 1) and parse:
            self.run_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('proj_name', help='the project to run hyperparameter optimization')
        return parser    

    def run_parser(self):
        parser = self.get_parser()
        if os.path.basename(sys.argv[0]) == 'hpogrid':
            args = parser.parse_args(sys.argv[2:])
        else:
            args = parser.parse_args(sys.argv[1:])
        self.run_project(args.proj_name)

    def get_scheduler(self, name, metric, mode, search_space = None, **args):
        if (name == None) or (name == 'None'):
            return None
        elif name == 'asynchyperband':
            from hpogrid.scheduler.asynchyperband_scheduler import AsyncHyperBandSchedulerWrapper
            return AsyncHyperBandSchedulerWrapper().create(metric, mode, **args)
        elif name == 'bohbhyperband':
            from hpogrid.scheduler.bohbhyperband_scheduler import BOHBHyperBandSchedulerWrapper
            return BOHBHyperBandSchedulerWrapper().create(metric, mode, **args)
        elif name == 'pbt':
            from hpogrid.scheduler.pbt_scheduler import PBTSchedulerWrapper
            if search_space is None:
                raise ValueError('search space must be set before using pbt scheduler')
            return PBTSchedulerWrapper().create(metric, mode, search_space, **args)

    def rename_algorithm(self, algo):
        if algo == 'random':
            algo = 'tune'
        elif algo == 'bayesian':
            algo = 'skopt'
        return algo
        
    def get_search_space(self, raw_space, algo):
        if raw_space is None:
            raise ValueError('search space can not be empty')    
        algo = self.rename_algorithm(algo)
        if algo == 'ax':
            from hpogrid.search_space.ax_space import AxSpace
            return AxSpace(raw_space).get_search_space()
        elif algo == 'bohb':
            from hpogrid.search_space.bohb_space import BOHBSpace
            return BOHBSpace(raw_space).get_search_space()
        elif algo == 'hyperopt':
            from hpogrid.search_space.hyperopt_space import HyperOptSpace
            return HyperOptSpace(raw_space).get_search_space()
        elif algo == 'skopt':
            from hpogrid.search_space.skopt_space import SkOptSpace
            return SkOptSpace(raw_space).get_search_space()
        elif algo == 'tune':
            from hpogrid.search_space.tune_space import TuneSpace
            return TuneSpace(raw_space).get_search_space()
        elif algo == 'nevergrad':
            from hpogrid.search_space.nevergrad_space import NeverGradSpace
            return NeverGradSpace(raw_space).get_search_space() 
        else:
            raise ValueError('the algorithm {} is not supported'.format(algo))

    def get_algorithm(self, algo, metric, mode, space, **args):
        algo = self.rename_algorithm(algo)
        if algo == 'ax':
            from hpogrid.algorithm.ax_algorithm import AxAlgoWrapper
            return AxAlgoWrapper().create(metric, mode, space, **args)
        elif algo == 'bohb':
            from hpogrid.algorithm.bohb_algorithm import BOHBAlgoWrapper
            return BOHBAlgoWrapper().create(metric, mode, space, **args)
        elif algo == 'hyperopt':
            from hpogrid.algorithm.hyperopt_algorithm import HyperOptAlgoWrapper
            return HyperOptAlgoWrapper().create(metric, mode, space, **args)
        elif algo == 'skopt':
            from hpogrid.algorithm.skopt_algorithm import SkOptAlgoWrapper
            return SkOptAlgoWrapper().create(metric, mode, space, **args)
        elif algo == 'nevergrad':
            from hpogrid.algorithm.nevergrad_algorithm import NeverGradAlgoWrapper
            return NeverGradAlgoWrapper().create(metric, mode, space, **args)
        elif algo == 'tune':
            return None
        else:
            raise ValueError('the algorithm {} is not supported'.format(algo))

    def get_model(self, script_name, model_name):
        model = None
        script_name_noext = os.path.splitext(script_name)[0]
        try: 
            module = importlib.import_module(script_name_noext)
            model = getattr(module, model_name)
        except: 
            raise ImportError('Unable to import function/class {} '
                'from training script: {}.py'.format(model_name, script_name_noext))
        return model

    def save_metadata(self, df, summary={}):
        hyperparameters = {key:key.replace('config/','') for key in df if 'config/' in key}
        df = df.rename(columns=hyperparameters)
        df = df.rename(columns={'time_total_s':'time_s'})
        hp_raw = list(hyperparameters.keys())
        hp = list(hyperparameters.values())
        columns_to_save = ['time_s']
        columns_to_save.extend(hp)
        if 'metric' in summary:
            columns_to_save.append(summary['metric'])
        df = df.filter(columns_to_save, axis=1).transpose()
        result = df.to_dict()
        summary['result'] = result
        summary['hyperparameters'] = hp

        with open(kGridSiteMetadataFileName,'w') as output:
            json.dump(summary, output)

    @staticmethod
    def get_resource_info():
        resource = {}
        n_gpu = helper.get_n_gpu()
        n_cpu = helper.get_n_cpu()
        print('INFO: Number of GPUs detected: ',n_gpu)
        print('INFO: Number of CPUs detected: ',n_cpu)
        if n_gpu > 0:
            resource['gpu'] = n_gpu
            print('INFO: Each trial will use {} GPU(s) resource'.format(n_gpu))
        if n_cpu > 0:
            resource['cpu'] = n_cpu
            print('INFO: Each trial will use {} CPU(s) resource'.format(n_cpu))
        if not resource:
            resource = None
        return resource

    def run(self, hpo_config, search_space, model_config, proj_name=None):
        start = time.time()

        algorithm = self.rename_algorithm(hpo_config['algorithm'])

        if algorithm == 'tune':
            tune_config_space = self.get_search_space(search_space, algo='tune')
        else:
            tune_config_space = {}

        tune_config_space.update(model_config['param'])

        algorithm = self.get_algorithm(
            algorithm,
            hpo_config['metric'],
            hpo_config['mode'],
            search_space, **hpo_config['algorithm_param'])
    
        scheduler = self.get_scheduler(
            hpo_config['scheduler'],
            hpo_config['metric'],
            hpo_config['mode'],
            search_space, **hpo_config['scheduler_param'])

        resources_per_trial = JobHandler.get_resource_info()

        model = self.get_model( model_config['script'], model_config['model'])

        #ray.init(node_ip_address="127.0.0.1", ignore_reinit_error=True)
        ray.init(ignore_reinit_error=True)

        start_data_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        analysis = tune.run(
            model,
            name=proj_name,
            scheduler=scheduler,
            search_alg=algorithm,
            config=tune_config_space,
            num_samples=hpo_config['trials'],
            resources_per_trial=resources_per_trial,
            verbose=hpo_config['verbose'],
            local_dir=hpo_config['log_dir'],
            stop=hpo_config['stop'],
            raise_on_failed_trial=False)

        end = time.time()
        total_time = float(end-start)
        end_data_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        best_config = analysis.get_best_config(metric=hpo_config['metric'], mode = hpo_config['mode'])
        print("Best config: ", best_config)
        print("Time taken in seconds: ", total_time)

        df = analysis.dataframe()

        summary = {
            'title' : proj_name,
            'start_date_time': start_data_time,
            'end_date_time': end_data_time,
            'task_time_s' : total_time,
            'metric': hpo_config['metric'],
            'mode' : hpo_config['mode'],
            'best_config' : best_config, 
        }

        self.save_metadata(df, summary)
    
        ray.shutdown()

    def run_project(self, proj_name):
        
        hpo_config = helper.get_hpo_config(proj_name)

        model_config = helper.get_model_config(proj_name)

        search_space = helper.get_search_space_config(proj_name)

        helper.set_script_paths(proj_name)

        self.run(hpo_config, search_space, model_config, proj_name)

        helper.set_script_paths(proj_name, undo=True)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('proj_name')
    args = parser.parse_args()
    JobHandler().run_project(args.proj_name)

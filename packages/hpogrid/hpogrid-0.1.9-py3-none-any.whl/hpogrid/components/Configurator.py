import sys, os
import argparse
import json
import shutil
#import re
import fnmatch


import pandas as pd 
from pdb import set_trace
from distutils import dir_util
from datetime import datetime
from tabulate import tabulate
from json import JSONDecodeError


try:
    from hpogrid.components import validation
    from hpogrid.components.defaults import *
    from hpogrid.utils import stylus
except:
    raise ImportError('Cannot import hpogrid module. Try source setupenv first.')


kAction = ['create', 'recreate', 'update', 'list', 'show', 'remove']  
kConfigAction = ['create', 'recreate', 'update']
kConfigList = ['hpo_config', 'grid_config', 'search_space', 'model_config', 'project_config']


class ConfigurationBase():

    def __init__(self):
        self.initialize()
        parser = self.get_parser() 
        args = parser.parse_args(sys.argv[2:3])
        action = args.action
        parser = self.get_parser(action)
        args = parser.parse_args(sys.argv[3:])

        if action in kConfigAction:
            self.configure(args, action)
        elif hasattr(self, action):
            getattr(self, action)(**vars(args))
        else:
            print('Unrecognized action: {}'.format(action))
            parser.print_help()
            exit(1)            

    def initialize(self):
        self.description = 'Manage configuration'
        self.usage = 'hpogrid <config_type> <action> <config_name> [<options>]'
        self.config_type = 'SUPPRESS'
        self.list_columns = []
        self.show_columns = []

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            description=self.description,
            usage=self.usage) 
        return parser

    def get_parser(self, action=None):
        parser = self.get_base_parser()           
        if not action:
            parser.add_argument('action', help='Action to be performed', choices=kAction)    
        elif action == 'list':
            parser.add_argument('--expr', metavar='',
                help='Filter out config files that matches the expression')
        elif action == 'show':
            parser.add_argument('name', help='Name of config file to show')
        elif action == 'remove':
            parser.add_argument('name', help='Name of config file to remove')
        else:
            raise ValueError('Unknown method: {}'.format(action))
        return parser

    def get_base_dir(self, config_type=None, force_create=True):

        if config_type is None:
            config_type = self.config_type
            
        if config_type == 'project':
            base_dir = os.path.join(os.environ[kHPOGridEnvPath], 'project')
        else:
            base_dir = os.path.join(os.environ[kHPOGridEnvPath], 'config', config_type)

        if (not os.path.exists(base_dir)) and force_create:
            os.makedirs(base_dir, exist_ok=True)
        return base_dir

    def get_config_path(self, config_name=None, config_type=None, extension='.json'):
        if config_name is None:
            config_name = self.config_name
        if config_type is None:
            config_type = self.config_type
        base_dir = self.get_base_dir(config_type)
        config_base_name = '{}{}'.format(config_name, extension)
        config_path = os.path.join(base_dir, config_base_name)
        return config_path

    def remove(self, name):
        config_path = self.get_config_path(name)
        if os.path.exists(config_path):
            os.remove(config_path)
            print('INFO: Removed file {}'.format(config_path))
        else:
            print('ERROR: Cannot remove file {}. File does not exist.'.format(config_path))

    def get_updated_config(self, config):
        non_updated_keys = []
        for key in config:
            if config[key] is None:
                non_updated_keys.append(key)
        for key in non_updated_keys:
            config.pop(key, None)
        config_path = self.get_config_path(config['name'])
        if not os.path.exists(config_path):
            raise FileNotFoundError('Configuration file {} not found. Update aborted.'.format(config_path))
        old_config = json.load(open(config_path))
        config = {**old_config, **config}
        return config

    def _retain_only_updated_options(self):
        parser = self.get_parser('update')
        for action in parser._actions:
            if (len(action.option_strings) > 0) and (action.default != '==SUPPRESS=='):
                action.default=None
        args = parser.parse_args(sys.argv[3:])
        return args

    def configure(self, args, action='create'):
        if action == 'update':
            args = self._retain_only_updated_options()

        config = vars(args)
        
        if action == 'update':
            config = self.get_updated_config(config)

        self.process_config(config)
        if config is not None:
            self.save(config, args.name, action)
        return config

    def process_config(self, config):
        for key in config:
            if isinstance(config[key], bool):
                config[key] = int(config[key])
        return config

    def save(self, config, name, action='create'):

        config_path = self.get_config_path(name)
        if (os.path.exists(config_path)) and (action=='create'):
            print('ERROR: {} configuration with name {} already exists.'
                'If you want to overwrite, use "recreate" or "update" action instead of "create".'.format(
                self.config_type, name))
        else:
            with open(config_path, 'w') as config_file:
                json.dump(config, config_file, indent=2)
            action_map = { 'create': 'Created', 'recreate': 'Recreated', 'update': 'Updated'}
            print('INFO: {} {} configuration {}'.format(action_map[action], self.config_type, config_path))
            self.show(name)

    def get_config_list(self, expr=None):
        if not expr:
            expr = '*'
        base_dir = self.get_base_dir()
        config_list = [os.path.splitext(d)[0] for d in os.listdir(base_dir) if not d.startswith('.')]
        if expr is not None:
            config_list = fnmatch.filter(config_list, expr)
        return config_list

    def load_config(self, config_name):
        config_path = self.get_config_path(config_name)
        if not (os.path.exists(config_path)):
            raise FileNotFoundError("The configuration file {} does not exist.".format(config_path))
        config = json.load(open(config_path))
        return config

    def list(self, expr=None):
        config_list = self.get_config_list(expr)
        table = stylus.create_table(config_list, self.list_columns)
        print(table)

    def show(self, name):
        config = self.load_config(name)
        table = stylus.create_table(config.items(), self.show_columns)
        print(table)

class HPOConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage configuration for hyperparameter optimization'
        self.usage = 'hpogrid hpo_config <action> <config_name> [<options>]'
        self.config_type = 'hpo'
        self.list_columns = ['HPO Configuration']
        self.show_columns = ['Attribute', 'Value']    

    def get_parser(self, action=None):
        parser = self.get_base_parser()        
        if action in kConfigAction:
            parser.add_argument('name', help= "Name given to the configuration file")
            parser.add_argument('-a','--algorithm', 
                                help='Algorithm for hyperparameter optimization', 
                                default=kDefaultSearchAlgorithm, choices=kSearchAlgorithms)
            parser.add_argument('-m', '--metric', metavar='',
                                help='Evaluation metric to be optimized', 
                                default=kDefaultMetric)
            parser.add_argument('-o', '--mode', 
                                help='Mode of optimization (either "min" or "max")', 
                                default=kDefaultMode, choices=kMetricMode)
            parser.add_argument('-s','--scheduler', 
                                help='Trial scheduling method for hyperparameter optimization',
                                default=kDefaultScheduler, choices=kSchedulers)
            parser.add_argument('-t','--trials', metavar='',
                                help='Number of trials (search points)', 
                                type=int, default=kDefaultTrials)
            parser.add_argument('-l', '--log_dir', metavar='',
                                help='Logging directory',
                                default=kDefaultLogDir)
            parser.add_argument('-v','--verbose', action='store_true', 
                                help='Check to enable verbosity')
            parser.add_argument('--stop', metavar='',
                                help='Stopping criteria for the training',
                                default=kDefaultStopping)
            parser.add_argument('--scheduler_param', metavar='',
                                help='Extra parameters given to the trial scheduler', 
                                default=kDefaultSchedulerParam)
            parser.add_argument('--algorithm_param', metavar='',
                                help='Extra parameters given to the hyperparameter optimization algorithm',
                                default=kDefaultAlgorithmParam)
        else:
            parser = super().get_parser(action)
        return parser

    def process_config(self, config):
        super().process_config(config)

        json_interp = ['stop', 'scheduler_param', 'algorithm_param']
        for key in json_interp:
            if (key in config) and isinstance(config[key],str):
                try:
                    config[key] = json.loads(config[key])
                except JSONDecodeError:
                    print('ERROR: Cannot decode the value of {} into json format.'
                        'Please check your input.'.format(key))
                    return None                

        return config

class GridConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage configuration for grid job submission'
        self.usage = 'hpogrid grid_config <action> <config_name> [<options>]'
        self.config_type = 'grid'
        self.list_columns = ['Grid Configuration']
        self.show_columns = ['Attribute', 'Value']  

    def get_parser(self, action=None):
        parser = self.get_base_parser()
        if action in kConfigAction:         
            parser.add_argument('name', help = "Name given to the configuration file")
            parser.add_argument('-s', '--site', 
                                help='Name of the grid site to where the jobs are submitted',
                                required=False, default=kDefaultGridSite,
                                choices=kGPUGridSiteList)
            parser.add_argument('-c', '--container', metavar='',
                                help='Name of the docker or singularity container in which the jobs are run', 
                                required=False, default=kDefaultContainer)
            parser.add_argument('-r', '--retry',
                                help='Check to enable retrying faild jobs',
                                action='store_true')
            parser.add_argument('-i', '--inDS', metavar='',
                                help='Name of input dataset')
            parser.add_argument('-o', '--outDS', metavar='',
                                help='Name of output dataset', 
                                default=kDefaultOutDS)                                                                        
        else:
            parser = super().get_parser(action)
        return parser


class SearchSpaceConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage configuration for hyperparameter search space'
        self.usage = 'hpogrid search_space <action> <config_name> <search_space_definition>'
        self.config_type = 'search_space'
        self.list_columns = ['Search Space Configuration']
        self.show_columns = ['Attribute', 'Value']  


    def get_parser(self, action=None):
        parser = self.get_base_parser()               
        if action in kConfigAction:     
            parser.add_argument('name', 
                help='Name given to the configuration file')  
            parser.add_argument('search_space', 
                help='A json decodable string defining the search space')  
        else:
            parser = super().get_parser(action)
        return parser

    def configure(self, args, action='create'):

        config = vars(args)
        config_name = config.pop('name', None)
        search_space = config.pop('search_space', None)

        try:
            search_space = json.loads(search_space)
        except JSONDecodeError:
            print('ERROR: Cannot to decode input string into json format. Please check your input.')
            return None

        if action == 'update':
            config_path = self.get_config_path(config_name)
            if not os.path.exists(config_path):
                raise FileNotFoundError('Search space file {} not found. Update aborted.'.format(config_path))
            old_serach_space = json.load(open(config_path))
            search_space = {**old_serach_space, **search_space}
        
        if validation.validate_search_space(search_space):
            self.save(search_space, config_name, action)
        return search_space

class ModelConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage configuration for machine learning model'
        self.usage = 'hpogrid model_config <action> <config_name> [<options>]'
        self.config_type = 'model'
        self.list_columns = ['Model Configuration']
        self.show_columns = ['Attribute', 'Value']  

    def get_parser(self, action=None):
        parser = self.get_base_parser()              
        if action in kConfigAction:  
            parser.add_argument('name', help= "Name given to the configuration file")            
            parser.add_argument('-s','--script', metavar='',
                help='Name of the training script where the function or class that defines'
                     ' the training model will be called to perform the training')
            parser.add_argument('-m','--model', metavar='',
                help='Name of the function or class that defines the training model')        
            parser.add_argument('-p','--param', metavar='',
                help='Extra parameters to be passed to the training model',
                default=kDefaultModelParam)
        else:
            parser = super().get_parser(action)
        return parser

    def process_config(self, config):
        super().process_config(config)

        if ('param' in config) and isinstance(config['param'],str):
            try:
                config['param'] = json.loads(config['param'])
            except JSONDecodeError:
                print('ERROR: Cannot decode input param into json format. Please check your input.')
                return None

        return config

class ProjectConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage a project for hyperparamter optimization'
        self.usage = 'hpogrid project <action> <project_name> [<options>]'
        self.config_type = 'project'
        self.list_columns = ['Project Title']
        self.show_columns = ['Attribute', 'Value']  
        self.project_config = {}


    def get_parser(self, action=None):
        parser = self.get_base_parser()           
        if action in kConfigAction:          
            parser.add_argument('name', help= "Name given the project")
            parser.add_argument('-p','--scripts_path', metavar='',
                help='Path to where the training scripts'
                ' (or the directory containing the training scripts) are located')
            parser.add_argument('-o','--hpo_config', metavar='',
                help='Name of the hpo configuration to use')
            parser.add_argument('-g','--grid_config', metavar='',
                help='Name of the grid configuration to use')
            parser.add_argument('-m','--model_config', metavar='',
                help='Name of the model configuration to use')
            parser.add_argument('-s','--search_space', metavar='',
                help='Name of the search space configuration to use')
        else:
            parser = super().get_parser(action)
        return parser

    def get_updated_config(self, config):
        return config

    def process_config(self, config):
        self.project_config = config

        print('INFO: Checking validity of input paths...')
        # check if path to training scripts exists
        if (config['scripts_path'] is not None):
            scripts_path = config['scripts_path']
            if not os.path.exists(scripts_path):
                print('ERROR: Path to training scripts {} does not exist.'
                       'Copy to project will be skipped.'.format(scripts_path))
                config['scripts_path'] = None
        else:
            print('INFO: Path to training scripts is not specified. Checking will be skipped.')

        config_type_map = {
            'hpo_config': 'hpo',
            'grid_config': 'grid',
            'model_config': 'model',
            'search_space': 'search_space'
        }

        # check if input configuration files exist
        for key in config_type_map:
            if (key in config) and (config[key] is not None):
                config_type = config_type_map[key]
                config_path = self.get_config_path(config[key], config_type)
                if not os.path.exists(config_path):
                    print('WARNING: Path to {} config {} does not exist.'.format(config_type, config_path))
                    config[key] = None
                else:
                    config[key] = config_path
            else:
                print('INFO: Path to {} config is not specified. Checking will be skipped.'.format(config_type_map[key]))
        print('INFO: Successfully validated input paths.')

        return config

    def get_project_path(self, proj_name):
        return self.get_config_path(proj_name, self.config_type, extension='')

    def save(self, config, name, action='create'):
        proj_name = name
        proj_path = self.get_project_path(proj_name)
        if (os.path.exists(proj_path)):
            if  action == 'create':
                print('ERROR: Project titled {} already exists. If you want to overwrite,'
                    ' use "recreate" or "update" action instead of "create".'.format(proj_name))
                return None
            elif action == 'recreate':
                backup_dir = self.get_config_path('backup', self.config_type, extension='')
                os.makedirs(backup_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                backup_proj_name = os.path.join(backup_dir, '{}_{}'.format(proj_name, timestamp))
                shutil.move(proj_path, backup_proj_name)
                print('INFO: Recreating project. Original project moved to backup directory {}.'.format(
                    backup_proj_name))
        # create project directories
        scripts_dir = os.path.join(proj_path, 'scripts')
        config_dir = os.path.join(proj_path, 'config')
        os.makedirs(proj_path, exist_ok=True)        
        os.makedirs(scripts_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)

        # copy input conifigurations
        print('INFO: Copying input configurations to the project directory')       
        if ('scripts_path' in config) and (config['scripts_path'] is not None):
            # copy contents of directory to project/scrsipts/
            if os.path.isdir(config['scripts_path']):
                dir_util.copy_tree(config['scripts_path'], scripts_dir)
            else:
                shutil.copy2(config['scripts_path'], scripts_dir)
            print('INFO: From {} copied training scripts to {}'.format(config['scripts_path'], scripts_dir))

        for key in kConfigList:
            if (key in config) and (config[key] is not None):
                dest = os.path.join(config_dir, '{}.json'.format(key))
                shutil.copy2(config[key], dest)
                print('INFO: Copied {} to {}'.format(config[key], dest))

        project_config = {}
        project_config_path = os.path.join(config_dir, kProjectConfigName)
        if os.path.exists(project_config_path):
            project_config = json.load(open(project_config_path))
        
        project_config = {**self.project_config, **project_config}
        with open(project_config_path,'w') as proj_config_file:
            json.dump(project_config, proj_config_file, indent=2)

    def get_config_list(self, expr=None):
        project_list = [ s for s in super().get_config_list() if s is not 'backup']
        return project_list

    def remove(self, name):
        proj_path = self.get_project_path(name)
        if os.path.exists(proj_path):
            print('WARNING: To avoid accidental deletion of important files. '
                'Please delete your project manually at:\n{}'.format(proj_path))
        else:
            print('ERROR: Cannot remove project in {}. Path does not exist.'.format(proj_path))

    def show(self, name):
        proj_path = self.get_project_path(name)
        config_path = os.path.join(proj_path, 'config', kProjectConfigName)
        if os.path.exists(config_path):
            with open(config_path,'r') as config_file:
                config = json.load(config_file)
            table = stylus.create_table(config.items(), self.show_columns)
            print(table)
        else:
            print('ERROR: Project {} does not exist.'.format(name))
import os
import sys
import json
import multiprocessing
from contextlib import contextmanager



from ray.tune.suggest.variant_generator import generate_variants,flatten_resolved_vars

try:
    from hpogrid.components.defaults import *  
except:
    raise ImportError('ERROR: Cannot import hpogrid module. Try source setupenv.sh first.')



def get_base_path():
	if kHPOGridEnvPath not in os.environ:
		raise KeyError('{} environment variable not set.'
			'Try source setupenv.sh first.'.format(kHPOGridEnvPath))
	return os.environ[kHPOGridEnvPath]

def set_script_paths(proj_name, undo=False):

	local_job_scripts_path = os.path.join(get_base_path(), 'project', proj_name, 'scripts')
	grid_job_scripts_path = os.path.join(get_base_path(), 'project', 'scripts')

	script_paths = [local_job_scripts_path, grid_job_scripts_path]

	for path in script_paths:
		if (path in sys.path) and (undo==True):
			sys.path.remove(path)
			os.environ["PYTHONPATH"].replace(path+":","")
		if (path not in sys.path) and (undo==False):
			sys.path.append(path)
			os.environ["PYTHONPATH"] = path + ":" + os.environ.get("PYTHONPATH", "")


def get_project_path(proj_name):
	if kHPOGridProjPath in os.environ:
		proj_path = os.environ[kHPOGridProjPath]
	else:
		base_path = get_base_path()
		proj_base_path = os.path.join(base_path, 'project')
		proj_path = os.path.join(proj_base_path, proj_name)
	if not os.path.exists(proj_path):
		raise FileNotFoundError('Project "{}" not found.'.format(proj_name))
	return proj_path

def get_config(proj_name, config_type):
	project_path = get_project_path(proj_name)
	config_name = kConfig2FileMap[config_type]
	confg_path = os.path.join(project_path, 'config', config_name)
	if not os.path.exists(confg_path):
		raise FileNotFoundError('Missing {} config file: {}'.format(
			config_type.replace('_',''), confg_path))
	with open(confg_path) as config_file:
		config = json.load(config_file)
	return config

def get_project_config(proj_name):
	return get_config(proj_name, config_type='project')

def get_hpo_config(proj_name):
	return get_config(proj_name, config_type='hpo')

def get_grid_config(proj_name):
	return get_config(proj_name, config_type='grid')	

def get_model_config(proj_name):
	return get_config(proj_name, config_type='model')	

def get_search_space_config(proj_name):
	return get_config(proj_name, config_type='search_space')	

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def generate_hparams(search_space, n_point=1):
	hparams = []
	for i in range(num_samples):
		for resolved_vars, _ in generate_variants(search_space):
			hparams.append(flatten_resolved_vars(resolved_vars))
	return hparams


def get_physical_devices(device_type='GPU'):
	import tensorflow as tf
	physical_devices = tf.config.list_physical_devices('GPU')
	return physical_devices

def get_n_gpu():
	physical_devices = get_physical_devices('GPU')
	return len(physical_devices)

def get_n_cpu():
	return multiprocessing.cpu_count()
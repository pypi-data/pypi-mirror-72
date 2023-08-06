import os
import sys
import copy
import json
import argparse
from pdb import set_trace

import pandas as pd
from tabulate import tabulate

try:
    from hpogrid.components.PandaTaskManager import PandaTaskManager
    from hpogrid.components.defaults import *
    from hpogrid.components.validation import validate_job_metadata
    from hpogrid.utils import stylus
except:
    raise ImportError('Cannot import hpogrid module. Try source setupenv.sh first.')

_h_test = ''

kDefaultExtraColumns = []
kSupportedExtraColumns = ['site', 'task_time_s', 'time_s', 'taskid']


class HPOReport():
    def __init__(self, data=None, verbose=True):
        self.verbose = verbose
        self.reset()
        if data:
            self.append(data)


    def reset(self):
        self.attrib = {}
        self.data = []

    def set_primary(self, data):
        self.attrib['title'] = data['title']
        self.attrib['hyperparameters'] = data['hyperparameters']
        self.attrib['metric'] = data['metric']
        self.attrib['mode'] = data['mode']
        if self.verbose:
            print('INFO: Setting up HPO report with the following attributes')
            print('Project Title   : {title} \n'
                  'Hyperparameters : {hyperparameters}\n'
                  'Metric          : {metric}\n'
                  'Mode            : {mode}'.format(**self.attrib))

    def check_consistency(self, data):
        if not validate_job_metadata(data):
            if self.verbose:
                print('ERROR: Invalid format for HPO result summary. '
                    'Result summary will be skipped')
            return False

        if not self.data:
            self.set_primary(data)

        if (data['title'] != self.attrib['title']):
            if self.verbose:
                print('INFO: Expecting HPO project name "{}" but "{}" is received. '
                    'Result summary will be skipped.')
            return False
        
        if (set(self.attrib['hyperparameters']) != set(data['hyperparameters'])):
            if self.verbose:
                print('INFO: Inconsistent hyperparameter space. '
                        'Result summary will be skipped.')
            return False

        if (self.attrib['metric'] != data['metric']) or (self.attrib['mode'] != data['mode']):
            if self.verbose:
                print('INFO: Inconsistent metric definition. '
                    'Result summary will be skipped.')
            return False
        return True

    def append(self, data, extras=None):
        if not self.check_consistency(data):
            return None
        keys_to_save = ['start_date_time', 'end_date_time', 'task_time_s', 'best_config', 'result']
        result = {key: data[key] for key in keys_to_save}
        if extras:
            for key in extras:
                result[key] = extras[key]
        self.data.append(result)

    def _check_data(self):
        if not self.data:
            print('ERROR: No HPO results to report.')
            return False
        return True

    @classmethod
    def from_json(cls, fname, verbose=True):
        with open(fname, 'r') as json_file:
            data = json.load(json_file)
        return cls(data, verbose)

    def merge_data(self, extra_columns=None, skip_time=True):
        merged_data = []
        for data in self.data:
            for index in data['result']:
                result = copy.deepcopy(data['result'][index])
                merged_data.append(result)
        if extra_columns:
            extras = []
            for data in self.data: 
                for index in data['result']:
                    extras.append({col: data[col] for col in extra_columns})
            for data, extra in zip(merged_data, extras):
                data.update(extra)
        if skip_time:
            for data in merged_data:
                data.pop('time_s')
        return merged_data

    def save_json(self, fname, indent=2):
        if not self._check_data():
            return None
        report = self.attrib
        report['jobs'] = self.data
        with open(fname, 'w') as file:
            json.dump(report, file, indent=indent)

    def to_json(self, fname, extra_columns=None, skip_time=True, indent=2):
        if not self._check_data():
            return None
        df = self.to_dataframe(extra_columns, skip_time)
        with open(fname, 'w') as output:
            json.dump(df.to_dict(), output, indent=indent)

    def to_dataframe(self, extra_columns=None, skip_time=True):
        if not self._check_data():
            return None
        data = self.merge_data(extra_columns, skip_time)
        df = pd.DataFrame(data)

        if self.attrib['mode'] == 'min':
            sort_ascending = True
        elif self.attrib['mode'] == 'max':
            sort_ascending = False

        df = df.sort_values(by=self.attrib['metric'] , ascending=sort_ascending).reset_index(drop=True)
        return df

    def to_mlflow(self, extra_columns=None, skip_time=True):
        if not self._check_data():
            return None
        from mlflow.tracking import MlflowClient
        client = MlflowClient()
        experiment_id = client.create_experiment(self.attrib['title'])
        hyperparameters = self.attrib['hyperparameters']
        metric = self.attrib['metric']
        merged_data = self.merge_data(extra_columns, skip_time)
        for data in merged_data:
            run = client.create_run(experiment_id)
            run_id = run.info.run_id
            for hp in hyperparameters:
                client.log_param(run_id, hp, data[hp])
            client.log_metric(run_id, metric, data[metric])
            client.set_terminated(run_id)
            
    def to_html(self, fname=None, extra_columns=None, skip_time=True):
        if not self._check_data():
            return None
        df = self.to_dataframe(extra_columns, skip_time)
        html_text = df.to_html()
        if fname:
            with open(fname, 'w') as outfile:
                outfile.write(html_text)
        return html_text

    def to_parallel_coordinate_plot(self, fname=None, extra_columns=None, skip_time=True):
        if not self._check_data():
            return None
        import hiplot as hip
        merged_data = self.merge_data(extra_columns, skip_time)
        html_text = hip.Experiment.from_iterable(merged_data).to_html()
        if fname:
            with open(file, 'w') as outfile:
                outfile.write(html_text)
        return html_text

    def to_csv(self, fname, extra_columns=None, skip_time=True):
        if not self._check_data():
            return None
        df = self.to_dataframe(extra_columns, skip_time)
        csv = df.to_csv(fname, encoding='utf-8')
        return csv

    def show(self, extra_columns=None, skip_time=True):
        if not self._check_data():
            return None
        df = self.to_dataframe(extra_columns, skip_time)
        print(tabulate(df, showindex=True, headers=df.columns, tablefmt="psql",stralign='center'))
'''
class HPOReporter():

    def __init__(self, summary=None, metric=None, mode=None):
        self.summary = summary
        self.metric = metric
        self.mode = mode

    @staticmethod
    def get_summary(data, extra=[]):
        summary = []
        if validate_job_metadata(data):
            raise RuntimeError('Invalid format for hpo result summary.')
        hparams = data['hyperparameters']
        metric = data['metric']  
        mode =  data['mode']  
        # gather results from different trials
        for index in data['result']:
            trial_result = {}
            for hp in hparams:
                trial_result[hp] = data['result'][index][hp]
            trial_result[metric] = data['result'][index][metric]
            if 'time_s' in extra:
                trial_result['time_s'] = data['result'][index]['time_total_s']
            summary.append(trial_result)
        return summary, metric, mode

    def display(self):
        if self.summary is None:
            print('WARNING: No summary to display. Action aborted.')
            return None
        df = self.to_dataframe()
        print(tabulate(df, showindex=True, headers=df.columns, tablefmt="psql",stralign='center'))

    @classmethod
    def from_data(cls, data, extra=[]):
        return cls(*HPOReporter.get_summary(data, extra))

    @classmethod
    def from_summary(cls, summary):
        return cls(summary)

    @classmethod
    def from_json(cls, file):
        with open(file) as json_file:
            summary = json.load(json_file)
        return cls(summary)            

    def to_dataframe(self):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to dataframe.')
            return None
        df = pd.DataFrame(self.summary)

        if (self.metric != None) and (self.mode != None):
            if self.mode == 'min':
                sort_ascending = True
            elif self.mode == 'max':
                sort_ascending = False
            else:
                raise RuntimeError('Invalid mode {} for the metric {}'.format(self.mode, self.metric))
            df = df.sort_values(by=[self.metric], ascending=sort_ascending).reset_index(drop=True)
        return df

    def to_json(self, file='hpo_summary.json'):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to json.')
            return None
        df = self.to_dataframe()
        with open(file, 'w') as output:
            json.dump(df.to_dict(), output)

    def to_html(self, file='hpo_result.html'):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to html.')
            return None
        df = self.to_dataframe()
        html_text = df.to_html()
        with open(file, 'w') as outfile:
            outfile.write(html_text)
        return html_text

    def to_parallel_coordinate_plot(self, file='hpo_result_parallel_coordinate_plot.html'):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to parallel coordinate plot.')
            return None

        import hiplot as hip
        html_text = hip.Experiment.from_iterable(self.summary).to_html()
        if file is not None:
            with open(file, 'w') as outfile:
                outfile.write(html_text)
        return html_text

    def to_csv(self, file='hpo_result.csv'):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to csv.')
            return None
        df = self.to_dataframe()
        csv = df.to_csv(file, encoding='utf-8')
        return csv
'''

class HPOTaskHandle(HPOReport):

    def __init__(self):
        super().__init__()
        self.taskmgr = PandaTaskManager()
        if len(sys.argv) > 1:
            self.run_parser()

    def get_parser(self, method=None):
        parser = argparse.ArgumentParser(description='Tool for managing HPO result',
                    formatter_class=argparse.RawDescriptionHelpFormatter)    
        parser.add_argument('proj_name', help='Name of the project')
        parser.add_argument('-l','--limit', type=int, default=1000,
            help='the maximum number of tasks to query')
        parser.add_argument('-d', '--days', type=int, default=30,
            help='filter tasks within the recent N days')
        parser.add_argument('-n', '--taskname',
            help='filter tasks by taskname (accept wildcards)')
        parser.add_argument('-r', '--range',
            help='filter tasks by jeditaskid range')
        parser.add_argument('-e', '--extra', nargs='+',
            default=kDefaultExtraColumns,
            help='extra data columns to be displayed and saved')
        parser.add_argument('-s', '--summary', action='store_true',
            help='save a complete hpo result summary as a json file')        
        parser.add_argument('-j', '--to_json', action='store_true',
            help='output result to a json file')
        parser.add_argument('-t', '--to_html', action='store_true',
            help='output result to an html file')
        parser.add_argument('-c', '--to_csv', action='store_true',
            help='output result to a csv file')
        parser.add_argument('-p', '--to_pcp', action='store_true',
            help='output result as a parallel coordinate plot')
        parser.add_argument('-f', '--to_mlflow', action='store_true',
            help='output result as an mlflow tracker directory')
        parser.add_argument('-o', '--outname', default='hpo_result',
            help='output file name (excluding extension)')
        return parser

    def run_parser(self):
        parser = self.get_parser()
        args = parser.parse_args(sys.argv[2:])
        self.show(args)

    def show(self, args):
        params = vars(args)
        params['status'] = 'done'
        params['metadata'] = True
        proj_name = params.pop('proj_name', '')
        outname = params.pop('outname', None)
        datasets = self.taskmgr.query_tasks(**params)
        # filter tasks by jetitaskid range
        if args.range is not None:
            datasets = self.taskmgr.filter_range(datasets, args.range)
        col = ['computingsite', 'jobs_metadata', 'jeditaskid', 'site']
        datasets = self.taskmgr.filter_datasets(datasets, col)

        extra_columns = args.extra or []
        for extra in args.extra:
            if not extra in kSupportedExtraColumns:
                raise ValueError('Unsupported extra column {}'.format(extra))

        skip_time = 'tims_s' not in extra_columns
        self.parse_datasets(datasets, proj_name, extra_columns=extra_columns)
        self.display(extra_columns, skip_time)

        if args.summary:
            self.save_json(outname+'_summary.json')
        if args.to_json:
            self.to_json(outname+'.json', extra_columns, skip_time)
        if args.to_html:
            self.to_html(outname+'.html', extra_columns, skip_time)
        if args.to_csv:
            self.to_csv(outname+'.csv', extra_columns, skip_time)    
        if args.to_pcp:
            self.to_parallel_coordinate_plot(outname+'_parallel_coordinate_plot.html', extra_columns, skip_time)   
        if args.to_mlflow:
            self.to_mlflow(extra_columns, skip_time)    

    def filter_invalid_datasets(self, datasets, proj_name):
        filtered_datasets = []
        for dataset in datasets:
            metadata = self.extract_metadata(dataset)
            if not metadata:
                continue
            if not validate_job_metadata(metadata):
                continue
            if metadata['title'] != proj_name:
                continue
            filtered_datasets.append(dataset)
        if len(filtered_datasets) == 0:
            print('INFO: No results found.')
            sys.exit(1)
        metrics = set([metadata['metric'] for data in filtered_datasets])
        if not len(metrics)==1 :
            raise RuntimeError('HPO results from different tasks consist of different metrics: {}'.format(metrics))
        hparams = [metadata['hyperparameters'] for data in filtered_datasets]
        if not all(hp == hparams[0] for hp in hparams):
            raise RuntimeError('HPO results from different tasks consist of different hyperparameter space')
        return filtered_datasets

    def extract_metadata(self, dataset):
        if 'jobs_metadata' in dataset:
            keys = list(dataset['jobs_metadata'].keys())
            if keys:
                return dataset['jobs_metadata'][keys[0]]
            else:
                return None
        else:
            return None

    def parse_datasets(self, datasets, proj_name, extra_columns=kDefaultExtraColumns):
        summary = []
        valid_datasets = self.filter_invalid_datasets(datasets, proj_name)

        metric =  None
        mode = None

        for dataset in valid_datasets:
            metadata = self.extract_metadata(dataset)
            extras = {}
            if 'taskid' in extra_columns:
                extras['taskid'] = dataset['jeditaskid']
            if 'site' in extra_columns:
                if 'computingsite' in dataset:
                    extras['site'] = dataset['computingsite']
                elif 'site' in dataset:
                    extras['site'] = dataset['site']
                else:
                    extras['site'] = ''
            self.append(metadata, extras)

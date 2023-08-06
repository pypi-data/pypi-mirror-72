kHPOGridEnvPath = 'HPOGRID_BASE_PATH'
kHPOGridProjPath = 'HPOGRID_PROJECT_PATH'

kProjectConfigName = 'project_config.json'
kModelConfigName = 'model_config.json'
kSearchSpaceConfigName = 'search_space.json'
kHPOConfigName = 'hpo_config.json'
kGridConfigName	 = 'grid_config.json'

kConfig2FileMap = {
	'project': kProjectConfigName,
	'hpo': kHPOConfigName,
	'search_space': kSearchSpaceConfigName,
	'model': kModelConfigName,
	'grid': kGridConfigName
}


kSearchAlgorithms = ['hyperopt', 'skopt', 'bohb', 'ax', 'tune', 'random', 'grid', 'bayesian', 'nevergrad']
kSchedulers = ['asynchyperband', 'bohbhyperband', 'pbt']
kMetricMode = ['min', 'max']


kDefaultSearchAlgorithm = 'random'
kDefaultMetric = 'accuracy'
kDefaultMode = 'max'
kDefaultScheduler = 'asynchyperband'
kDefaultLogDir = './log'
kDefaultTrials = 100
kDefaultStopping = '{"training_iteration": 1}'
kDefaultSchedulerParam = '{}'
kDefaultAlgorithmParam = '{"max_concurrent": 4}'
kDefaultModelParam = '{}'

kGPUGridSiteList = ['ANALY_MANC_GPU_TEST', 'ANALY_QMUL_GPU_TEST', 'ANALY_MWT2_GPU',
'ANALY_BNL_GPU_ARC', 'ANALY_INFN-T1_GPU']


kDefaultGridSite = 'ANALY_MANC_GPU_TEST'
kDefaultContainer = '/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:latest'
kDefaultContainer2 = '/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/clcheng/hyperparameter-optimization-on-the-grid:latest'
kDefaultContainer3 = 'docker://gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:latest'

kDefaultOutDS = 'user.${{RUCIO_ACCOUNT}}.hpogrid.{HPO_PROJECT_NAME}.out.$(date +%Y%m%d%H%M%S)'

kGridSiteMetadataFileName = 'userJobMetadata.json'

kHPOGridMetadataFormat = ['title', 'metric', 'mode', 'task_time_s', 'result', 'hyperparameters', 'best_config', 'start_date_time', 'end_date_time']

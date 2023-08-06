import os
import argparse
from pdb import set_trace
import tarfile

_help_test = 'test'

kDefaultDisk = 'UKI-NORTHGRID-MAN-HEP_SCRATCHDISK'
kDefaultDatasetName = 'user.${RUCIO_ACCOUNT}.hpo.test01.dataset'

def get_rucio_parser():
	
	parser = argparse.ArgumentParser()
	parser.add_argument('data_paths', nargs='+', help=_help_test)
	parser.add_argument('-n', '--name', help=_help_test, default=kDefaultDatasetName)
	parser.add_argument('-t', '--temp_dir', help=_help_test)
	parser.add_argument('-d','--disk', help=_help_test, default=kDefaultDisk)
	parser.add_argument('-s', '--save', action='store_true', help=_help_test, default=False)

	return parser


def upload_rucio(args):
	disk_name = args.disk
	dataset_name = args.name
	tarfile_name = args.name.replace('user.${RUCIO_ACCOUNT}.','')+'.tar.gz'
	tarfile_fullpath = os.path.join(args.temp_dir, tarfile_name)
	make_tarfile(args.data_paths, tarfile_fullpath)

	os.system('rucio add-dataset {}'.format(dataset_name))
	os.system('rucio upload {} --name {} --rse {}'.format(tarfile_fullpath, tarfile_name, disk_name))
	os.system('rucio attach {} user.${{RUCIO_ACCOUNT}}:{}'.format(dataset_name, tarfile_name))


def make_tarfile(source, outname):
    with tarfile.open(outname, "w:gz") as tar:
    	for src in source:
        	tar.add(src, arcname=os.path.basename(src))


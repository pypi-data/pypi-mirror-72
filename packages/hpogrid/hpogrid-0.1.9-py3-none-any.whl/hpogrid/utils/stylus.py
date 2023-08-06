"""
	Module for formatting tables, texts and figures used in hpogrid
"""
from tabulate import tabulate
import pandas as pd
from pdb import set_trace

kDefaultTableStyle = 'psql'
kDefaultStrAlign = 'left'

class ColorCode():
	RED = '\033[0;91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	BLUE = '\033[94m'
	MAGENTA = '\033[95m'
	CYAN = '\033[96m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	BLINK = '\033[5m'

def create_table(data, columns=None, indexed=True, transpose=False,
	tableformat=kDefaultTableStyle, stralign=kDefaultStrAlign):
	df = pd.DataFrame(data, columns=columns)
	if transpose:
		df = df.transpose()
	set_trace()
	table = tabulate(df, showindex=indexed, headers=df.columns, 
	    tablefmt=tableformat,
	    stralign=stralign)
	return table

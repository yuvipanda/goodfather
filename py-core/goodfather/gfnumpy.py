from numpy import *
from gfpersist import *

def load_recarray(filepath, select, headers, filter=None):
	records = []
	for p in read_streaming(filepath):
		if (not filter) or filter(p):
			records.append(select(p))
	
	if not records:
		return None
	else:
		return rec.fromrecords(records, names=headers)



from numpy import *
from gfpersist import *

def load_recarray(filepath, select, headers, filter=None):
	records = []
    pc = PersistanceContainer(filepath)
	for p in pc.read_all():
		if (not filter) or filter(p):
			records.append(select(p))
	
	if not records:
		return None
	else:
		return rec.fromrecords(records, names=headers)



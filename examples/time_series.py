from pathlib import Path
import json
from concurrent.futures import ProcessPoolExecutor as PPE

import smart_open

def pmap(arg):
	key,path = arg
	date_freq = {}
	print(path)
	fp = open(path)
	for line in fp:
		line = line.strip()	
		try:
			obj = json.loads(line)
		except: 
			continue
		datetime = obj['datetime']
		datetime = '/'.join(datetime.split('/')[0:2])
		#print(datetime, line)
		if len(datetime) != 5:
			continue
		if date_freq.get(datetime) is None:
			date_freq[datetime] = 0
		date_freq[datetime] += 1
	return date_freq

args = [(index,path) for index, path in enumerate(list(Path('../posts').glob('*.jsonl')))]

date_freq = {}
with PPE(max_workers=12) as exe:
	for _date_freq in exe.map(pmap, args):
		for date, freq in _date_freq.items():
			if date_freq.get(date) is None:
				date_freq[date] = 0
			date_freq[date] += freq
	
for date, freq in sorted(date_freq.items()):
	print(date, freq)

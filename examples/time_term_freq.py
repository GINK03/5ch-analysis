from pathlib import Path
import json
from concurrent.futures import ProcessPoolExecutor as PPE
import gzip
import smart_open

targets = ['orz', '尊師', '香具師', '笑 ', '初音ミク', '結月ゆかり', 'コードギアス', 'hshs', 'iphone','ソース', 'うｐ', '自宅警備員', 'ワンチャン', 'ステマ', '情弱', 'チラ裏', '今北産業', '禿同', 'w ', 'メシウマ' ,'まどかマギカ', 'まどマギ', 'ソシャゲ', 'FGO', '艦これ', 'エヴァ', 'ジワる', 'ナマポ', '(ry', 'ggrks', 'オワコン' ]
def pmap(arg):
	key,path = arg
	date_freq = {}
	print(path)
	fp = gzip.open(path, 'rt')
	try:
		for index, line in enumerate(fp):
			#if index >= 500000:
			#	break
			line = line.strip()	
			try:
				obj = json.loads(line)
			except: 
				continue
			datetime = obj['datetime']
			datetime = '20' + '/'.join(datetime.split('/')[0:2])
			post = obj['post'].lower()
			#print(datetime, line)
			if len(datetime) != 7:
				continue
			if date_freq.get(datetime) is None:
				date_freq[datetime] = [0,{}]

			date_freq[datetime][0] += 1
			for target in targets:
				if target in post:
					if date_freq[datetime][1].get(target) is None:
						date_freq[datetime][1][target] = 0
					date_freq[datetime][1][target] += 1
	except Exception as ex:
		print(ex)
		...
	#print(date_freq)
	return date_freq

args = [(index,path) for index, path in enumerate(list(Path('../posts').glob('*.jsonl')))]

date_freq = {}
with PPE(max_workers=12) as exe:
	for _date_freq in exe.map(pmap, args):
		for date, val in _date_freq.items():
			docs, target_freq = val
			if date_freq.get(date) is None:
				date_freq[date] = [0,{}]
			date_freq[date][0] += docs
			for target, freq in target_freq.items():
				if date_freq[date][1].get(target) is None:
					date_freq[date][1][target] = 0
				date_freq[date][1][target] += freq
#print(date_freq)

objs = []
for date, target_freq in sorted(date_freq.items()):
	total, target_freq = target_freq
	for target in target_freq.keys():
		target_freq[target] /= total
	target_freq['date'] = date
	objs.append(target_freq)
import pandas as pd

df = pd.DataFrame(objs).fillna(0.0)
df.to_csv('objs.csv', index=None)

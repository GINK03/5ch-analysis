import os
import glob
import gzip
import bs4, lxml
import concurrent.futures
import re
import hashlib
import json
from pathlib import Path
import chardet
def _map(arg):
	index, names = arg
	fp =gzip.open(f'posts/{index:02d}.jsonl.gz', 'wt')
	for name in names:
		print(name)
		html = gzip.decompress(open(name, 'rb').read()).decode()
		soup = bs4.BeautifulSoup(html, 'html5lib')
		for script in soup(["script", "style"]):
			script.extract()		# rip it out
		#for d in soup.find_all('div'):
		#		print(d)
		if soup.find('dl', {'class':'thread'}) is None:
			continue
		dts = soup.find('dl', {'class':'thread'}).find_all('dt')
		dds = soup.find('dl', {'class':'thread'}).find_all('dd')
		for dt,dd in zip(dts,dds):
			try:
				user = dt.find('b').text
				datetime = re.search(r'\d\d\/\d\d/\d\d', dt.text).group(0)
				post = re.sub(r'\n', ' ', dd.text)
				# 文字化けならファイルを削除してなかったことに
				if '�' in post or '�' in user:
					Path(name).unlink()
					break
				obj = {'user':user, 'datetime':datetime, 'post':post}
				ser = json.dumps(obj, ensure_ascii=False)
				fp.write(ser + '\n')
				#print(user, datetime, post)
			except Exception as ex:
				#print(ex)
				#print(dt.text)
				...
args = {}
for index,name in enumerate(glob.glob('htmls/*')):
	key = index%128
	if args.get(key) is None:
		args[key] = []
	args[key].append(name)
args = [(key, names) for key,names in args.items()]
#[_map(arg) for arg in args]
with concurrent.futures.ProcessPoolExecutor(max_workers=128) as exe:
	exe.map( _map, args)

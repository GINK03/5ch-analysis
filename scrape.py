import os
import math
import sys
import urllib.request, urllib.error, urllib.parse
import requests
import http.client
import ssl 
import re
import multiprocessing as mp
from socket import error as SocketError
import bs4
import concurrent.futures
import pickle
import os
import gzip
import random
import json
import re
import hashlib
import time
import gc
try:
	os.mkdir('htmls')
	os.mkdir('hrefs')
except:
	...
URL = 'http://lavender.5ch.net/kakolog_servers.html'
def html(arg): 
	key, urls = arg
	returns = set()
	random.shuffle(urls)
	for url in urls:
		try:
			print(key, url)
			save_name = 'htmls/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
			save_href = 'hrefs/' + hashlib.sha256(bytes(url,'utf8')).hexdigest()
			if os.path.exists(save_name) is True:
				continue
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
			try:
				r = requests.get(url, headers=headers, timeout=5)
			except Exception as e:
				continue
			r.encoding = r.apparent_encoding
			html = r.text
			try:
				open(save_name, 'wb').write( gzip.compress(bytes(html,'utf8')) )
			except OSError:
				continue
			soup = bs4.BeautifulSoup(html, 'html5lib')
		 
			hrefs = []
			for href in soup.find_all('a', href=True): 
				_url = href['href']
				try:
					if '//' == _url[0:2]:
						_url = 'https:' + _url
				except IndexError as e:
					continue
				try:
					if '/' == _url[0]:
						_url = '/'.join(url.split('/')[:3]) + _url
				except IndexError as e:
					continue
				if '5ch.net/' in _url:
					hrefs.append(_url)
			open(save_href, 'w').write( json.dumps(hrefs) )
			del soup, r
			gc.collect()
			[returns.add(href) for href in hrefs if os.path.exists('htmls/' + hashlib.sha256(bytes(href,'utf8')).hexdigest()) == False] 
		except Exception as ex:
			print(ex)
	return returns
def main():
	seed = URL
	urls = html(['seed', [seed]]) 
	
	try:
		print('try to load pickled urls')
		if '--resume' in sys.argv:
			urls = pickle.loads( gzip.decompress( open('urls.pkl.gz', 'rb').read() ) )
		if '--regen' in sys.argv:
			urls = pickle.loads( gzip.decompress( open('urls_regen.pkl.gz', 'rb').read() ) )

		print(urls)
		print('finished to load pickled urls')
	except FileNotFoundError as e:
		...
	
	while urls != set():
		nextUrls = set()
		# make args
		key_urls = {}
		for index, url in enumerate(urls):
			key = index%128
			if key_urls.get(key) is None:
				key_urls[key] = []
			key_urls[key].append(url)
		args = [(key,urls) for key,urls in key_urls.items()]
		with concurrent.futures.ProcessPoolExecutor(max_workers=128) as executor:
			for rurls in executor.map(html, args):
				for url in rurls:
					nextUrls.add(url)
					print('next_url', url)
		urls = nextUrls
		print(urls)
		open('urls.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(urls)) )
			 
main()

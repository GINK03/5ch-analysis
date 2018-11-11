import json
from pathlib import Path
import pickle, gzip

urls = set()
for path in Path('./hrefs/').glob('*'):
  for url in json.load(path.open()):
    urls.add(url)
open('urls_regen.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(urls)) )



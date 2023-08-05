Filoc File Locator
==================

This tiny library eases the saving and reading of files within a structured folder tree.

Example
-------

```python
from filoc import Filoc

loc = Filoc('/data/simid={simid:d}/epid={epid:d}/settings.json') 

path1 = loc.build_path(simid=0, epid=1)  # /data/simid=0/epid=1/settings.json
with open(path1, 'w') as f:
    f.write('Coucou')

path2 = loc.build_path(simid=0, epid=2)  # /data/simid=0/epid=2/settings.json
with open(path2, 'w') as f:
    f.write('Salut')

paths = loc.find_paths(simid=0)          # ['/data/simid=0/epid=1/settings.json', '/data/simid=0/epid=2/settings.json']

props = loc.extract_properties(paths[0]) # { 'simid': 0, 'epid': 1 }
```    

Install
-------

    pip install filoc

Syntax
------

The Filoc constructor accepts a file path/url, which will finally be interpreted by [fsspec](https://pypi.org/project/fsspec). 
That way, it is possible to access ftp, HDFS or any other file repository supported by fsspec. 
The path is at the same time a format string with named placeholder, which will be parsed by the [parse library](https://pypi.org/project/parse/).
Each placeholder defines a *property* associated to the files to save or retrieve.
 
    
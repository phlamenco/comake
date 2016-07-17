#encoding=utf-8
import codecs
import glob

import pytoml as toml


def Parse():
    with codecs.open('COMAKE', 'r', 'utf-8') as f:
        comake = toml.load(f)
    size = len(comake['output'])
    sources_set = set()
    headers_set = set()
    for i in range(size):
        comake['output'][i]['sources'] = _parsePath(comake['output'][i]['sources'])
        for source in comake['output'][i]['sources']:
            sources_set.add(source)
        for header in comake['output'][i]['headers']:
            headers_set.add(header)
        comake['output'][i]['headers'] = _parsePath(comake['output'][i]['headers'])
    comake['total_sources'] = list(sources_set)
    comake['total_headers'] = list(headers_set)
    return comake


def _validateComake(comake):
    # TODO add COMAKE format validation check
    pass


def _parsePath(line):
    res = []
    for token in line.split():
        if '*' in token:
            for path in glob.glob(token.strip()):
                res.append(path)
        else:
            res.append(token)
    return res
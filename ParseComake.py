#encoding=utf-8
import codecs
import glob

import pytoml as toml


def Parse():
    with codecs.open('COMAKE', 'r', 'utf-8') as f:
        comake = toml.load(f)
    size = len(comake['output'])

    total_sources = set()
    total_headers = set()
    for i in range(size):
        sources_set = _parsePath(comake['output'][i]['sources'])
        comake['output'][i]['sources'] = ' '.join(sources_set)
        headers_set = _parsePath(comake['output'][i]['headers'])
        comake['output'][i]['headers'] = ' '.join(headers_set)
        total_sources.update(sources_set)
        total_headers.update(headers_set)
    comake['total_sources'] = ' '.join(total_sources)
    comake['total_headers'] = ' '.join(total_headers)

    comake['include_path'] = ' '.join(['-I' + s for s in comake['include_path'].split()])
    comake['library_path'] = ' '.join(['-I' + s for s in comake['library_path'].split()])
    return comake


def _validateComake(comake):
    # TODO add COMAKE format validation check
    pass


def _parsePath(line):
    res = set()
    for token in line.split():
        if '*' in token:
            for path in glob.glob(token.strip()):
                res.add(path)
        else:
            res.add(token)
    return res
#encoding=utf-8

import codecs
import glob

import pytoml as toml


class ComakeParser:
    def __init__(self):
        self.comake = {}
        self.total_sources = set()
        self.total_headers = set()

    def Parse(self, path = 'COMAKE'):
        with codecs.open(path, 'r', 'utf-8') as f:
            comake = toml.load(f)
        size = len(comake['output'])

        for i in range(size):
            sources_set = _parsePath(comake['output'][i]['sources'])
            comake['output'][i]['sources'] = ' '.join(sources_set)
            headers_set = _parsePath(comake['output'][i]['headers'])
            comake['output'][i]['headers'] = ' '.join(headers_set)
            comake['output'][i]['a'] = comake['output'][i]['a'].strip()
            comake['output'][i]['so'] = comake['output'][i]['so'].strip()
            self.total_sources.update(sources_set)
            self.total_headers.update(headers_set)

        comake['total_sources'] = ' '.join(self.total_sources)
        comake['total_headers'] = ' '.join(self.total_headers)

        comake['include_path'] = ' '.join(['-I' + s for s in comake['include_path'].split()])
        comake['library_path'] = ' '.join(['-L' + s for s in comake['library_path'].split()])
        self.comake = comake
        if 'use_local_makefile' not in self.comake.keys():
            self.comake['use_local_makefile'] = 0

        return comake

    def getComake(self):
        return self.comake


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
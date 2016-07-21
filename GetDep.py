#encoding=utf-8
from threading import Thread

import git
from git import Repo
from urlparse import urlparse
from os import path, makedirs
from Queue import Queue, Empty

from ParseComake import ComakeParser


class DepFetcher:
    def __init__(self, comake):
        self.comake = comake
        self.root = comake['project_root']
        self.queue = Queue()
        self.dep_set = set()
        self.thread = None

    def worker(self):
        while True:
            try:
                dep = self.queue.get_nowait()
            except Empty:
                self.queue.task_done()
                break
            else:
                if dep["uri"] not in self.dep_set:
                    print "start fetch {0}".format(dep["uri"])
                    deps = self.getOneRepo(dep)
                    print "end fetch {}".format(dep["uri"])
                    self.dep_set.add(dep["uri"])
                    for d in deps:
                        self.queue.put(d)

    def getRepo(self):
        for dep in self.comake["dependency"]:
            if len(dep['uri']) == 0:
                continue
            self.queue.put(dep)
        self.thread = Thread(target=self.worker)
        self.thread.start()
        self.thread.join()
        self.queue.join()

    def getOneRepo(self, dep):
        if len(dep["uri"]) == 0:
            return
        url = urlparse(dep["uri"])
        if url == "file":
            pass
        else:
            local_path = [self.root, url.netloc]
            local_path.extend([x for x in url.path.split('/') if x])
            local_path[-1] = local_path[-1].rstrip('.git')
            repo_path = path.sep.join(local_path)

            if not path.isdir(repo_path):
                makedirs(repo_path)
            try:
                repo = Repo(repo_path)
            except git.exc.InvalidGitRepositoryError:
                repo = Repo.clone_from(dep['uri'], repo_path)
            finally:
                try:
                    if dep['tag'] is not "master":
                        tagRepo = repo.tags[dep['tag']]
                        repo.head.reference = tagRepo
                        repo.head.reset(index=True, working_tree=True)
                except IndexError:
                    # TODO pull master to get latest tag version
                    print "can't find tag '{0}' in repo {1}".format(dep['tag'], repo_path)

            comake_file = path.sep.join([repo_path, 'COMAKE'])
            if path.exists(comake_file):
                parser = ComakeParser(comake_file)
                return parser.Parse()["dependency"]
            else:
                print "can't find COMAKE in repo " + repo_path
                return {}





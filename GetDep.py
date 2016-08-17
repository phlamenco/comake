#encoding=utf-8
import os
from threading import Thread
from urlparse import urlparse, urljoin
import git
from git import Repo
from os import path, makedirs
from Queue import Queue, Empty
import urllib

from ParseComake import ComakeParser
from utils import RedIt, GreenIt, GetComake

REPO_URL = 'http://101.200.138.197:8080/comake/'

class DepFetcher:
    def __init__(self, comake):
        self.comake = comake
        self.root = os.getenv('COMAKEPATH')
        if not path.isdir(self.root):
            makedirs(self.root)
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
                    try:
                        deps = self.getOneRepo(dep)
                    except Exception as e:
                        print RedIt(e.message)
                    else:
                        for d in deps:
                            if len(d["uri"]) == 0:
                                continue
                            self.dep_set.add(d["uri"])
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
        repo = None
        if len(dep["uri"]) == 0:
            return {}
        url = urlparse(dep["uri"])
        if url == "file":
            #TODO
            return {}
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
                    print GreenIt("[NOTICE]{0} ({1}) {2} set success.".format(local_path[-1], dep['tag'], repo_path))
                except IndexError:
                    # TODO pull master to get latest tag version
                    print RedIt("[NOTICE]{0} ({1}) {2} set failed as {1} is invalid.".format(local_path[-1], dep['tag'], repo_path))

            if self.comake['use_local_makefile'] == 1:
                return []

            comake_file = path.sep.join([repo_path, 'COMAKE'])

            if not path.exists(comake_file):
                #c_file = local_path[1:]
                #c_file.append('COMAKE')
                c_file = local_path[-1]
                comake_url = urljoin(REPO_URL, c_file)
                print "start fetching " + comake_url
                GetComake(comake_url, comake_file)

            parser = ComakeParser()
            ret = parser.Parse(comake_file)["dependency"]
            print GreenIt("[NOTICE]{0} parsed success.".format(comake_file))
            return ret

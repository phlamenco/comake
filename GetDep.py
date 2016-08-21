#encoding=utf-8
import os
from threading import Thread
from urlparse import urlparse, urljoin
import git
import pickle
from git import Repo
from os import path, makedirs
from Queue import Queue, Empty, LifoQueue

import utils
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
        self.stack = LifoQueue()
        self.dep_set = set()
        self.thread = None
        self.stop = False
        self.work_num = 4
        self.dep_version = {}

    def set_work_num(self, num):
        self.work_num = num

    def worker(self):
        while True:
            try:
                dep = self.queue.get_nowait()
            except Empty:

                break
            else:
                repo = utils.GetPathFromUri(dep['uri'])
                if repo:
                    self.stack.put(repo)
                if dep["uri"] not in self.dep_set:
                    try:
                        self.dep_version[dep["uri"]] = dep
                        deps = self.getOneRepo(dep)
                    except Exception as e:
                        print RedIt(e.message)
                    else:
                        for d in deps:
                            if len(d["uri"]) == 0:
                                continue
                            self.dep_set.add(d["uri"])
                            self.queue.put(d)
                self.queue.task_done()

    def getRepo(self):
        for dep in self.comake["dependency"]:
            if len(dep['uri']) == 0:
                continue
            self.queue.put(dep)
        self.thread = Thread(target=self.worker)
        self.thread.start()
        self.thread.join()
        self.queue.join()

        duplicated_dep = set()
        dep_list = []
        while True:
            try:
                dep = self.stack.get_nowait()
            except Empty:
                break
            else:
                if dep not in duplicated_dep:
                    duplicated_dep.add(dep)
                    dep_list.append(dep)

        with open('.comake_deps', "wb") as f:
            pickle.dump(dep_list, f)

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
            if not local_path[-1].endswith('.git'):
                print RedIt("[error] wrong dependency uri format: {}".format(dep['uri']))
                return []
            local_path[-1] = local_path[-1][0:-4]
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
                    print GreenIt("[NOTICE] {0} ({1}) set success.".format(local_path[-1], dep['tag']))
                except IndexError:
                    # TODO pull master to get latest tag version
                    print RedIt("[NOTICE] {0} ({1}) {2} set failed as {1} is invalid.".format(local_path[-1], dep['tag'], repo_path))

            # if self.comake['use_local_makefile'] == 1:
            #     return []

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
            print GreenIt("[NOTICE] {0} ({1}) parsed success.".format(local_path[-1], dep['tag']))
            #self.stack.append(repo_path)
            return ret

#encoding=utf-8
import git
from git import Repo
from urlparse import urlparse
from os import path, makedirs

class DepFetcher:
    def __init__(self, comake):
        self.comake = comake
        self.root = comake['project_root']

    def getRepo(self):
        for dep in self.comake["dependency"]:
            if len(dep['uri']) == 0:
                continue
            self.getOneRepo(dep)

    def getOneRepo(self, dep):
        if len(dep["uri"]) == 0:
            return
        url = urlparse(dep["uri"])
        if url == "file":
            pass
        else:
            local_path = [self.root, url.netloc]
            local_path.extend([x for x in url.path.split('/')])
            local_path[-1].rstrip('.git')
            repo_path = path.sep.join(local_path)
            if not path.isdir(repo_path):
                makedirs(repo_path)
            try:
                repo = Repo(repo_path)
            except git.exc.InvalidGitRepositoryError:
                repo = Repo.clone_from(dep['uri'], repo_path)
            finally:
                try:
                    tagRepo = repo.tags[dep['tag']]
                except IndexError:
                    # TODO pull master to get latest tag version
                    print "can't find tag in repo " + repo_path
                else:
                    repo.head.reference = tagRepo
                    repo.head.reset(index=True, working_tree=True)






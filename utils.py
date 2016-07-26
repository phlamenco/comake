#encoding=utf-8

import sys


def RedIt(s):
    if(sys.__stderr__.isatty()):
        return "\033[1;31;40m%s\033[0m"%(s)
    else:
        return s


def GreenIt(s):
    if(sys.__stderr__.isatty()):
        return "\033[1;32;40m%s\033[0m"%(s)
    else:
        return s


def PullRepo(repo):
    # may have another way to do this
    repo.head.ref = repo.heads.master
    repo.head.reset(index=True, working_tree=True)
    res = repo.git.reset('--hard','origin/master')
    print GreenIt(res)
#encoding=utf-8
import codecs
import os
import sys

import subprocess
import urllib


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


def PullRepo(repo, path):
    # may have another way to do this
    repo.head.ref = repo.heads.master
    repo.head.reset(index=True, working_tree=True)
    repo.git.reset('--hard','origin/master')
    print GreenIt("[NOTICE]{0} ({1}) {2} set success.".format(path.split(os.path.sep)[-1], repo.head.ref, path))


def GetComake(comake_url, write_path):
    try:
        f = urllib.urlopen(comake_url)
        if f.getcode() != 200:
            print RedIt("[error]{} doesn't exist".format(comake_url))
            return
        res = f.read()
    except Exception as e:
        print RedIt("[error]{} get failed".format(comake_url))
    else:
        with codecs.open(write_path, "w", "utf-8") as ff:
            ff.write(res)
        print GreenIt("[NOTICE]{} get success".format(comake_url))


def CallCmd(cmd):
    p=subprocess.Popen('%s'%(cmd),
                       shell=True,
                       bufsize=0,
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    (out,err)=p.communicate()
    return (p.returncode,
            out,
            err)
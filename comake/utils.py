#encoding=utf-8
import codecs
import os
import sys

import subprocess
import traceback
import urllib
from urlparse import urlparse


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
    print GreenIt("[NOTICE] {0} ({1}) {2} set success.".format(path.split(os.path.sep)[-1], repo.head.ref, path))


def GetComake(comake_url, write_path):
    try:
        f = urllib.urlopen(comake_url)
        if f.getcode() != 200:
            print RedIt("[error] {} doesn't exist".format(comake_url))
            return
        res = f.read()
        print "[NOTICE] start writing COMAKE " + write_path
        with codecs.open(write_path, "w", "utf-8") as ff:
            ff.write(res.decode('utf-8'))
        print GreenIt("[NOTICE] get {} success".format(comake_url))
    except Exception as e:
        os.remove(write_path)
        traceback.print_exc()
        print RedIt("[error] {} get failed: ".format(comake_url))


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


def GetPathFromUri(uri):
    url = urlparse(uri)
    local_path = [os.getenv("COMAKEPATH"), url.netloc]
    local_path.extend([x for x in url.path.split('/') if x])
    if local_path[-1].endswith('.git'):
        local_path[-1] = local_path[-1][0:-4]
        return os.path.sep.join(local_path)
    else:
        print RedIt("[error] wrong dependency uri format: {}".format(uri))
        return None

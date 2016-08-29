import codecs
import getopt
import sys

import git
from git import Repo

import CompileDep
import ParseComake
import utils
from GenComake import GenComake
from GenMakefile import GenMakefile
import os

from GetDep import DepFetcher
from utils import RedIt

VERSION = "0.1.0"
COMAKE = "COMAKE"


def usage():
    return "usage sample"


def main():
    if not os.getenv("COMAKEPATH"):
        print "COMAKEPATH is empty. Please set it first"
        return
    parser = ParseComake.ComakeParser()
    default_parallel = 4
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hSUFBvdj:", ["help", "debug", "test"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    if "j" in [x for x, _ in opts]:
        default_parallel = int(opts['j'])
    if len(opts) == 0 and len(args) == 0:
        if not os.path.exists('COMAKE'):
            print "COMAKE doesn't exist"
            sys.exit()
        maker = GenMakefile()
        comake = parser.Parse()
        maker.setComake(comake)
        maker.generate()
    for o, a in opts:
        if o == "-v":
            print "comake version: " + VERSION
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--debug"):
            maker = GenMakefile()
            comake = parser.Parse()
            comake["opt_level"] = ""
            comake["cxx_compile_flags"] += " -g"
            comake["c_compile_flags"] += " -g"
            maker.setComake(comake)
            maker.generate()
        elif o == "-S":
            GenComake()
        elif o == "-F":
            parser.Parse()
            repo_paths = parser.getDepRepoPath()
            for repo_path, dep_uri in repo_paths.iteritems():
                try:
                    repo = Repo(repo_path)
                    utils.PullRepo(repo, repo_path)
                except git.exc.InvalidGitRepositoryError:
                    Repo.clone_from(dep_uri, repo_path)

        elif o == "-U":
            if not os.path.exists("COMAKE"):
                print RedIt("COMAKE doesn't exist")
                return
            comake = parser.Parse()
            fetcher = DepFetcher(comake)
            fetcher.getRepo()
        elif o == "-B":
            compiler = CompileDep.CompileDep()
            if compiler.init(default_parallel):
                compiler.start()
            else:
                print RedIt("[ERROR] please execute -U before -B")
        elif o == "--test":
            utils.CallCmd("echo helloworld")
        elif o == "-j":
            continue
        else:
            assert False, "invalid argument"

if __name__ == "__main__":
    main()

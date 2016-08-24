#encoding=utf-8
import Queue
import os

import pickle
from threading import Thread

import utils
from GenMakefile import GenMakefile
from ParseComake import ComakeParser


class CompileDep:
    def __init__(self):
        self.work_num = 1
        #self.root = os.getenv("COMAKEPATH")
        self.stack = None
        self.comake = None
        self.queue = Queue.Queue()

    def init(self, work_num = 4):
        if os.path.exists(".comake_deps"):
            with open('.comake_deps', 'rb') as f:
                self.stack = pickle.load(f)
                for s in self.stack:
                    self.queue.put(s)
                self.work_num = work_num
                return True
        return False

    def compile_worker(self):
        while True:
            try:
                path = self.queue.get_nowait()
            except Queue.Empty:
                break
            else:
                makeGenerator = GenMakefile()
                parser = ComakeParser()
                makeGenerator.setPath(path)
                makeGenerator.setComake(parser.Parse(os.sep.join([path, 'COMAKE'])))
                makeGenerator.generate()
                if makeGenerator.comake['use_local_makefile'] == 0:
                    res = utils.CallCmd("cd {0} && make -j4 -s".format(path))
                else:
                    res = utils.CallCmd("cd {0} && make -j4 -s -f Makefile.comake".format(path))

                if res[0] == 0:
                    print utils.GreenIt(res[1].strip())
                else:
                    print utils.RedIt(res[2])

    def start(self):
        thread_list = []
        for i in range(0, self.work_num):
            thread_list.append(Thread(target=self.compile_worker()))
            thread_list[i].start()
        for i in range(self.work_num):
            thread_list[i].join()

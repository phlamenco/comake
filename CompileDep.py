#encoding=utf-8
import Queue
import os


class CompileDep:
    def __init__(self, work_num):
        self.work_num = work_num
        self.root = os.getenv("COMAKEPATH")
        self.stack = Queue.LifoQueue()
        self.set = set()

    def travel_tree(self):
        pass

    def compile_worker(self):
        while True:
            pass

    def start(self):
        pass
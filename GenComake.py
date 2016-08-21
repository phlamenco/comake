#encoding=utf-8
from utils import RedIt

COMAKE = u"""project = "helloworld"

CC = "gcc"

CXX = "g++"

# C预处理参数
c_pre_flags = "-DGNU_SOURCE"

# C编译参数
c_compile_flags = "-Wall"

# C++编译参数
cxx_compile_flags = "-Wall -std=c++11"

# 优化等级,只对release生效
opt_level = "-O3"

# 链接参数
ld_flags = "-lpthread"

# 搜索头文件路径
include_path = "."

# 搜索库文件路径
library_path = "."

[[dependency]]
uri = "https://github.com/gflags/gflags.git"
tag = "v2.1.2"
[[dependency]]
uri = "https://github.com/google/glog.git"
tag = "v0.3.4"

[[output]]
sources = "*.cc *.cpp"
headers = "*.h"
libs = ""
bin = "helloworld"
so = ""
a = ""

[cmd]
before = ""
after = ""
"""
import os, codecs


def GenComake():
    if os.path.exists('COMAKE'):
        confirm = raw_input(RedIt("Overwrite an exist COMAKE file, y/[n]:"))
        if confirm.strip() != 'y':
            print "exit without generating COMAKE"
            return
    with codecs.open('COMAKE', 'w', 'utf-8') as f:
        f.write(COMAKE)

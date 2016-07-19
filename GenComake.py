#encoding=utf-8

COMAKE = u"""project_root = ""

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
include_path = ". ./include"

# 搜索库文件路径
library_path = ". ./lib"

[dependency]

[[output]]
sources = "*.cc *.cpp"
headers = "*.h"
libs = ""
bin = "helloworld"
so = ""
a = ""

[shell]
before = "mkdir -p output/include && mkdir -p output/lib && mkdir -p output/bin"
after = "cp -r bin/* output/bin && cp -r include/* output/include"
"""
import os, codecs


def GenComake():
    if os.path.exists('COMAKE'):
        confirm = raw_input("Overwrite an exist COMAKE file, y/[n]:")
        if confirm is not 'y':
            print "exit without generating COMAKE"
            return
    with codecs.open('COMAKE', 'w', 'utf-8') as f:
        f.write(COMAKE)

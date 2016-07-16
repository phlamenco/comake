#encoding=utf-8

COMAKE = u"""
project_root = ""

[configure]

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

[output]
sources = "*.cc *.cpp"
headers = "*.h"
libs =

[output.release]
bin = helloworld
[output.debug]
# 默认会加上-g,去掉所有的-O
so =
a =

"""
import os


def GenComake():
    if os.path.exists('COMAKE'):
        confirm = raw_input("Overwrite an exist COMAKE file, y/[n]:")
        if confirm is not 'y':
            print "exit without generating COMAKE"
            return
    with open('COMAKE', 'w') as f:
        f.write(COMAKE)

# comake
Comake - A compiling tool for c++ which handles dependency automatically.

## Introduction
Comake is a tool that aimed to be a handy c++ project organizer such as 'cargo' in rust or 'go get' in golang. It downloads and compiles 
denpendencies automatically and organizes the include paths and library paths in a uniform way to support your main c++ application, and
it also generate a custom Makefile for your application which makes you free of the pain of writing the Makefile.

Since comake simplifies the process of the dependencies' and your main application's build, it may lack some of customization and flexibility.

## Prerequisites
* c++11 or above
* python 2.7+ (python 3 may don't work)
* cmake 3.4.1+
* GNU autoconf & automake
* [GitPython](https://github.com/gitpython-developers/GitPython)
* [Jinja2](http://jinja.pocoo.org/)
* [pytoml](https://github.com/avakar/pytoml)

## Install
1. git clone this repo
2. add the root path of this repo to environment varible PYTHONPATH and PATH
3. set COMAKEPATH environment varible to your project path
4. type 'comake.py -v' to test whether installation is success or not

## Basic usage
Basically, comake is a command line tool which has several options to act different functions as follows:

* comake.py -S
it generates a COMAKE file which is the core configuration file of comake
* comake.py -U
it fetchs dependencies and switch them to specified version that is set in COMAKE file
* comake.py -B
it compiles all dependencies that is set in COMAKE file, the dependency version is not changed
* comake.py
it generate a Makefile according to the COMAKE file

## Set COMAKE file
A COMAKE file set many aspects of your project including project name, dependencies, compilers, compiling options and outputs and so on.
Take gflags's COMAKE as an example:
```
project = "gflags"

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
uri = ""
tag = ""

[[output]]
sources = ""
headers = ""
libs = ""
bin = ""
so = ""
a = ""

[cmd]
before = "if [ ! -d build ]; then mkdir build; fi && cd build && cmake .. && make"
after = "mv build/include/gflags/* output/include/gflags && mv build/lib/* output/lib"
```
some config option is obvious, we skip them. 
* include_path and library_path is the corresponding compiler options which don't contained in your dependencies. It should be your project's headers and library path
* dependency is an array that the element contains uri and tag. The uri is the git address and tag is git tag which indicates its version
* output is an array too. it's sources and headers should be your projct's c++ sources and headers, and libs, bin, so, a represents the outputing
library name, binary file name, dynamic library name and static library name
* cmd is a configuration for shell script execution before application building and after it's building.
As for exmaple 'gflag', [before] cmd uses cmake to build gflag dependency and [after] cmd copies output to specified path which will be written
into generated Makefile

## Note
The project is inspired by a product of Baidu Inc, but it has nothing relative to the product. The only relation between this product and that from
Baidu Inc is their name is identical, nothing else. The code is dependently written and open-sourced, pull request and advise are welcome.

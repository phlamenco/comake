#encoding=utf-8

import pytoml as toml
from jinja2 import Template

MAKEFILE = """
# define the C compiler to use
CC = {{CC}}

CXX = {{CXX}}

# define any compile-time flags
CFLAGS = {{c_pre_flags}} {{c_compile_flags}} {{opt_level}}

CPPFLAGS = {{c_pre_flags}} {{cxx_compile_flags}} {{opt_level}}

# define any directories containing header files other than /usr/include
#
INCLUDES = {{include_path}}

# define library paths in addition to /usr/lib
#   if I wanted to include libraries not in /usr/lib I'd specify
#   their path using -Lpath, something like:
LFLAGS = {{library_path}}

# define any libraries to link into executable:
#   if I want to link in libraries (libx.so or libx.a) I use the -llibname
#   option, something like (this will link in libmylib.so and libm.so:
LIBS = {{ld_flags}}

# define the C source files
#SRCS = {{sources}}

# define the C object files
#
# This uses Suffix Replacement within a macro:
#   $(name:string1=string2)
#         For each word in 'name' replace 'string1' with 'string2'
# Below we are replacing the suffix .c of all words in the macro SRCS
# with the .o suffix
#
#OBJS = $(SRCS:.cpp=.o)

{% for index, out in enumerate(output) %}
SRCS_{{index}} = {{out["sources"]}}
OBJS_{{index}} = $(SRCS:.cpp=.o)
BINS_{{index}} = {{out["bin"]}}
{% endfor %}

# define the executable file
MAIN = {{binary}}

#
# The following part of the makefile is generic; it can be used to
# build any executable just by changing the definitions above and by
# deleting dependencies appended to the file from 'make depend'
#

.PHONY: clean

all:    $(MAIN)
    @echo  Simple compiler named main has been compiled
all:

$(MAIN): $(OBJS)
    $(CC) $(CFLAGS) $(INCLUDES) -o $(MAIN) $(OBJS) $(LFLAGS) $(LIBS)

# this is a suffix replacement rule for building .o's from .c's
# it uses automatic variables $<: the name of the prerequisite of
# the rule(a .c file) and $@: the name of the target of the rule (a .o file)
# (see the gnu make manual section about automatic variables)
.c.o:
    $(CC) $(CFLAGS) $(INCLUDES) -c $<  -o $@

clean:
    $(RM) *.o *~ $(MAIN)

DEPDIR := .comake/dep
$(shell mkdir -p $(DEPDIR) >/dev/null)
DEPFLAGS = -MT $@ -MMD -MP -MF $(DEPDIR)/$*.Td

COMPILE.c = $(CC) $(DEPFLAGS) $(CFLAGS) $(CPPFLAGS) $(TARGET_ARCH) -c
COMPILE.cc = $(CXX) $(DEPFLAGS) $(CXXFLAGS) $(CPPFLAGS) $(TARGET_ARCH) -c
POSTCOMPILE = mv -f $(DEPDIR)/$*.Td $(DEPDIR)/$*.d

%.o : %.c
%.o : %.c $(DEPDIR)/%.d
    $(COMPILE.c) $(OUTPUT_OPTION) $<
    $(POSTCOMPILE)

%.o : %.cc
%.o : %.cc $(DEPDIR)/%.d
    $(COMPILE.cc) $(OUTPUT_OPTION) $<
    $(POSTCOMPILE)

%.o : %.cxx
%.o : %.cxx $(DEPDIR)/%.d
    $(COMPILE.cc) $(OUTPUT_OPTION) $<
    $(POSTCOMPILE)

$(DEPDIR)/%.d: ;
.PRECIOUS: $(DEPDIR)/%.d

#-include $(patsubst %,$(DEPDIR)/%.d,$(basename $(SRCS)))
-include $(patsubst %,$(DEPDIR)/%.d,$(basename {{total_sources}}))
"""
# TODO the total_sources may be a wrong use above
class GenMakefile:
    def __init__(self):
        self.comake = None
        self.template = Template(MAKEFILE)

    def setComake(self, comake):
        self.comake = comake

    def generate(self):
        self.template.render(self.comake)




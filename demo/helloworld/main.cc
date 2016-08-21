#include <iostream>
#include "gflags/gflags.h"
#include "gflags.h"
#include "glog.h"


int main(int argc, char** argv)
{
    gflags::ParseCommandLineFlags(&argc, &argv, true);
    std::cout << "hello world" << std::endl;
    gflags_test();
    glog();
    gflags::ShutDownCommandLineFlags();
}

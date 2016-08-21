#include "gflags/gflags.h"
#include <iostream>

DEFINE_string(test, "hello gflags", "test string");

void gflags_test() {
    std::cout << FLAGS_test << std::endl;
}

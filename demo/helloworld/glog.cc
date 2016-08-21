#include "glog/logging.h"

void glog() {
    google::InitGoogleLogging("hello.log");
    google::SetLogDestination(google::INFO, "."); 
    LOG(INFO) << "hello glog!";
}

cmake_minimum_required(VERSION 3.10)

project(test_package)

find_package(tinynet REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cc)

target_link_libraries(${PROJECT_NAME} tinynet::tinynet)

cmake_minimum_required(VERSION 3.10)

project(test_package)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

find_package(roomkit REQUIRED)

add_executable(${PROJECT_NAME} ../test_package/test_package.cc)

target_link_libraries(${PROJECT_NAME} roomkit::roomkit)

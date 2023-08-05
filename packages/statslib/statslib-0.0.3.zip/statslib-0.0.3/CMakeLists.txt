cmake_minimum_required (VERSION 3.0)
set(CMAKE_CXX_STANDARD 17)
project(statslib)

# option(USE_OPENMP "Compile with OpenMP" OFF)

set(DEPS_DIR "${CMAKE_CURRENT_LIST_DIR}/deps")

include_directories(SYSTEM "${DEPS_DIR}/gcem/include")
include_directories(SYSTEM "${DEPS_DIR}/stats/include")

add_subdirectory("${DEPS_DIR}/pybind11")
pybind11_add_module(statslib src/main.cpp src/dens.cpp src/rand.cpp src/prob.cpp src/quant.cpp)

# OpenMP support?
# find_package(OpenMP)
# if(OpenMP_FOUND AND USE_OPENMP)
#     target_link_libraries(statslib PRIVATE OpenMP::OpenMP_CXX)
#     #add_definitions(-DSTATS_USE_OPENMP)
# endif()

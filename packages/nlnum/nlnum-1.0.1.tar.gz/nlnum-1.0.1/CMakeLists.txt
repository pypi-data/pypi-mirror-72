cmake_minimum_required(VERSION 3.11...3.16)
if (${CMAKE_VERSION} VERSION_LESS 3.11)
    cmake_policy(VERSION ${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION})
endif ()

project(NLNum
        VERSION 1.0
        DESCRIPTION "Calculate Newell-Littlewood Numbers"
        LANGUAGES CXX)
cmake_minimum_required(VERSION 2.8.12)
project(NLNum)

# Optionally set things like CMAKE_CXX_STANDARD, CMAKE_POSITION_INDEPENDENT_CODE here

# In a real CMake application you wouldn't enable a debug
# build like this, but for our purposes it's just fine.
#
# This tells the compiler to not aggressively optimize and
# to include debugging information so that the debugger
# can properly read what's going on.
set(CMAKE_BUILD_TYPE Debug)
# Let's ensure -std=c++xx instead of -std=g++xx
set(CMAKE_CXX_EXTENSIONS OFF)
# Make the output folder `cmake-build-debug`.
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY cmake-build-debug/)
# Set the correct python version.
find_package(Python3 COMPONENTS Interpreter Development)
if(Python3_FOUND)
    message("python3 found" ${Python3_STDLIB})
else()
    message(FATAL_ERROR "python3 not found :(")
endif()
# Use OpenMP.
find_package(OpenMP)
if (NOT OpenMP_CXX_FOUND)
    message(FATAL_ERROR "OpenMP not found :(")
endif ()
# Let's nicely support folders in IDE's
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Allow code coverage.
if("{CMAKE_C_COMPILER_ID}" MATCHES "(Apple)?[Cc]lang"
    OR "${CMAKE_CXX_COMPILER_ID}" MATCHES "(Apple)?[Cc]lang")
  message("Building with llvm Code Coverage Tools")
  set(CMAKE_CXX_FLAGS "-fprofile-instr-generate -fcoverage-mapping")
elseif(CMAKE_COMPILER_IS_GNUCXX)
  message("Building with lcov Code Coverage Tools")
  set(CMAKE_CXX_FLAGS "--coverage")
endif()

# Set flags.
set(CMAKE_CXX_FLAGS "-Wall -Wextra -Wswitch -Wconversion -Wparentheses -Wfloat-equal -Wzero-as-null-pointer-constant -Wpedantic -pedantic -pedantic-errors")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-Ofast")

# FetchContent added in CMake 3.11, downloads during the configure step
include(FetchContent)

# FetchContent_MakeAvailable was not added until CMake 3.14
if(${CMAKE_VERSION} VERSION_LESS 3.14)
    include(cmake/add_FetchContent_MakeAvailable.cmake)
endif()

# Testing library. Header-only.
FetchContent_Declare(
    catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v2.11.1
)

# Pybind.
FetchContent_Declare(
    pybind
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.5.0
)

# LRCalc
FetchContent_Declare(
    lrcalc
    GIT_REPOSITORY https://github.com/iclue-summer-2020/lrcalc.git
    GIT_TAG        master
)

# Adds catch2 library.
FetchContent_GetProperties(catch2)
if(NOT catch2_POPULATED)
    FetchContent_Populate(catch2)
    # This is overkill since we only need a single file. Though it is a clean solution.
    add_library(catch2 INTERFACE)
    target_include_directories(catch2 INTERFACE ${catch2_SOURCE_DIR}/single_include)
endif()

# Adds pybind::pybind11
FetchContent_GetProperties(pybind)
if(NOT pybind_POPULATED)
    FetchContent_Populate(pybind)
    add_subdirectory(${pybind_SOURCE_DIR} ${pybind_BINARY_DIR})
endif()

# Adds lrcalc
FetchContent_GetProperties(lrcalc)
if(NOT lrcalc_POPULATED)
    FetchContent_Populate(lrcalc)
    add_subdirectory(${lrcalc_SOURCE_DIR} ${lrcalc_BINARY_DIR})
endif()

# The library code is here.
add_subdirectory(src)

# The tests are here.
add_subdirectory(tests)

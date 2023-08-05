# Note that headers are optional, and do not affect add_library, but they will not
# show up in IDEs unless they are listed in add_library.

# Optionally glob, but only for CMake 3.12 or later:
file(GLOB HEADER_LIST CONFIGURE_DEPENDS
        "${NLNum_SOURCE_DIR}/include/nlnum/*.h"
        "${NLNum_SOURCE_DIR}/include/nlnum/*.hpp")

file(GLOB SOURCE_LIST CONFIGURE_DEPENDS
        "${NLNum_SOURCE_DIR}/src/*.h"
        "${NLNum_SOURCE_DIR}/src/*.hpp"
        "${NLNum_SOURCE_DIR}/src/*.cc"
        "${NLNum_SOURCE_DIR}/src/*.cpp")

file(GLOB MODULE_FILES CONFIGURE_DEPENDS
        "${NLNum_SOURCE_DIR}/src/module.cc")

list(REMOVE_ITEM SOURCE_LIST ${MODULE_FILES})

add_library(nlnum-lib ${SOURCE_LIST} ${HEADER_LIST})

# We need this directory, and users of our library will need it too
target_include_directories(nlnum-lib PUBLIC "${NLNum_SOURCE_DIR}/include/")

target_link_libraries(nlnum-lib PUBLIC lrcalc PRIVATE ${Python3_LIBRARIES} OpenMP::OpenMP_CXX)

# All users of this library will need at least C++11
target_compile_features(nlnum-lib PUBLIC cxx_std_11)

# Enable fPIC.
set_property(TARGET nlnum-lib PROPERTY POSITION_INDEPENDENT_CODE ON)



#############################
# Create the pybind module. #
#############################

# Make an automatic library - will be static or dynamic based on user setting
pybind11_add_module(nlnum ${MODULE_FILES})

# We need this directory, and users of our library will need it too
# target_include_directories(nlnum-module PUBLIC ../include)

target_link_libraries(nlnum PRIVATE nlnum-lib pybind11)

# All users of this library will need at least C++11
target_compile_features(nlnum PUBLIC cxx_std_11)

set_property(TARGET nlnum PROPERTY POSITION_INDEPENDENT_CODE ON)

# IDEs should put the headers in a nice place
source_group(TREE "${PROJECT_SOURCE_DIR}/include" PREFIX "Header Files" FILES ${HEADER_LIST})

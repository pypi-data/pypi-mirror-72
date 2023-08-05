file(GLOB SOURCE_LIST CONFIGURE_DEPENDS
        "${NLNum_SOURCE_DIR}/tests/*.h"
        "${NLNum_SOURCE_DIR}/tests/*.hpp"
        "${NLNum_SOURCE_DIR}/tests/*.cc"
        "${NLNum_SOURCE_DIR}/tests/*.cpp")

# This target runs all of the tests.
# Make sure CATCH_CONFIG_MAIN is only defined in one test file.
add_executable(test-nlnum ${SOURCE_LIST})

# We're using C++17 in the test
target_compile_features(test-nlnum PRIVATE cxx_std_17)

# Should be linked to the main library, as well as the Catch2 testing library
target_link_libraries(test-nlnum PRIVATE nlnum-lib catch2 pybind11 lrcalc)

# If you register a test, then ctest and make test will run it.
# You can also run examples and check the output, as well.
add_test(NAME test-nlnum COMMAND test-nlnum) # Command can be a target

# Add folders
set_target_properties(test-nlnum PROPERTIES FOLDER iclue)

add_custom_command(
        TARGET test-nlnum
        PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -DSRC_DIR="${CMAKE_CURRENT_SOURCE_DIR}/data" -DDEST_DIR="${CMAKE_CURRENT_BINARY_DIR}/data" -P "${CMAKE_SOURCE_DIR}/cmake/configure_files.cmake"
)


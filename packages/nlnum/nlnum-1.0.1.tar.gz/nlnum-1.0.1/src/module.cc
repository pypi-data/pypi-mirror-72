// Copyright 2020 ICLUE @ UIUC. All rights reserved.

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <nlnum/nlnum.h>

namespace py = pybind11;

int add(int i, int j) {
  return i + j;
}

PYBIND11_MODULE(nlnum, m) {
  m.doc() = R"pbdoc(
    Pybind11 example plugin
    -----------------------
    .. currentmodule:: cmake_example
    .. autosummary::
       :toctree: _generate
       add
       subtract
    )pbdoc";

  m.def("add", &add, R"pbdoc(
            Add two numbers
            Some other explanation about the add function.
        )pbdoc");

  m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
            Subtract two numbers
            Some other explanation about the subtract function.
        )pbdoc");

  m.def("nlcoef_slow", &nlnum::nlcoef_slow, R"pbdoc(
    Compute a single Newell-Littlewood coefficient using Proposition 2.3.
    INPUT:
    - ``mu`` -- a partition (weakly decreasing list of non-negative integers).
    - ``nu`` -- a partition.
    - ``lambda`` -- a partition.
    EXAMPLES::
        python: from nlnum import nlcoef_slow
        python: nlcoef_slow([2,1], [2,1], [4, 2])
        1
  )pbdoc");

  m.def("nlcoef", &nlnum::nlcoef, R"pbdoc(
    Compute a single Newell-Littlewood coefficient using the definition (1.1).
    INPUT:
    - ``mu`` -- a partition (weakly decreasing list of non-negative integers).
    - ``nu`` -- a partition.
    - ``lambda`` -- a partition.
    EXAMPLES::
        python: from nlnum import nlcoef
        python: nlcoef([2,1], [2,1], [4, 2])
        1
  )pbdoc");

  m.def("lrcoef", &nlnum::lrcoef, R"pbdoc(
    Compute a single Littlewood-Richardson coefficient.
    Return the coefficient of ``outer`` in the product of the Schur
    functions indexed by ``inner1`` and ``inner2``.
    INPUT:
    - ``outer`` -- a partition (weakly decreasing list of non-negative integers).
    - ``inner1`` -- a partition.
    - ``inner2`` -- a partition.
    EXAMPLES::
        python: from nlnum import lrcoef
        python: lrcoef([3,2,1], [2,1], [2,1])
        2
        python: lrcoef([3,3], [2,1], [2,1])
        1
        python: lrcoef([2,1,1,1,1], [2,1], [2,1])
        0
  )pbdoc");

  #ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
  #else
  m.attr("__version__") = "dev";
  #endif
}

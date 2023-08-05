#ifndef _Pragma // MSVC
#define _Pragma __pragma
#endif
#include <pybind11/pybind11.h>

// ----------------
// Python interface
// ----------------

namespace py = pybind11;

void rand(py::module&);
void dens(py::module&);
void prob(py::module&);
void quant(py::module&);

PYBIND11_MODULE(statslib, m)
{
  m.doc() = "pybind11 wrapper for kthohr/statslib";
  dens(m);
  rand(m);
  prob(m);
  quant(m);
}

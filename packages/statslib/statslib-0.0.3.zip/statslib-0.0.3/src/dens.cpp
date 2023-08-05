#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "stats.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

void dens(py::module &m)
{
    m.def("dnorm", py::vectorize(&stats::dnorm<double, double, double>), 
          "x"_a, "mu"_a=0, "sigma"_a=1, "log"_a=false);
    m.def("dbern", py::vectorize(&stats::dbern<double>),
          "x"_a, "prob"_a, "log"_a=false);
    m.def("dbeta", py::vectorize(&stats::dbeta<double, double, double>),
          "x"_a, "a"_a, "b"_a, "log"_a=false);
    m.def("dbinom", py::vectorize(&stats::dbinom<double>),
          "x"_a, "n_trials"_a, "prob"_a, "log"_a=false);
    m.def("dcauchy", py::vectorize(&stats::dcauchy<double, double, double>),
          "x"_a, "mu"_a, "sigma"_a, "log"_a=false);
    m.def("dchisq", py::vectorize(&stats::dchisq<double, double>),
          "x"_a, "dof"_a, "log"_a=false);
    m.def("dexp", py::vectorize(&stats::dexp<double, double>),
          "x"_a, "rate"_a, "log"_a=false);
    m.def("df", py::vectorize(&stats::df<double, double, double>),
          "x"_a, "df1"_a, "df2"_a, "log"_a=false);
    m.def("dgamma", py::vectorize(&stats::dgamma<double, double, double>),
          "x"_a, "shape"_a, "scale"_a, "log"_a=false);
    m.def("dinvgamma", py::vectorize(&stats::dinvgamma<double, double, double>),
          "x"_a, "shape"_a, "scale"_a, "log"_a=false);
    m.def("dlaplace", py::vectorize(&stats::dlaplace<double, double, double>), 
          "x"_a, "mu"_a, "sigma"_a, "log"_a=false);
    m.def("dlnorm", py::vectorize(&stats::dlnorm<double, double, double>), 
          "x"_a, "mu"_a, "sigma"_a, "log"_a=false);
    m.def("dlogis", py::vectorize(&stats::dlogis<double, double, double>), 
          "x"_a, "mu"_a, "sigma"_a, "log"_a=false);
    m.def("dpois", py::vectorize(&stats::dpois<double>),
          "x"_a, "rate"_a, "log"_a=false);
    m.def("dt", py::vectorize(&stats::dt<double, double>),
          "x"_a, "dof"_a, "log"_a=false);
    m.def("dunif", py::vectorize(&stats::dunif<double, double, double>),
          "x"_a, "a"_a, "b"_a, "log"_a=false);
    m.def("dweibull", py::vectorize(&stats::dweibull<double, double, double>),
          "x"_a, "shape"_a, "scale"_a, "log"_a=false);
}
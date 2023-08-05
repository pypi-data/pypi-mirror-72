// cloned from dens.cpp-- just replaced d with p
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "stats.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

void prob(py::module &m)
{
    m.def("pnorm", py::vectorize(&stats::pnorm<double, double, double>), 
          "x"_a, "mu"_a=0, "sigma"_a=1, "log_p"_a=false);
    m.def("pbern", py::vectorize(&stats::pbern<double>),
          "x"_a, "prob"_a, "log_p"_a=false);
    m.def("pbeta", py::vectorize(&stats::pbeta<double, double, double>),
          "x"_a, "a"_a, "b"_a, "log_p"_a=false);
    m.def("pbinom", py::vectorize(&stats::pbinom<double>),
          "x"_a, "n_trials"_a, "prob"_a, "log_p"_a=false);
    m.def("pcauchy", py::vectorize(&stats::pcauchy<double, double, double>),
          "x"_a, "mu"_a, "sigma"_a, "log_p"_a=false);
    m.def("pchisq", py::vectorize(&stats::pchisq<double, double>),
          "x"_a, "dof"_a, "log_p"_a=false);
    m.def("pexp", py::vectorize(&stats::pexp<double, double>),
          "x"_a, "rate"_a, "log_p"_a=false);
    m.def("pf", py::vectorize(&stats::pf<double, double, double>),
          "x"_a, "df1"_a, "df2"_a, "log_p"_a=false);
    m.def("pgamma", py::vectorize(&stats::pgamma<double, double, double>),
          "x"_a, "shape"_a, "scale"_a, "log_p"_a=false);
    m.def("pinvgamma", py::vectorize(&stats::pinvgamma<double, double, double>),
          "x"_a, "shape"_a, "scale"_a, "log_p"_a=false);
    m.def("plaplace", py::vectorize(&stats::plaplace<double, double, double>), 
          "x"_a, "mu"_a, "sigma"_a, "log_p"_a=false);
    m.def("plnorm", py::vectorize(&stats::plnorm<double, double, double>), 
          "x"_a, "mu"_a, "sigma"_a, "log_p"_a=false);
    m.def("plogis", py::vectorize(&stats::plogis<double, double, double>), 
          "x"_a, "mu"_a, "sigma"_a, "log_p"_a=false);
    m.def("ppois", py::vectorize(&stats::ppois<double>),
          "x"_a, "rate"_a, "log_p"_a=false);
    m.def("pt", py::vectorize(&stats::pt<double, double>),
          "x"_a, "dof"_a, "log_p"_a=false);
    m.def("punif", py::vectorize(&stats::punif<double, double, double>),
          "x"_a, "a"_a, "b"_a, "log_p"_a=false);
    m.def("pweibull", py::vectorize(&stats::pweibull<double, double, double>),
          "x"_a, "shape"_a, "scale"_a, "log_p"_a=false);
}

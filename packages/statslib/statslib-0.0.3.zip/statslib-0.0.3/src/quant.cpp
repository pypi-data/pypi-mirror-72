#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "stats.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

void quant(py::module &m)
{
    m.def("qnorm", py::vectorize(&stats::qnorm<double, double, double>), 
          "p"_a, "mu"_a=0, "sigma"_a=1);
    m.def("qbern", py::vectorize(&stats::qbern<double, double>),
          "p"_a, "prob"_a);
    m.def("qbeta", py::vectorize(&stats::qbeta<double, double, double>),
          "p"_a, "a"_a, "b"_a);
    m.def("qbinom", py::vectorize(&stats::qbinom<double, double>),
          "p"_a, "n_trials"_a, "prob"_a);
    m.def("qcauchy", py::vectorize(&stats::qcauchy<double, double, double>),
          "p"_a, "mu"_a, "sigma"_a);
    m.def("qchisq", py::vectorize(&stats::qchisq<double, double>),
          "p"_a, "dof"_a);
    m.def("qexp", py::vectorize(&stats::qexp<double, double>),
          "p"_a, "rate"_a);
    m.def("qf", py::vectorize(&stats::qf<double, double, double>),
          "p"_a, "df1"_a, "df2"_a);
    m.def("qgamma", py::vectorize(&stats::qgamma<double, double, double>),
          "p"_a, "shape"_a, "scale"_a);
    m.def("qinvgamma", py::vectorize(&stats::qinvgamma<double, double, double>),
          "p"_a, "shape"_a, "scale"_a);
    m.def("qlaplace", py::vectorize(&stats::qlaplace<double, double, double>), 
          "p"_a, "mu"_a, "sigma"_a);
    m.def("qlnorm", py::vectorize(&stats::qlnorm<double, double, double>), 
          "p"_a, "mu"_a, "sigma"_a);
    m.def("qlogis", py::vectorize(&stats::qlogis<double, double, double>), 
          "p"_a, "mu"_a, "sigma"_a);
    m.def("qpois", py::vectorize(&stats::qpois<double, double>),
          "p"_a, "rate"_a);
    m.def("qt", py::vectorize(&stats::qt<double, double>),
          "p"_a, "dof"_a);
    m.def("qunif", py::vectorize(&stats::qunif<double, double, double>),
          "p"_a, "a"_a, "b"_a);
    m.def("qweibull", py::vectorize(&stats::qweibull<double, double, double>),
          "p"_a, "shape"_a, "scale"_a);
}
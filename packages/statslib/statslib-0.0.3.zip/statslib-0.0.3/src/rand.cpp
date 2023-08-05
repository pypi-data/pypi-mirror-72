#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "stats.hpp"

namespace py = pybind11;
using namespace pybind11::literals;
using engine_t = stats::rand_engine_t;
using llint_t = stats::llint_t;

template <auto Func, typename T1, typename T2, typename S>
struct Vectorize2
{
      auto operator()(const T1 a, const T2 b, const S size,
                      stats::rand_engine_t &engine) const
      {
            auto out_array = py::array_t<T2, py::array::c_style>(size);
            const auto info = out_array.request();
            T2 *r = static_cast<T2 *>(info.ptr);
            for (int i = 0; i < info.size; i++)
            {
                  r[i] = Func(a, b, engine);
            }
            return out_array;
      }
};

template <auto Func, typename T1, typename S>
struct Vectorize1
{
      auto operator()(const T1 a, const S size, stats::rand_engine_t &engine) const
      {
            auto out_array = py::array_t<T1, py::array::c_style>(size);
            const auto info = out_array.request();
            T1 *r = static_cast<T1 *>(info.ptr);
            for (int i = 0; i < info.size; i++)
            {
                  r[i] = Func(a, engine);
            }
            return out_array;
      }
};

constexpr auto rnorm = py::overload_cast<double, double, engine_t &>(&stats::rnorm<double, double>);
constexpr Vectorize2<rnorm, double, double, std::vector<size_t>&> vrnorm;
constexpr Vectorize2<rnorm, double, double, size_t> srnorm;

constexpr auto rbern = py::overload_cast<double, engine_t &>(&stats::rbern<double>);
constexpr Vectorize1<rbern, double, std::vector<size_t>&> vrbern;
constexpr Vectorize1<rbern, double, size_t> srbern;

constexpr auto rbeta = py::overload_cast<double, double, engine_t &>(&stats::rbeta<double, double>);
constexpr Vectorize2<rbeta, double, double, std::vector<size_t>&> vrbeta;
constexpr Vectorize2<rbeta, double, double, size_t> srbeta;

constexpr auto rbinom = py::overload_cast<llint_t, double, engine_t &>(&stats::rbinom<double>);
constexpr Vectorize2<rbinom, llint_t, double, std::vector<size_t>&> vrbinom;
constexpr Vectorize2<rbinom, llint_t, double, size_t> srbinom;

constexpr auto rcauchy = py::overload_cast<double, double, engine_t &>(&stats::rcauchy<double, double>);
constexpr Vectorize2<rcauchy, double, double, std::vector<size_t>&> vrcauchy;
constexpr Vectorize2<rcauchy, double, double, size_t> srcauchy;

constexpr auto rchisq = py::overload_cast<double, engine_t &>(&stats::rchisq<double>);
constexpr Vectorize1<rchisq, double, std::vector<size_t>&> vrchisq;
constexpr Vectorize1<rchisq, double, size_t> srchisq;

constexpr auto rexp = py::overload_cast<double, engine_t &>(&stats::rexp<double>);
constexpr Vectorize1<rexp, double, std::vector<size_t>&> vrexp;
constexpr Vectorize1<rexp, double, size_t> srexp;

constexpr auto rf = py::overload_cast<double, double, engine_t &>(&stats::rf<double, double>);
constexpr Vectorize2<rf, double, double, std::vector<size_t>&> vrf;
constexpr Vectorize2<rf, double, double, size_t> srf;

constexpr auto rgamma = py::overload_cast<double, double, engine_t &>(&stats::rgamma<double, double>);
constexpr Vectorize2<rgamma, double, double, std::vector<size_t>&> vrgamma;
constexpr Vectorize2<rgamma, double, double, size_t> srgamma;

constexpr auto rinvgamma = py::overload_cast<double, double, engine_t &>(&stats::rinvgamma<double, double>);
constexpr Vectorize2<rinvgamma, double, double, std::vector<size_t>&> vrinvgamma;
constexpr Vectorize2<rinvgamma, double, double, size_t> srinvgamma;

constexpr auto rlaplace = py::overload_cast<double, double, engine_t &>(&stats::rlaplace<double, double>);
constexpr Vectorize2<rlaplace, double, double, std::vector<size_t>&> vrlaplace;
constexpr Vectorize2<rlaplace, double, double, size_t> srlaplace;

constexpr auto rlnorm = py::overload_cast<double, double, engine_t &>(&stats::rlnorm<double, double>);
constexpr Vectorize2<rlnorm, double, double, std::vector<size_t>&> vrlnorm;
constexpr Vectorize2<rlnorm, double, double, size_t> srlnorm;

constexpr auto rlogis = py::overload_cast<double, double, engine_t &>(&stats::rlogis<double, double>);
constexpr Vectorize2<rlogis, double, double, std::vector<size_t>&> vrlogis;
constexpr Vectorize2<rlogis, double, double, size_t> srlogis;

constexpr auto rpois = py::overload_cast<double, engine_t &>(&stats::rpois<double>);
constexpr Vectorize1<rpois, double, std::vector<size_t>&> vrpois;
constexpr Vectorize1<rpois, double, size_t> srpois;

constexpr auto rt = py::overload_cast<double, engine_t &>(&stats::rt<double>);
constexpr Vectorize1<rt, double, std::vector<size_t>&> vrt;
constexpr Vectorize1<rt, double, size_t> srt;

constexpr auto runif = py::overload_cast<double, double, engine_t &>(&stats::runif<double, double>);
constexpr Vectorize2<runif, double, double, std::vector<size_t>&> vrunif;
constexpr Vectorize2<runif, double, double, size_t> srunif;

constexpr auto rweibull = py::overload_cast<double, double, engine_t &>(&stats::rweibull<double, double>);
constexpr Vectorize2<rweibull, double, double, std::vector<size_t>&> vrweibull;
constexpr Vectorize2<rweibull, double, double, size_t> srweibull;

void rand(py::module &m)
{
      py::class_<engine_t>(m, "Engine").def(py::init<int>());
      py::object engine = m.attr("Engine")(1); // default engine

      m.def("rnorm", rnorm, "mu"_a = 0, "sigma"_a = 1, "engine"_a = engine);
      m.def("rnorm", vrnorm, "mu"_a = 0, "sigma"_a = 1, "size"_a, "engine"_a = engine);
      m.def("rnorm", srnorm, "mu"_a = 0, "sigma"_a = 1, "size"_a, "engine"_a = engine);
      m.def("rbern", rbern, "prob"_a, "engine"_a = engine);
      m.def("rbern", vrbern, "prob"_a, "size"_a, "engine"_a = engine);
      m.def("rbern", srbern, "prob"_a, "size"_a, "engine"_a = engine);
      m.def("rbeta", rbeta, "a"_a, "b"_a, "engine"_a = engine);
      m.def("rbeta", vrbeta, "a"_a, "b"_a, "size"_a, "engine"_a = engine);
      m.def("rbeta", srbeta, "a"_a, "b"_a, "size"_a, "engine"_a = engine);
      m.def("rbinom", rbinom, "n_trials"_a, "prob"_a, "engine"_a = engine);
      m.def("rbinom", vrbinom, "n_trials"_a, "prob"_a, "size"_a, "engine"_a = engine);
      m.def("rbinom", srbinom, "n_trials"_a, "prob"_a, "size"_a, "engine"_a = engine);
      m.def("rcauchy", rcauchy, "mu"_a, "sigma"_a, "engine"_a = engine);
      m.def("rcauchy", vrcauchy, "mu"_a, "sigma"_a, "size"_a, "engine"_a = engine);
      m.def("rcauchy", srcauchy, "mu"_a, "sigma"_a, "size"_a, "engine"_a = engine);
      m.def("rchisq", rchisq, "dof"_a, "engine"_a = engine);
      m.def("rchisq", vrchisq, "dof"_a, "size"_a, "engine"_a = engine);
      m.def("rchisq", srchisq, "dof"_a, "size"_a, "engine"_a = engine);
      m.def("rexp", rexp, "rate"_a, "engine"_a = engine);
      m.def("rexp", vrexp, "rate"_a, "size"_a, "engine"_a = engine);
      m.def("rexp", srexp, "rate"_a, "size"_a, "engine"_a = engine);
      m.def("rf", rf, "df1"_a, "df2"_a, "engine"_a = engine);
      m.def("rf", vrf, "df1"_a, "df2"_a, "size"_a, "engine"_a = engine);
      m.def("rf", srf, "df1"_a, "df2"_a, "size"_a, "engine"_a = engine);
      m.def("rgamma", rgamma, "shape"_a, "scale"_a, "engine"_a = engine);
      m.def("rgamma", vrgamma, "shape"_a, "scale"_a, "size"_a, "engine"_a = engine);
      m.def("rgamma", srgamma, "shape"_a, "scale"_a, "size"_a, "engine"_a = engine);
      m.def("rinvgamma", rinvgamma, "shape"_a, "scale"_a, "engine"_a = engine);
      m.def("rinvgamma", vrinvgamma, "shape"_a, "scale"_a, "size"_a, "engine"_a = engine);
      m.def("rinvgamma", srinvgamma, "shape"_a, "scale"_a, "size"_a, "engine"_a = engine);
      m.def("rlaplace", rlaplace, "mu"_a, "sigma"_a, "engine"_a = engine);
      m.def("rlaplace", vrlaplace, "mu"_a, "sigma"_a, "size"_a, "engine"_a = engine);
      m.def("rlaplace", srlaplace, "mu"_a, "sigma"_a, "size"_a, "engine"_a = engine);
      m.def("rlnorm", rlnorm, "mu"_a, "sigma"_a, "engine"_a = engine);
      m.def("rlnorm", vrlnorm, "mu"_a, "sigma"_a, "size"_a, "engine"_a = engine);
      m.def("rlnorm", srlnorm, "mu"_a, "sigma"_a, "size"_a, "engine"_a = engine);
      m.def("rlogis", rlogis, "mu"_a, "sigma"_a, "engine"_a = engine);
      m.def("rlogis", vrlogis, "mu"_a, "sigma"_a, "size"_a, "engine"_a = engine);
      m.def("rlogis", srlogis, "mu"_a, "sigma"_a, "size"_a, "engine"_a = engine);
      m.def("rpois", rpois, "rate"_a, "engine"_a = engine);
      m.def("rpois", vrpois, "rate"_a, "size"_a, "engine"_a = engine);
      m.def("rpois", srpois, "rate"_a, "size"_a, "engine"_a = engine);
      m.def("rt", rt, "dof"_a, "engine"_a = engine);
      m.def("rt", vrt, "dof"_a, "size"_a, "engine"_a = engine);
      m.def("rt", srt, "dof"_a, "size"_a, "engine"_a = engine);
      m.def("runif", runif, "a"_a, "b"_a, "engine"_a = engine);
      m.def("runif", vrunif, "a"_a, "b"_a, "size"_a, "engine"_a = engine);
      m.def("runif", srunif, "a"_a, "b"_a, "size"_a, "engine"_a = engine);
      m.def("rweibull", rweibull, "shape"_a, "scale"_a, "engine"_a = engine);
      m.def("rweibull", vrweibull, "shape"_a, "scale"_a, "size"_a, "engine"_a = engine);
      m.def("rweibull", srweibull, "shape"_a, "scale"_a, "size"_a, "engine"_a = engine);
}

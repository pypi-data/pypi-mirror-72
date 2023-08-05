#include <pybind11/pybind11.h>

namespace py = pybind11;

int add(int i, int j) { // implementation code
    return i + j;
}

struct Pet {
    Pet(const std::string &name) : name(name) { }
    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }

    std::string name;
};
/*
    BELOW:
    The PYBIND11_MODULE() macro creates a function that is called when an import statement is used in python.
    The module name (example) is given as the first macro argument (it should not be in quotes)
    The second argument (m) defines a variable of type py::module which is the main interface for creating bindings
    The method module::def() generates binding code that exposes the add() function to python.

    class_ creates bindings for a cpp class or struct style data structure.
    init() is a convinience function that takes the types of a constructor's params as template arguments,
        and wraps the correpsonding constructor.

*/
PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function which adds two numbers",
            py::arg("i"), py::arg("j"));

    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &>())
        .def("setName", &Pet::setName)
        .def("getName", &Pet::getName);
}
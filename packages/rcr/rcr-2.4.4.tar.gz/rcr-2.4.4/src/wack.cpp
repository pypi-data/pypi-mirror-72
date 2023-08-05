

FunctionalForm getFunctionalFormObject(py::args args, py::kwargs kwargs){ // this one works for sure
    FunctionalForm FFobj;

    std::vector <double> ydata = py::cast <std::vector <double> >(args[2]);
    std::vector <double> guess = py::cast <std::vector <double> >(args[4]);

    const double DEFAULT_TOL = 1e-6;

    double tol = DEFAULT_TOL;

    std::function <double(double, std::vector <double> )> f; 
    std::vector <double> xdata; 
    std::vector < std::function <double(double, std::vector <double>)> > model_partials;
    
    f = py::cast< std::function <double(double, std::vector <double> )> >(args[0]);
    xdata = py::cast< std::vector <double> >(args[1]);
    model_partials = py::cast < std::vector < std::function <double(double, std::vector <double>)> > > (args[3]);

    FFobj = FunctionalForm(f, xdata, ydata, model_partials, tol, guess);

    return FFobj;
}
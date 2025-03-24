#pragma once

#include <vector>
#include <cstddef> // size_t

class Regression{
private:
    std::vector<double> x_values;
    std::vector<double> y_values;
    double m_slope;
    double m_intercept;
    size_t m_max_data_points;

public:

    explicit Regression(size_t max_data_points); // explicit : forbid translations

    void addDataPoint(double x, double y);

    void calculate();

    double predict(double x) const;

    double Regression::getSlope() const;

    double Regression::getIntercept() const;

    void Regression::setMaxDataPoints(size_t max);

    void clear();
};
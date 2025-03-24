#include "regression.h"
#include <stdexcept>

Regression::Regression(size_t max_data_points)
    : m_slope(0), m_intercept(0), m_max_data_points(max_data_points)
{
}

void Regression::addDataPoint(const double x, const double y)
{
    x_values.push_back(x);
    y_values.push_back(y);

    if (x_values.size() > m_max_data_points)
    {
        x_values.erase(x_values.begin());
        y_values.erase(y_values.begin());
    }
}

void Regression::calculate()
{
    const size_t n = x_values.size();
    if (n < 2)
    {
        throw std::runtime_error("Not enough data points for regression");
    }

    double sum_x = 0, sum_y = 0, sum_xy = 0, sum_xx = 0;

    for (size_t i = 0; i < n; i++)
    {
        sum_x += x_values[i];
        sum_y += y_values[i];
        sum_xy += x_values[i] * y_values[i];
        sum_xx += x_values[i] * x_values[i];
    }

    const double denominator = n * sum_xx - sum_x * sum_x;
    if (denominator == 0) {
        throw std::runtime_error("Cannot compute regression for vertical line");
    }

    m_slope = (n * sum_xy - sum_x * sum_y) / denominator;
    m_intercept = (sum_y - m_slope * sum_x) / n;
}

double Regression::predict(const double x) const
{
    return m_slope * x + m_intercept;
}

double Regression::getSlope() const
{
    return m_slope;
}

double Regression::getIntercept() const
{
    return m_intercept;
}

void Regression::setMaxDataPoints(size_t max) {
    m_max_data_points = max;
    if (x_values.size() > m_max_data_points) {
        x_values.erase(x_values.begin(), x_values.end() - m_max_data_points);
        y_values.erase(y_values.begin(), y_values.end() - m_max_data_points);
    }
}

void Regression::clear() {
    x_values.clear();
    y_values.clear();
    m_slope = 0;
    m_intercept = 0;
}
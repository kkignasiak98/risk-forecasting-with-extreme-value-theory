import pandas as pd
from scipy.stats import genpareto, norm
import math
def calculate_var_evt(location, scale, shape, n, nu, significance):
    """
    Calculate the extreme value theory (EVT) estimate of Value at Risk (VaR).

    Parameters:
        location (float): The location parameter of the Pareto distribution.
        scale (float): The scale parameter of the Pareto distribution.
        shape (float): The shape parameter of the Pareto distribution.
        n (int): The number of observations.
        nu (int): The number of extreme events to consider.
        significance (float): The significance level for the VaR calculation.

    Returns:
        float: The EVT estimate of Value at Risk.

    """

    var_evt = location + (scale / shape) * ( math.pow(significance * n  / nu,-shape) - 1)
    return var_evt

def calculate_var(values, windows_size, threshold, significance):
    """
    Calculate the Value at Risk (VaR) using the extreme value theory.

    Parameters:
        values (pd.Series): The series of values.
        windows_size (int): The size of the window.
        threshold (int): The threshold for selecting extreme events.
        significance (float): The significance level for the VaR calculation.

    Returns:
        float: The extreme value theory estimate of Value at Risk.

    Note:
        - The Pareto distribution is used to model the extreme events.
        - The VaR is calculated as a positive number by convention.
    """

    small = values.nsmallest(threshold) *(-1)
    shape, location, scale = genpareto.fit(small)

    var = calculate_var_evt(location=location,scale= scale, shape = shape, n = windows_size, nu = threshold, significance=significance)
    return var

def in_sample_prediction(values:pd.core.series.Series, windows_size:int, threshold:float, significance:float):
    """
    Generate the in-sample prediction for Value at Risk (VaR) using extreme value theory.

    Parameters:
        values (pd.core.series.Series): The series of values.
        windows_size (int): The size of the rolling window.
        threshold (float): The threshold for selecting extreme events.
        significance (float): The significance level for the VaR calculation.

    Returns:
        pd.core.series.Series: The in-sample prediction series.

    Note:
        - The Value at Risk is calculated as a positive number by convention.
    """

    in_sample_prediction = values.rolling(windows_size).apply(lambda x: calculate_var(x, windows_size, threshold, significance))
    in_sample_prediction = in_sample_prediction.apply(lambda x: x * -1) # Value at Risk is calculated as a positive number by convention
    return in_sample_prediction
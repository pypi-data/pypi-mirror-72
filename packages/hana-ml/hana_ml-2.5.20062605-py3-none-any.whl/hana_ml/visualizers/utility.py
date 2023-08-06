"""
This module contains binning and sampling method for ploting large dataset.
"""
from hana_ml.dataframe import quotename
from hana_ml.algorithms.pal.preprocessing import Sampling
#pylint: disable=line-too-long, invalid-name, too-many-arguments, too-many-locals

def binning_2d(data, x, y, x_bins, y_bins, rounding_precision=3, range_info=False, order=False):
    """
    Returns DataFrame with banding key.

    Parameters
    ----------
    data : DataFrame
        DataFrame to use for the plot.
    x : str
        Column to be plotted on the x axis.
    y : str
        Column to be plotted on the y axis.
    x_bins : int
        Number of x axis bins to create based on the value of column.
    y_bins : int
        Number of y axis bins to create based on the value of column.
    rounding_precision : int, optional
        The rounding precision for bin size.
    range_info : bool, optional
        If True, caculate and return the detailed range info.

        Defaults to False.
    order : bool, optional
        If True, sort the returned dataframe by x and y.

        Defaults to False.

    Returns
    -------
    DataFrame
        DataFrame with banding key.
    """
    conn_context = data.connection_context
    x = quotename(x)
    y = quotename(y)
    x_max = "SELECT MAX({}) FROM ({})".format(x, data.select_statement)
    x_maxi = conn_context.sql(x_max).collect().values[0][0]
    x_min = "SELECT MIN({}) FROM ({})".format(x, data.select_statement)
    x_mini = conn_context.sql(x_min).collect().values[0][0]
    x_diff = x_maxi-x_mini
    x_bin_size = float(x_diff)/float(x_bins)
    y_max = "SELECT MAX({}) FROM ({})".format(y, data.select_statement)
    y_maxi = conn_context.sql(y_max).collect().values[0][0]
    y_min = "SELECT MIN({}) FROM ({})".format(y, data.select_statement)
    y_mini = conn_context.sql(y_min).collect().values[0][0]
    y_diff = y_maxi-y_mini
    y_bin_size = float(y_diff)/float(y_bins)
    query = "SELECT {0},".format(x)
    query += " {0},".format(y)
    if range_info:
        query += " ROUND(FLOOR({0}/{1})*{1}, {2}) AS X_L,".format(x, x_bin_size, rounding_precision)
        query += " ROUND(((FLOOR({0}/{1})*{1})+{1}), {2}) AS X_R,".format(x, x_bin_size, rounding_precision)
        query += " ROUND(FLOOR({0}/{1})*{1}, {2}) AS Y_L,".format(y, y_bin_size, rounding_precision)
        query += " ROUND(((FLOOR({0}/{1})*{1})+{1}), {2}) AS Y_R,".format(y, y_bin_size, rounding_precision)
    query += " '[' || ROUND(FLOOR({0}/{1})*{1}, {2}) || ', ' || ".format(x, x_bin_size, rounding_precision)
    query += "ROUND(((FLOOR({0}/{1})*{1})+{1}), {2})  || ')' AS BANDING_X,".format(x, x_bin_size, rounding_precision)
    query += " '[' || ROUND(FLOOR({0}/{1})*{1}, {2}) || ', ' || ".format(y, y_bin_size, rounding_precision)
    query += "ROUND(((FLOOR({0}/{1})*{1})+{1}), {2}) || ')'".format(y, y_bin_size, rounding_precision)
    query += " AS BANDING_Y FROM ({})".format(data.select_statement)
    query2 = "SELECT {}, {},".format(x, y)
    if range_info:
        query2 += "X_L, X_R, Y_L, Y_R,"
    query2 += " BANDING_X, BANDING_Y FROM ({})".format(query)
    if order:
        query2 += " ORDER BY {}, {}".format(x, y)
    bin_data = conn_context.sql(query2)
    return bin_data

def sampling_for_scatter_plot(data, x, y, x_bins, y_bins, percentage, rounding_precision=3):
    """
    Returns a 2D stratfied sampled DataFrame.

    Parameters
    ----------
    data : DataFrame
        DataFrame to use for the plot.
    x : str
        Column to be plotted on the x axis.
    y : str
        Column to be plotted on the y axis.
    x_bins : int
        Number of x axis bins to create based on the value of column.
    y_bins : int
        Number of y axis bins to create based on the value of column.
    percentage : double
        Sampling percentage.
    rounding_precision : int, optional
        The rounding precision for bin size.

    Returns
    -------
    DataFrame
        Returns a 2D stratifed sampled DataFrame.
    """
    bin_data = binning_2d(data, x, y, x_bins, y_bins, rounding_precision, False, False)
    samp = Sampling(method='stratified_without_replacement', percentage=percentage)
    return samp.fit_transform(data=bin_data, features=['BANDING_X', 'BANDING_Y'])

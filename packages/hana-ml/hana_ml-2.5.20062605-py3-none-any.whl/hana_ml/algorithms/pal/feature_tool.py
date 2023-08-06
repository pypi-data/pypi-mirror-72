"""
This module supports to generate additional features for HANA DataFrame.
"""
from hana_ml import dataframe
from hana_ml.dataframe import quotename

#pylint: disable=invalid-name
#pylint: disable=eval-used
#pylint: disable=unused-variable
#pylint: disable=line-too-long

def generate_feature(data,
                     target,
                     group_by=None,
                     agg_func=None,
                     trans_func=None):
    """
    Add additional features to the existing dataframe using agg_func and trans_func.

    Parameters
    ----------
    data : DataFrame
        SAP HANA DataFrame.
    target : str
        The column in data to be feature engineered.
    group_by: str
        The column in data for group by when performing agg_func.
    agg_func : str
        HANA aggeration operations. SUM, COUNT, MIN, MAX, ...
    trans_func : str
        HANA transformation operations. MONTH, YEAR, LAG, ...

    Returns
    -------

    DataFrame
        SAP HANA DataFrame with new features.

    Examples
    --------

    >>> feat_df = generate_feature(data, "ds", agg_func="max", group_by="y")
    """
    view_sql = data.select_statement
    if agg_func is not None:
        if group_by is None:
            raise Exception("group_by cannot be None!")
        agg_keyword = '"{}({})"'.format(agg_func, target)
        agg_sql = "SELECT {}, {}({}) {} FROM ({}) GROUP BY {}".format(quotename(group_by),\
             agg_func, quotename(target), agg_keyword, view_sql, quotename(group_by))
        view_sql = "SELECT T1.*, T2.{} FROM ({}) T1 INNER JOIN ({}) T2 ON T1.{}=T2.{}"\
            .format(agg_keyword, view_sql, agg_sql, quotename(group_by), quotename(group_by))
    if trans_func is not None:
        view_sql = "SELECT *, {}({}) FROM ({})".format(trans_func, quotename(target), view_sql)
    return dataframe.DataFrame(data.connection_context, view_sql)

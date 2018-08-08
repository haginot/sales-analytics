import pandas as pd

ROW_ORDER = 'ROW_ORDER'

ROW_PRODUCT = 'ROW_PRODUCT'

def get_schema_type(data):
    """
    Parameters
    ----------
    data : DataFrame

    Returns
    -------
    string
        The DataFrame schema type
    """
    row_count = data.shape[0]

    # TODO : this method require ordered datetime and subject user column name
    grouped_count = data.groupby(['datetime_order', 'subject_user']).size().values.size

    if grouped_count < row_count:
        return ROW_PRODUCT
    else:
        return ROW_ORDER


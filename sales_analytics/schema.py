import pandas as pd
import itertools
from collections import defaultdict
from .base import get_vartype

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

def get_minimal_keys(df):

    total_count = len(df)

    vartypes = {col: get_vartype(s) for col, s in df.iteritems()}
    """
    {'cat_type': 'CAT',
     'datetime_order': 'DATE',
     'subject_user': 'CAT',
     'object_product': 'CAT',
     ...
     'target': 'NUM'}
    """

    # group by vartype
    vartype_cols = defaultdict(list)
    for col in vartypes:
        vartype_cols[vartypes[col]].append(col)
    """
    defaultdict(list,
            {'CAT': ['cat_parent', 'cat_product', 'cat_type', 'subject_user',
              'object_product', 'cat_payment', 'cat_group', 'cat_postal', 'cat_prefecture'],
             'DATE': ['datetime_order'],
             'NUM': ['num_amount', 'num_point', 'num_subscription', 'target'],
             'BOOL': ['bin_repeat', 'bin_mobile']})
    """

    # more statistical way to detect column mean
    value_counts = pd.DataFrame({col: s.value_counts(dropna=True).agg(['count','std']).astype('int').values for col, s in df.iteritems()}, index=['count', 'std']).transpose()

    # choose atomic field
    # datetime field
    dtcol = vartype_cols['DATE'][0]

    # subject_user
    """
    ユーザを識別する値のため、カテゴリカルデータを対象としている。
    value_counts で求めた各カラムのユニーク値の数と、各値の行数の標準偏差から
    ユニーク値がデータ行全体に対して、10%以上であること、標準偏差が10以下であることを条件としている
    """
    cand = list(set(value_counts[(value_counts['count'] / len(df) > 0.1) & (value_counts['std'] < 10)].index).intersection(set(vartype_cols['CAT'])))

    a = {t: df.groupby([t[0], t[1]]).size().reset_index().subject_user.size / df[t[0]].unique().size for t in list(itertools.combinations(cand, 2))}
    b = {t: df.groupby([t[0], t[1]]).size().reset_index().subject_user.size / df[t[0]].unique().size for t in [tuple(reversed(t)) for t in list(itertools.combinations(cand, 2))]}
    a.update(b)


    return a

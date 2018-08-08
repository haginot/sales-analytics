import pandas as pd
from .schema import get_minimal_keys

class SalesAnalyze(object):
    file = None

    def __init__(self, df, **kwargs):
        # TODO : create minimal table contains required column
        # so you should detect columns order datetime, subject user or object product and so.

        # parse date columns
        for col, s in df.iteritems():
            if s.dtype == 'object':
                try:
                    df[col] = pd.to_datetime(s)
                except ValueError:
                    pass

        minimal_df = get_minimal_keys(df)

        # DEBUG : test minimal table schema

        pass

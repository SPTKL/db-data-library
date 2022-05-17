import tempfile

import pandas as pd


def df_to_tempfile(df: pd.DataFrame, encode_utf_8=False) -> str:
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(f, index=False)
    return f.name

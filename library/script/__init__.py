import tempfile

import pandas as pd


def df_to_tempfile(df: pd.DataFrame, encode_utf_8=False) -> str:
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    if encode_utf_8:
        df.to_csv(f, encoding="utf-8", index=False)
    df.to_csv(f, index=False)
    return f.name

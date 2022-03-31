import pandas as pd

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        df = pd.read_csv("dob_now_applications.csv", encoding="Windows-1252")
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df, encode_utf_8=True)
        return local_path



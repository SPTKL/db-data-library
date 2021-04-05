import pandas as pd

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        url = "https://maps.nyc.gov/prek/data/pka/pka.csv"
        df = pd.read_csv(url, encoding="unicode_escape", dtype="str")
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

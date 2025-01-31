import pandas as pd
import requests

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        df = pd.read_excel("https://adip.faa.gov/publishedAirports/all-airport-data.xlsx", sheet_name="Airports")
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

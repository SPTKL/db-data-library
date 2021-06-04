from zipfile import ZipFile

import pandas as pd
import requests

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def version(self):
        return self.config["dataset"]["version"]

    def ingest(self) -> pd.DataFrame:

        url = f"https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/pad{self.version}.zip"
        resp = requests.get(url)
        with ZipFile(file_name, "r") as zip:
            zip.extract(f"pad{self.version}/bobaadr.txt")
            df = pd.read_csv("bobaadr.txt", dtype=str)
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

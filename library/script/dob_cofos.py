import pandas as pd

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def version(self):
        return self.config["dataset"]["version"]

    @property
    def previous_version(self) -> str:
        return self.config["dataset"]["info"]["previous_version"]

    def ingest(self) -> pd.DataFrame:
        df = pd.read_csv("dob_cofos.csv", dtype=str)
        df.insert(0, "v", self.version)
        return df

    def previous(self) -> pd.DataFrame:
        url = f"https://nyc3.digitaloceanspaces.com/edm-recipes/datasets/dob_cofos/{self.previous_version}/dob_cofos.csv"
        return pd.read_csv(url, dtype=str)

    def runner(self) -> str:
        new = self.ingest()
        previous = self.previous()
        new.columns = previous.columns
        df = pd.concat([previous, new])
        df = df.drop_duplicates()
        local_path = df_to_tempfile(df)
        return local_path

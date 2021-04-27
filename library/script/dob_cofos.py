import pandas as pd

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    @property
    def version(self):
        return self.config['dataset']['version']

    def ingest(self) -> pd.DataFrame:
        df = pd.read_csv('dob_cofos.csv', dtype=str)
        df['v'] = self.version
        return df
    
    def current(self) -> pd.DataFrame:
        url = 'https://nyc3.digitaloceanspaces.com/edm-recipes/datasets/dob_cofos/latest/dob_cofos.csv'
        return pd.read_csv(url, dtype=str)

    def runner(self) -> str:
        df = pd.concat([self.ingest(), self.current()])
        df = df.drop_duplicates()
        local_path = df_to_tempfile(df)
        return local_path
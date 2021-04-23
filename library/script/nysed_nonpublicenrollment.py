import json

import pandas as pd
import requests

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def version(self):
        return self.config['dataset']['version']
        
    def ingest(self) -> pd.DataFrame:
        df = pd.read_excel(f'http://www.p12.nysed.gov/irs/statistics/nonpublic/{self.version}_NonPub_Enrollment_Grade.xlsx')
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

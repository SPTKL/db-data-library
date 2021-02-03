import json

import pandas as pd
import requests

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.Dataframe:
        url = "https://www.bklynlibrary.org/locations/json"
        response = requests.get(url)
        content = json.loads(response.content)
        data = []
        for i in content["locations"]:
            data.append(i["data"])
        df = pd.DataFrame.from_dict(data, orient="columns")
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

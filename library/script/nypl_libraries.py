import json

import pandas as pd
import requests

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        url = "https://refinery.nypl.org/api/nypl/locations/v1.0/locations"
        content = requests.get(url).content
        records = json.loads(content)["locations"]
        data = []
        for i in records:
            parsed = dict(
                lon=str(i["geolocation"]["coordinates"][0]),
                lat=str(i["geolocation"]["coordinates"][1]),
                name=i["name"],
                zipcode=i["postal_code"],
                address=i["street_address"],
                locality=i["locality"],
                region=i["region"],
            )
            data.append(parsed)
        df = pd.DataFrame.from_dict(data, orient="columns")
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

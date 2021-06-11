import os

import requests


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def metadata(self):
        return requests.get("https://data.cityofnewyork.us/api/views/nqwf-w8eh").json()

    @property
    def uid(self):
        return self.metadata["childViews"][0]

    @property
    def url(self):
        return f"https://data.cityofnewyork.us/api/geospatial/{self.uid}\?method=\export\&format=\Shapefile"

    def runner(self) -> str:
        local_path = "buildingfootprints.zip"
        print("Downloading from url:\n", self.url)
        os.system(f"curl -o {local_path} {self.url}")
        return local_path

import re
import ssl
from urllib.request import Request, urlopen

import pandas as pd
import requests
import usaddress
from bs4 import BeautifulSoup

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_hnum(self, address):
        result = [k for (k, v) in usaddress.parse(address) if re.search("Address", v)]
        return " ".join(result)

    def get_sname(self, address):
        result = [k for (k, v) in usaddress.parse(address) if re.search("Street", v)]
        return " ".join(result)

    def get_zipcode(self, address):
        result = [k for (k, v) in usaddress.parse(address) if re.search("ZipCode", v)]
        return " ".join(result)

    def ingest(self) -> pd.DataFrame:
        url = "http://www.doccs.ny.gov/faclist.html"
        soup = BeautifulSoup(requests.get(url).content, features="html.parser")
        data = []
        for i in soup.find_all("tr")[1:]:
            info = [
                item.strip()
                for item in i.get_text().split("\n")
                if item not in ["", "Map", "Driving Directions"]
            ]
            address_long = ", ".join(info[1:-2]).split(", (")[0]
            county = (
                (", ".join(info[1:-2]).split(", (")[1]).split("(")[1].split(" Co")[0]
            )
            result = dict(
                facility_name=info[0],
                address=address_long,
                house_number=self.get_hnum(address_long),
                street_name=self.get_sname(address_long).replace(",", ""),
                county=county,
                zipcode=self.get_zipcode(address_long),
                security_level=info[-2],
                male_or_female=info[-1],
            )
            data.append(result)
        df = pd.DataFrame.from_dict(data, orient="columns")
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

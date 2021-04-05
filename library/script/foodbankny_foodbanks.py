import json
import ssl
from urllib.request import Request, urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        url = "https://www.foodbanknyc.org/wp-admin/admin-ajax.php?action=asl_load_stores&nonce=83cc04ac0d&load_all=0&layout=1&lat=40.7983474111969&lng=-73.9395518&nw%5B%5D=41.15908281222903&nw%5B%5D=-74.4614023859375&se%5B%5D=40.43761201016478&se%5B%5D=-73.4177012140625"
        hdr = {"User-Agent": "Mozilla/5.0"}
        req = Request(url, headers=hdr)
        gcontext = ssl.SSLContext()
        page = urlopen(req, context=gcontext)
        soup = BeautifulSoup(page, features="lxml")
        p = soup.find("p").get_text()
        data = json.loads(p)
        df = pd.DataFrame.from_dict(data, orient="columns")

        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

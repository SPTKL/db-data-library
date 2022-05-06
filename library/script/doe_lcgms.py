import json

import pandas as pd
import requests

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }
        body = "__EVENTTARGET=ctl00%24ContentPlaceHolder1%24LCGMSDataDownload%24Button1&__EVENTARGUMENT=&__VIEWSTATE=C7eAfHR%2FgZPxj29X50UYi6HVZO%2BJktQaDNCB5tjukvT5hzkKtTXlfz67jqxji6Bre9zcC4yyYkWeLd5aJSz6l%2B1mEfpoP6TGaZ6naJZ8%2BxNR8sNWVr7F26%2FlMfbhdZee&__VIEWSTATEGENERATOR=B9B96176&__EVENTVALIDATION=BEdLs1b7UJRDrD1O1phZV7VXmY%2ByE4%2F1LJ%2BXczt3sVncgOKsPke3fvII6oby1u7P%2Fwys0qcI5DZrWBQdivZ4ylrKkOUlNDwKfulKTQ%2FpIGLwNK%2BaUPJjH4x1bn11pVOD"
        
        r = requests.post(
            "https://www.nycenet.edu/PublicApps/LCGMS.aspx", #data=body, headers=headers
        )
        print(r.text)
        df = pd.read_html(r.text)
        df = df[0]  # first page of worksheet
        df.columns = df.iloc[0].str.replace("\t", " ")  # First row as column names
        df = df[1:]
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

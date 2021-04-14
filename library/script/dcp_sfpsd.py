import pandas as pd

from . import df_to_tempfile


class Scriptor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def ingest(self) -> pd.DataFrame:
        url = "https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/facilities_csv_201901.zip"
        df = pd.read_csv(url)
        df = df[
            df.pgtable.str.contains(
                "amtrak_facilities_sfpsd|bbpc_facilities_sfpsd|hrpt_facilities_sfpsd|"
                "mta_facilities_sfpsd|nysdot_facilities_sfpsd|panynj_facilities_sfpsd|"
                "tgi_facilities_sfpsd|rioc_facilities_sfpsd"
            )
        ]
        return df

    def runner(self) -> str:
        df = self.ingest()
        local_path = df_to_tempfile(df)
        return local_path

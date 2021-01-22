from osgeo import gdal
from .config import Config
from .sources import postgres_source, generic_source
import os

class Ingestor:
    def __init__(self):
        self.base_path = ".library"

    def translate_postgres(self, path: str, postgres_url: str) -> bool:
        """
        This function will take in a configuration then send to a
        postgres database
        path: path of the configuration
        postgres_url: connection string for the destination database
        """
        # Initiate configuration
        c = Config(path)
        _, source, destination, _ = c.compute_parsed

        # initiate source and destination datasets
        dstDS = postgres_source(postgres_url)
        srcDS = generic_source(
            path=source["url"]["gdalpath"],
            options=source["options"],
            fields=destination["fields"],
        )

        # Initiate the translation
        gdal.VectorTranslate(
            dstDS,
            srcDS,
            format="PostgreSQL",
            layerCreationOptions=destination["options"],
            dstSRS=destination["geometry"]["SRS"],
            srcSRS=source["geometry"]["SRS"],
            geometryType=destination["geometry"]["type"],
            layerName=destination["name"],
            accessMode="overwrite",
            # optional settings
            SQLStatement=destination.get("sql", ""),
            callback=gdal.TermProgress,
        )
        return True

    def translate_csv(self, path: str, clean: bool = False) -> bool:
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, source, destination, _ = c.compute_parsed
        # initiate source and destination datasets
        folder_path=f"{self.base_path}/datasets/{dataset['name']}/{dataset['version']}"
        os.makedirs(folder_path, exist_ok=True)
        destination_path = f"{folder_path}/{dataset['name']}.csv"
        dstDS = destination_path
        srcDS = generic_source(
            path=source["url"]["gdalpath"],
            options=source["options"],
            fields=destination.get("fields", ''),
        )

        # Initiate the translation
        gdal.VectorTranslate(
            dstDS,
            srcDS,
            format="CSV",
            layerCreationOptions=destination["options"],
            dstSRS=destination["geometry"]["SRS"],
            srcSRS=source["geometry"]["SRS"],
            geometryType=destination["geometry"]["type"],
            layerName=destination["name"],
            # optional settings
            SQLStatement=destination.get("sql", None),
            callback=gdal.TermProgress,
        )
        return True

    def translate_pgdump(self, path: str, clean: bool = False) -> bool:
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, source, destination, _ = c.compute_parsed
        # initiate source and destination datasets
        folder_path=f"{self.base_path}/datasets/{dataset['name']}/{dataset['version']}"
        os.makedirs(folder_path, exist_ok=True)
        destination_path = f"{folder_path}/{dataset['name']}.sql"
        dstDS = destination_path
        srcDS = generic_source(
            path=source["url"]["gdalpath"],
            options=source["options"],
            fields=destination.get("fields", ''),
        )

        # Initiate the translation
        gdal.VectorTranslate(
            dstDS,
            srcDS,
            format="PGDump",
            layerCreationOptions=destination["options"],
            dstSRS=destination["geometry"]["SRS"],
            srcSRS=source["geometry"]["SRS"],
            geometryType=destination["geometry"]["type"],
            layerName=destination["name"],
            accessMode="overwrite",
            # optional settings
            SQLStatement=destination.get("sql", None),
            callback=gdal.TermProgress,
        )
        return True
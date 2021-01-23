from osgeo import gdal
from .config import Config
from .sources import postgres_source, generic_source
import os
import zipfile


class Ingestor:
    def __init__(self):
        self.base_path = ".library"

    def translate(
        self, dstDS, srcDS, output_format: str, source: dict, destination: dict
    ):
        gdal.VectorTranslate(
            dstDS,
            srcDS,
            format=output_format,
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

    def compress(self, path: str, *files, inplace: bool = True):
        with zipfile.ZipFile(
            path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as _zip:
            for f in files:
                if os.path.isfile(f):
                    _zip.write(f, os.path.basename(f))
                    if inplace:
                        os.remove(f)
                else:
                    raise f"{f} does not exist!"
        return True

    def write_config(self, path: str, config: str):
        with open(path, "w") as f:
            f.write(config)

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

        # Initiate translation
        self.translate(dstDS, srcDS, "PostgreSQL", source, destination)
        return True

    def translate_csv(
        self,
        path: str,
        compress: bool = False,
        inplace: bool = False,
    ) -> bool:
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, source, destination, _ = c.compute_parsed
        # initiate source and destination datasets
        folder_path = (
            f"{self.base_path}/datasets/{dataset['name']}/{dataset['version']}"
        )
        os.makedirs(folder_path, exist_ok=True)
        destination_path = f"{folder_path}/{dataset['name']}.csv"
        dstDS = destination_path
        srcDS = generic_source(
            path=source["url"]["gdalpath"],
            options=source["options"],
            fields=destination.get("fields", ""),
        )

        # Initiate translation
        self.translate(dstDS, srcDS, "CSV", source, destination)

        # Compression if needed
        if compress:
            output_path = f"{destination_path}.zip"
            self.compress(output_path, destination_path, inplace=inplace)

        # Output config file
        self.write_config(f"{folder_path}/config.json", c.compute_json)
        self.write_config(f"{folder_path}/config.yml", c.compute_yml)

        return True

    def translate_pgdump(
        self,
        path: str,
        compress: bool = False,
        inplace: bool = False,
    ) -> bool:
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, source, destination, _ = c.compute_parsed
        # initiate source and destination datasets
        folder_path = (
            f"{self.base_path}/datasets/{dataset['name']}/{dataset['version']}"
        )
        os.makedirs(folder_path, exist_ok=True)
        destination_path = f"{folder_path}/{dataset['name']}.sql"
        dstDS = destination_path
        srcDS = generic_source(
            path=source["url"]["gdalpath"],
            options=source["options"],
            fields=destination.get("fields", ""),
        )

        # Initiate translation
        self.translate(dstDS, srcDS, "PGDump", source, destination)

        # Compression if needed
        if compress:
            output_path = f"{destination_path}.zip"
            self.compress(output_path, destination_path, inplace=inplace)

        # Output config file
        self.write_config(f"{folder_path}/config.json", c.compute_json)
        self.write_config(f"{folder_path}/config.yml", c.compute_yml)

        return True

    def translate_shapefile(self, path: str) -> bool:
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, source, destination, _ = c.compute_parsed
        name = dataset["name"]
        # initiate source and destination datasets
        folder_path = f"{self.base_path}/datasets/{name}/{dataset['version']}"
        os.makedirs(folder_path, exist_ok=True)
        destination_path = f"{folder_path}/{name}.shp"
        dstDS = destination_path
        srcDS = generic_source(
            path=source["url"]["gdalpath"],
            options=source["options"],
            fields=destination.get("fields", ""),
        )

        # Initiate the translation
        self.translate(dstDS, srcDS, "ESRI Shapefile", source, destination)

        # Zipping output
        files = [
            f"{folder_path}/{name}.{suffix}" for suffix in ["shp", "prj", "shx", "dbf"]
        ]
        self.compress(f"{destination_path}.zip", *files)

        # Output config file
        self.write_config(f"{folder_path}/config.json", c.compute_json)
        self.write_config(f"{folder_path}/config.yml", c.compute_yml)

        return True

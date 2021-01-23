from osgeo import gdal
from .config import Config
from .sources import postgres_source, generic_source
import os
import zipfile


class Ingestor:
    def __init__(self):
        self.base_path = ".library"

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
                    print(f"{f} does not exist!")
        return True

    def write_config(self, path: str, config: str):
        with open(path, "w") as f:
            f.write(config)

    def translator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            path = args[1]
            c = Config(path)
            _, source, destination, _ = c.compute_parsed
            srcDS = generic_source(
                path=source["url"]["gdalpath"],
                options=source["options"],
                fields=destination["fields"],
            )
            (
                dstDS,
                folder_path,
                destination_path,
                output_format,
                compress,
                inplace,
            ) = func(*args, **kwargs)

            # initiate source and destination datasets
            if folder_path:
                os.makedirs(folder_path, exist_ok=True)
                # Output config file
                self.write_config(f"{folder_path}/config.json", c.compute_json)
                self.write_config(f"{folder_path}/config.yml", c.compute_yml)

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

            # Compression if needed
            if compress and destination_path:
                if output_format == "ESRI Shapefile":
                    files = [
                        f"{destination_path[:-4]}.{suffix}"
                        for suffix in ["shp", "prj", "shx", "dbf"]
                    ]
                    self.compress(f"{destination_path}.zip", *files, inplace=True)
                else:
                    self.compress(
                        f"{destination_path}.zip", destination_path, inplace=inplace
                    )

        return wrapper

    @translator
    def postgres(
        self, path: str, postgres_url: str, compress: bool = False, inplace=False
    ):
        """
        This function will take in a configuration then send to a
        postgres database
        path: path of the configuration
        postgres_url: connection string for the destination database
        """
        dstDS = postgres_source(postgres_url)
        folder_path, destination_path = None, None
        output_format = "PostgreSQL"
        return dstDS, folder_path, destination_path, output_format, compress, inplace

    @translator
    def csv(
        self,
        path: str,
        compress: bool = False,
        inplace: bool = False,
    ):
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, _, _, _ = c.compute_parsed
        # initiate source and destination datasets
        folder_path = (
            f"{self.base_path}/datasets/{dataset['name']}/{dataset['version']}"
        )
        destination_path = f"{folder_path}/{dataset['name']}.csv"
        dstDS = destination_path
        return dstDS, folder_path, destination_path, "CSV", compress, inplace

    @translator
    def pgdump(
        self,
        path: str,
        compress: bool = False,
        inplace: bool = False,
    ):
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, _, _, _ = c.compute_parsed
        # initiate source and destination datasets
        folder_path = (
            f"{self.base_path}/datasets/{dataset['name']}/{dataset['version']}"
        )
        destination_path = f"{folder_path}/{dataset['name']}.sql"
        dstDS = destination_path
        return dstDS, folder_path, destination_path, "PGDump", compress, inplace

    @translator
    def shapefile(self, path: str) -> bool:
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, _, _, _ = c.compute_parsed
        name = dataset["name"]
        # initiate source and destination datasets
        folder_path = f"{self.base_path}/datasets/{name}/{dataset['version']}"
        destination_path = f"{folder_path}/{name}.shp"
        dstDS = destination_path
        compress, inplace = True, True
        return dstDS, folder_path, destination_path, "ESRI Shapefile", compress, inplace

    @translator
    def geojson(
        self,
        path: str,
        compress: bool = False,
        inplace: bool = False,
    ):
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        clean: remove temporary files (this is used in conjunction with s3 upload_file)
        """
        # Initiate configuration
        c = Config(path)
        dataset, _, _, _ = c.compute_parsed
        # initiate source and destination datasets
        folder_path = (
            f"{self.base_path}/datasets/{dataset['name']}/{dataset['version']}"
        )
        destination_path = f"{folder_path}/{dataset['name']}.geojson"
        dstDS = destination_path
        return dstDS, folder_path, destination_path, "GeoJSON", compress, inplace

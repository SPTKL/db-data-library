import os
import zipfile

from osgeo import gdal

from .config import Config
from .sources import generic_source, postgres_source


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
            dataset, source, destination, _ = c.compute_parsed
            name = dataset["name"]
            version = dataset["version"]
            (dstDS, output_format, output_suffix, compress, inplace) = func(
                *args, **kwargs
            )

            # initiate source and destination datasets
            folder_path = f"{self.base_path}/datasets/{name}/{version}"
            destination_path = (
                f"{folder_path}/{name}.{output_suffix}" if output_suffix else None
            )

            # Default dstDS is destination_path if no dstDS is specificed
            dstDS = destination_path if not dstDS else dstDS
            srcDS = generic_source(
                path=source["url"]["gdalpath"],
                options=source["options"],
                fields=destination["fields"],
            )

            # Create output folder and output config
            if folder_path and output_suffix:
                os.makedirs(folder_path, exist_ok=True)
                self.write_config(f"{folder_path}/config.json", c.compute_json)
                self.write_config(f"{folder_path}/config.yml", c.compute_yml)

            # Initiate vector translate
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
        https://gdal.org/drivers/vector/pg.html

        This function will take in a configuration then send to a
        postgres database
        path: path of the configuration
        postgres_url: connection string for the destination database
        compress: default to False because no files created when output to "PostgreSQL"
        inplace: default to False because no compress = False by default
        """
        dstDS = postgres_source(postgres_url)
        return dstDS, "PostgreSQL", None, compress, inplace

    @translator
    def csv(self, path: str, compress: bool = False, inplace: bool = False):
        """
        https://gdal.org/drivers/vector/csv.html

        path: path of the configuration file
        compress: True if compression is needed
        inplace: True if the compressed file will replace the original output
        """
        return None, "CSV", "csv", compress, inplace

    @translator
    def pgdump(self, path: str, compress: bool = False, inplace: bool = False):
        """
        https://gdal.org/drivers/vector/pgdump.html

        path: path of the configuration file
        compress: True if compression is needed
        inplace: True if the compressed file will replace the original output
        """
        return None, "PGDump", "sql", compress, inplace

    @translator
    def shapefile(self, path: str, compress: bool = True, inplace=True) -> bool:
        """
        https://gdal.org/drivers/vector/shapefile.html

        path: path of the configuration file
        compress: default to True so that [shp, shx, dbf, prj] are bundled
        inplace: default to True for ease of transport
        """
        return None, "ESRI Shapefile", "shp", compress, inplace

    @translator
    def geojson(self, path: str, compress: bool = False, inplace: bool = False):
        """
        https://gdal.org/drivers/vector/geojson.html

        path: path of the configuration file
        compress: True if compression is needed
        inplace: True if the compressed file will replace the original output
        """
        return None, "GeoJSON", "geojson", compress, inplace

from osgeo import gdal

class Ingestor:
    def __init__(self):
        self.S3 = None # Not implemented yet
        self.DB = None # Not implemented yet

    def archive_postgres(self, config: dict):
        """
        archive dataset to a postgres database
        """
        return None

    def archive_pgdump(self, config: dict):
        """
        archive dataset as pgdump
        """
        return None


    def archive_shapefile(self, config: dict):
        """
        archive dataset as a shapefile
        """
        return None


    def archive_csv(self, config: dict):
        """
        archive dataset as a csv
        """
        return None
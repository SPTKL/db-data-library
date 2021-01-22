from osgeo import gdal
from .config import Config


class Ingestor:
    def __init__(self):
        self.S3 = None

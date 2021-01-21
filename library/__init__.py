import os
from osgeo import gdal

# gdal configure aws s3 connection info
gdal.SetConfigOption(
    "AWS_S3_ENDPOINT", os.environ["AWS_S3_ENDPOINT"].replace("https://", "")
)
gdal.SetConfigOption("AWS_SECRET_ACCESS_KEY", os.environ["AWS_SECRET_ACCESS_KEY"])
gdal.SetConfigOption("AWS_ACCESS_KEY_ID", os.environ["AWS_ACCESS_KEY_ID"])

__version__ = '0.1.0'
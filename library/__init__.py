import os
from osgeo import gdal
import pprint
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# Initialize pretty print
pp = pprint.PrettyPrinter(indent=4)

# gdal configure aws s3 connection info
gdal.SetConfigOption("PG_USE_COPY", "YES")

# gdal configure aws s3 connection info
aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
aws_s3_endpoint = os.environ["AWS_S3_ENDPOINT"]
aws_s3_bucket = os.environ["AWS_S3_BUCKET"]
recipe_engine = os.environ["RECIPE_ENGINE"]

gdal.SetConfigOption("AWS_S3_ENDPOINT", aws_s3_endpoint.replace("https://", ""))
gdal.SetConfigOption("AWS_SECRET_ACCESS_KEY", aws_secret_access_key)
gdal.SetConfigOption("AWS_ACCESS_KEY_ID", aws_access_key_id)

# Create a local .library directory to store temporary files
if not os.path.isdir(".library"):
    os.makedirs(".library", exist_ok=True)
    # create .gitignore so that files in this directory aren't tracked
    with open(".library/.gitignore", "w") as f:
        f.write("*")
    os.makedirs(".library/datasets", exist_ok=True)
    os.makedirs(".library/configurations", exist_ok=True)

__version__ = "0.1.0"

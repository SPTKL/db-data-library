from library.s3 import S3
from pathlib import Path
from library import (
    aws_access_key_id,
    aws_secret_access_key,
    aws_s3_endpoint,
    aws_s3_bucket,
)

s3 = S3(aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket)

def test_s3_upload_file():
    s3.upload_file(name='test', version='20210120', path=f"{Path(__file__).parent}/data/socrata.yml")
    assert s3.exists('test/20210121/test.yml') == True
    # s3.upload_file(name='test', version='20210121', path=f"{Path(__file__).parent}/data/socrata.yml", acl='private')
    # assert s3.check_existence('test/20210121/test.yml') == True

def test_s3_ls():
    s3.ls('test')
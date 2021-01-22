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
    # Make sure file doesn't already exist
    assert s3.exists('test/20210121/test.yml') == False

    # Attempt to upload to 20210121/test.yml
    s3.upload_file(name='test', version='20210120', path=f"{Path(__file__).parent}/data/socrata.yml")

    # Make sure file now exists
    assert s3.exists('test/20210121/test.yml') == True

    # s3.upload_file(name='test', version='20210121', path=f"{Path(__file__).parent}/data/socrata.yml", acl='private')
    # assert s3.check_existence('test/20210121/test.yml') == True

def test_s3_ls():
    s3.ls('test')

def test_s3_info():
    # Make sure file exists before trying to pull info
    assert s3.exists('test/20210121/test.yml') == True

    # Pull file info
    info = s3.info(key='test/20210121/test.yml')
    if info:
        print(info)
    else:
        print('File exists, but no info retrieved.')

def test_s3_cp():
    # Make sure the 20210121 version exists, but the latest version doesn't
    assert s3.exists('test/20210121/test.yml') == True

    # Copy 20210121 to latest
    s3.cp(source_key='test/20210121/test.yml', dest_key='test/latest/test.yml')

    # Make sure the 20210121 version exists, and the latest version doesn't
    assert s3.exists('test/20210121/test.yml') == True
    assert s3.exists('test/latest/test.yml') == True

def test_s3_mv():
    # Make sure that the 20210121 version exists, but the moved version doesn't
    assert s3.exists('test/20210121/test.yml') == True
    assert s3.exists('test/moved/test.yml') == False

    # Move the 20210121 version to moved
    s3.mv(source_key='test/20210121/test.yml', dest_key='test/moved/test.yml')

    # Make sure that the moved version exists, but the 20210121 version doesn't
    assert s3.exists('test/moved/test.yml') == True
    assert s3.exists('test/20210121/test.yml') == False

def test_s3_rm():
    # Make sure that the moved version exists prior to move
    assert s3.exists('test/moved/test.yml') == True

    # Remove file
    s3.rm('test/moved/test.yml')

    # Make sure the file no longer exists
    assert s3.exists('test/moved/test.yml') == False

if __name__ == "__main__":
    print("Test upload...")
    test_s3_upload_file()

    print("Test ls...")
    test_s3_ls()

    print("Test info...")
    test_s3_info()

    print("Test cp...")
    test_s3_cp()

    print("Test mv...")
    test_s3_mv()

    print("Test rm...")
    test_s3_rm()
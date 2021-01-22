from library.s3 import S3
from pathlib import Path
from datetime import date
from library import (
    aws_access_key_id,
    aws_secret_access_key,
    aws_s3_endpoint,
    aws_s3_bucket,
)

s3 = S3(aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket)

def test_s3_upload_file(version:str):
    # Make sure file doesn't already exist
    assert s3.exists(f'test/{version}/test.yml') == False

    '''
    if s3.exists(f'test/{version}/test.yml') == True:
        s3.rm(f'test/{version}/test.yml')
    '''

    # Attempt to upload to {version}/test.yml
    s3.upload_file(name='test', version=version, path=f"{Path(__file__).parent}/data/socrata.yml")

    # Make sure file now exists
    assert s3.exists(f'test/{version}/test.yml') == True

    # s3.upload_file(name='test', version=version, path=f"{Path(__file__).parent}/data/socrata.yml", acl='private')
    # assert s3.check_existence(f'test/{version}/test.yml') == True

def test_s3_ls(version:str):
    print(s3.ls('test'))

def test_s3_info(version:str):
    # Make sure file exists before trying to pull info
    assert s3.exists(f'test/{version}/test.yml') == True

    # Pull file info
    info = s3.info(key=f'test/{version}/test.yml')
    if info:
        print(info)
    else:
        print('File exists, but no info retrieved.')

def test_s3_cp(version:str):
    # Make sure the {version} version exists, but the latest version doesn't
    assert s3.exists(f'test/{version}/test.yml') == True

    # Copy {version} to latest
    s3.cp(source_key=f'test/{version}/test.yml', dest_key='test/latest/test.yml')

    # Make sure the {version} version exists, and the latest version doesn't
    assert s3.exists(f'test/{version}/test.yml') == True
    assert s3.exists('test/latest/test.yml') == True

def test_s3_mv(version:str):
    # Make sure that the {version} version exists, but the moved version doesn't
    assert s3.exists(f'test/{version}/test.yml') == True
    assert s3.exists('test/moved/test.yml') == False

    # Move the {version} version to moved
    s3.mv(source_key=f'test/{version}/test.yml', dest_key='test/moved/test.yml')

    # Make sure that the moved version exists, but the {version} version doesn't
    assert s3.exists('test/moved/test.yml') == True
    assert s3.exists(f'test/{version}/test.yml') == False

def test_s3_rm(version:str):
    # Make sure that the moved version and latest version exist prior to rm
    assert s3.exists('test/moved/test.yml') == True
    assert s3.exists('test/latest/test.yml') == True
    # Remove files
    s3.rm(['test/moved/test.yml','test/latest/test.yml'])
    # Make sure the file no longer exists
    assert s3.exists('test/moved/test.yml') == False
    assert s3.exists('test/latest/test.yml') == False

if __name__ == "__main__":
    
    test_date = date.today().strftime("%Y-%m-%d")

    print("\nTest upload...")
    test_s3_upload_file(test_date)

    print("\nTest ls...")
    test_s3_ls(test_date)

    print("\nTest info...")
    test_s3_info(test_date)

    print("\nTest cp...")
    test_s3_cp(test_date)

    print("\nTest mv...")
    test_s3_mv(test_date)

    print("\nTest rm and clean up test directory...")
    test_s3_rm(test_date)
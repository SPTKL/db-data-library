from library.s3 import S3
from pathlib import Path
from datetime import date
from library import (
    aws_access_key_id,
    aws_secret_access_key,
    aws_s3_endpoint,
    aws_s3_bucket,
    pp
)

s3 = S3(aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket)
version = date.today().strftime("%Y-%m-%d")

def test_s3_upload_file():
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

def test_s3_ls():
    pp.pprint(s3.ls('test'))
    assert True

def test_s3_info():
    print("\nTest info...")
    # Make sure file exists before trying to pull info
    assert s3.exists(f'test/{version}/test.yml') == True

    # Pull file info
    info = s3.info(key=f'test/{version}/test.yml')
    if info:
        pp.pprint(info)
    else:
        pp.pprint('File exists, but no info retrieved.')

def test_s3_cp():
    print("\nTest cp...")
    # Make sure the {version} version exists, but the latest version doesn't
    assert s3.exists(f'test/{version}/test.yml') == True

    # Copy {version} to latest
    s3.cp(source_key=f'test/{version}/test.yml', dest_key='test/latest/test.yml')

    # Make sure the {version} version exists, and the latest version doesn't
    assert s3.exists(f'test/{version}/test.yml') == True
    assert s3.exists('test/latest/test.yml') == True

def test_s3_mv():
    print("\nTest mv...")
    # Make sure that the {version} version exists, but the moved version doesn't
    assert s3.exists(f'test/{version}/test.yml') == True
    assert s3.exists('test/moved/test.yml') == False

    # Move the {version} version to moved
    s3.mv(source_key=f'test/{version}/test.yml', dest_key='test/moved/test.yml')

    # Make sure that the moved version exists, but the {version} version doesn't
    assert s3.exists('test/moved/test.yml') == True
    assert s3.exists(f'test/{version}/test.yml') == False

def test_s3_rm():
    print("\nTest rm and clean up test directory...")
    # Make sure that the moved version and latest version exist prior to rm
    assert s3.exists('test/moved/test.yml') == True
    assert s3.exists('test/latest/test.yml') == True
    # Remove files
    s3.rm(['test/moved/test.yml','test/latest/test.yml'])
    # Make sure the file no longer exists
    assert s3.exists('test/moved/test.yml') == False
    assert s3.exists('test/latest/test.yml') == False
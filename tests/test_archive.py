import os

from sqlalchemy import create_engine

from library import recipe_engine
from library.archive import Archive

from . import test_root_path

a = Archive()
pg = create_engine(recipe_engine)


def start_clean(local_files: list, s3_files: list):
    for f in local_files:
        if os.path.isfile(f):
            os.remove(f)
    for f in s3_files:
        if a.s3.exists(f):
            a.s3.rm(f)


def test_archive_1():
    local_not_exist = [
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.csv.zip",
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.csv",
    ]
    s3_exist = [
        "datasets/nypl_libraries/20210122/nypl_libraries.csv.zip",
        "datasets/nypl_libraries/latest/nypl_libraries.csv.zip",
        "datasets/nypl_libraries/20210122/config.yml",
        "datasets/nypl_libraries/20210122/config.json",
        "datasets/nypl_libraries/latest/nypl_libraries.csv.zip",
        "datasets/nypl_libraries/latest/config.yml",
        "datasets/nypl_libraries/latest/config.json",
    ]
    start_clean(local_not_exist, s3_exist)
    a(
        f"{test_root_path}/data/nypl_libraries.yml",
        output_format="csv",
        push=True,
        clean=True,
        latest=True,
        compress=True,
    )
    for f in local_not_exist:
        assert not os.path.isfile(f)
    for f in s3_exist:
        assert a.s3.exists(f)
    start_clean(local_not_exist, s3_exist)


def test_archive_2():
    s3_not_exist = [
        "datasets/nypl_libraries/20210122/nypl_libraries.geojson.zip",
        "datasets/nypl_libraries/20210122/config.yml",
        "datasets/nypl_libraries/20210122/config.json",
        "datasets/nypl_libraries/20210122/nypl_libraries.geojson",
        "datasets/nypl_libraries/latest/nypl_libraries.geojson.zip",
        "datasets/nypl_libraries/latest/config.yml",
        "datasets/nypl_libraries/latest/config.json",
        "datasets/nypl_libraries/latest/nypl_libraries.geojson",
    ]
    local_exist = [
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.geojson.zip",
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.geojson",
        ".library/datasets/nypl_libraries/20210122/config.yml",
        ".library/datasets/nypl_libraries/20210122/config.json",
    ]
    start_clean(local_exist, s3_not_exist)
    a(
        f"{test_root_path}/data/nypl_libraries.yml",
        output_format="geojson",
        push=False,
        clean=False,
        latest=True,
        compress=True,
    )
    for f in s3_not_exist:
        assert not a.s3.exists(f)
    for f in local_exist:
        assert os.path.isfile(f)
    start_clean(local_exist, s3_not_exist)


def test_archive_3():
    a(
        f"{test_root_path}/data/nypl_libraries.yml",
        output_format="postgres",
        postgres_url=recipe_engine,
    )
    sql = """
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE  table_schema = 'public'
        AND    table_name   = 'nypl_libraries'
    );
    """
    result = pg.execute(sql).fetchall()
    assert result[0][0], "nypl_libraries is not in postgres database yet"

    # Clean up
    if result[0][0]:
        pg.execute("DROP TABLE IF EXISTS nypl_libraries;")
    result = pg.execute(sql).fetchall()
    assert not result[0][0], "clean up failed"


def test_archive_4():
    s3_not_exist = [
        "datasets/nypl_libraries/testor/nypl_libraries.csv.zip",
        "datasets/nypl_libraries/latest/nypl_libraries.csv.zip",
        "datasets/nypl_libraries/latest/nypl_libraries.csv",
        "datasets/nypl_libraries/latest/config.yml",
        "datasets/nypl_libraries/latest/config.json",
    ]
    s3_exist = [
        "datasets/nypl_libraries/testor/config.yml",
        "datasets/nypl_libraries/testor/config.json",
        "datasets/nypl_libraries/testor/nypl_libraries.csv",
    ]
    local_exist = [
        ".library/datasets/nypl_libraries/testor/nypl_libraries.csv",
        ".library/datasets/nypl_libraries/testor/config.yml",
        ".library/datasets/nypl_libraries/testor/config.json",
    ]
    local_not_exist = [".library/datasets/nypl_libraries/testor/nypl_libraries.csv.zip"]
    start_clean(local_exist + local_not_exist, s3_exist + s3_not_exist)
    a(
        f"{test_root_path}/data/nypl_libraries.yml",
        output_format="csv",
        push=True,
        clean=False,
        compress=False,
        latest=False,
        version="testor",
    )
    for f in local_exist:
        assert os.path.isfile(f)
    for f in local_not_exist:
        assert not os.path.isfile(f)
    for f in s3_exist:
        assert a.s3.exists(f)
    for f in s3_not_exist:
        assert not a.s3.exists(f)
    start_clean(local_exist + local_not_exist, s3_exist + s3_not_exist)

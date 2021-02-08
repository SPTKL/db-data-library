import os

from library.ingest import Ingestor

from . import pg, recipe_engine, test_root_path


def test_ingest_postgres():
    ingestor = Ingestor()
    ingestor.postgres(
        f"{test_root_path}/data/nypl_libraries.yml", postgres_url=recipe_engine
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


def test_ingest_csv():
    ingestor = Ingestor()
    ingestor.csv(f"{test_root_path}/data/nypl_libraries.yml", compress=True)
    assert os.path.isfile(
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.csv"
    )


def test_ingest_pgdump():
    ingestor = Ingestor()
    ingestor.pgdump(f"{test_root_path}/data/nypl_libraries.yml", compress=True)
    assert os.path.isfile(
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.sql"
    )


def test_ingest_geojson():
    ingestor = Ingestor()
    ingestor.geojson(f"{test_root_path}/data/nypl_libraries.yml", compress=True)
    assert os.path.isfile(
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.geojson"
    )


def test_ingest_shapefile():
    ingestor = Ingestor()
    ingestor.shapefile(f"{test_root_path}/data/nypl_libraries.yml")
    assert os.path.isfile(
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.shp.zip"
    )


def test_ingest_version_overwrite():
    ingestor = Ingestor()
    ingestor.csv(f"{test_root_path}/data/nypl_libraries.yml", version="test")
    assert os.path.isfile(".library/datasets/nypl_libraries/test/nypl_libraries.csv")

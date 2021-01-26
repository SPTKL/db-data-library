import os

from library import recipe_engine
from library.archive import Archive

from . import test_root_path

a = Archive()


def test_archive_1():
    a(
        f"{test_root_path}/data/nypl_libraries.yml",
        output_format="csv",
        push=True,
        clean=True,
        latest=True,
        compress=True,
    )


def test_archive_2():
    a(
        f"{test_root_path}/data/nypl_libraries.yml",
        output_format="geojson",
        push=False,
        clean=False,
        latest=True,
        compress=True,
    )


def test_archive_3():
    a(
        f"{test_root_path}/data/nypl_libraries.yml",
        output_format="postgres",
        postgres_url=recipe_engine,
    )


def test_archive_4():
    a(
        f"{test_root_path}/data/nypl_libraries.yml",
        output_format="csv",
        version="testor",
    )

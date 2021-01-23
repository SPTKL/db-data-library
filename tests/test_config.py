from library.config import Config
from pathlib import Path


def test_config_parsed_rendered_template():
    c = Config(f"{Path(__file__).parent}/data/url.yml")
    rendered = c.parsed_rendered_template(version="20v7")
    assert rendered["dataset"]["version"] == "20v7"


def test_config_source_type():
    c = Config(f"{Path(__file__).parent}/data/socrata.yml")
    assert c.source_type == "socrata"
    c = Config(f"{Path(__file__).parent}/data/url.yml")
    assert c.source_type == "url"


def test_config_version_socrata():
    c = Config(f"{Path(__file__).parent}/data/socrata.yml")
    uid = c.parsed_unrendered_template["dataset"]["source"]["socrata"]["uid"]
    version = c.version_socrata(uid)
    assert len(version) == 8  # format: YYYYMMDD
    assert int(version[-2:]) <= 31  # check date
    assert int(version[-4:-2]) <= 12  # check month


def test_config_version_today():
    c = Config(f"{Path(__file__).parent}/data/socrata.yml")
    version = c.version_today
    assert len(version) == 8  # format: YYYYMMDD
    assert int(version[-2:]) <= 31  # check date
    assert int(version[-4:-2]) <= 12  # check month


def test_config_compute():
    config = Config(f"{Path(__file__).parent}/data/socrata.yml").compute
    assert type(config["dataset"]["source"]["url"]) == dict


def test_config_compute_parsed():
    dataset, source, destination, info = Config(
        f"{Path(__file__).parent}/data/socrata.yml"
    ).compute_parsed
    assert dataset["source"] == source
    assert dataset["info"] == info
    assert dataset["destination"] == destination
    assert "url" in list(source.keys())
    assert "options" in list(source.keys())
    assert "geometry" in list(source.keys())
    assert "fields" in list(destination.keys())
    assert "options" in list(destination.keys())
    assert "geometry" in list(destination.keys())

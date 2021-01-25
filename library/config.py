import json
from datetime import datetime

import requests
import yaml
from jinja2 import Template

from .utils import format_url


# Custom dumper created for list indentation
class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)


class Config:
    """
    Config will take a configuration file from the templates directly
    or any given configuration file and compute/output a configuration
    file to pass into the Ingestor
    """

    def __init__(self, path: str):
        self.path = path

    @property
    def unparsed_unrendered_template(self) -> str:
        """importing the yml file into a string"""
        with open(self.path, "r") as f:
            return f.read()

    @property
    def parsed_unrendered_template(self) -> dict:
        """parsing unrendered template"""
        return yaml.safe_load(self.unparsed_unrendered_template)

    def parsed_rendered_template(self, **kwargs) -> dict:
        """render template, then parse into a dictionary"""
        template = Template(self.unparsed_unrendered_template)
        return yaml.safe_load(template.render(**kwargs))

    @property
    def source_type(self) -> str:
        """determin the type of the source, either url or socrata"""
        template = self.parsed_unrendered_template
        source = template["dataset"]["source"]
        return list(source.keys())[0]

    def version_socrata(self, uid: str) -> str:
        """using the socrata API to collect data last update date"""
        metadata = requests.get(
            f"https://data.cityofnewyork.us/api/views/{uid}.json"
        ).json()
        version = datetime.fromtimestamp(metadata["rowsUpdatedAt"]).strftime("%Y%m%d")
        return version

    # @property
    # def version_bytes(self) -> str:
    #     """parsing bytes of the big apple to get the latest bytes version"""
    #     # scrape from bytes to get a version
    #     return None

    @property
    def version_today(self) -> str:
        """using today as the version name"""
        return datetime.today().strftime("%Y%m%d")

    @property
    def compute(self) -> dict:
        """based on given yml file and compute configuration"""
        if self.source_type == "url":
            # Note that version here is only provided as an option
            # if version is verbosely defined, it will not replace what's in yaml
            config = self.parsed_rendered_template(version=self.version_today)

        if self.source_type == "socrata":
            # For socrata we are computing the url and add the url object to the config file
            _uid = self.parsed_unrendered_template["dataset"]["source"]["socrata"][
                "uid"
            ]
            _format = self.parsed_unrendered_template["dataset"]["source"]["socrata"][
                "format"
            ]
            config = self.parsed_rendered_template(version=self.version_socrata(_uid))
            if _format == "csv":
                url = f"https://data.cityofnewyork.us/api/views/{_uid}/rows.csv"
            if _format == "geojson":
                url = f"https://nycopendata.socrata.com/api/geospatial/{_uid}?method=export&format=GeoJSON"
            options = config["dataset"]["source"]["options"]
            geometry = config["dataset"]["source"]["geometry"]
            config["dataset"]["source"] = {
                "url": {"path": url, "subpath": ""},
                "options": options,
                "geometry": geometry,
            }

        path = config["dataset"]["source"]["url"]["path"]
        subpath = config["dataset"]["source"]["url"]["subpath"]
        config["dataset"]["source"]["url"]["gdalpath"] = format_url(path, subpath)
        return config

    @property
    def compute_json(self) -> str:
        return json.dumps(self.compute, indent=4)

    @property
    def compute_yml(self) -> str:
        return yaml.dump(
            self.compute,
            Dumper=Dumper,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )

    @property
    def compute_parsed(self) -> (dict, dict, dict, dict):
        config = self.compute
        dataset = config["dataset"]
        source = dataset["source"]
        destination = dataset["destination"]
        info = dataset["info"]
        return dataset, source, destination, info

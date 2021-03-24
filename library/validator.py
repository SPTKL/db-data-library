from functools import cached_property
from typing import List, Literal

import yaml
from pydantic import BaseModel, ValidationError, validator

VALID_ACL_VALUES = ("public-read", "private")
VALID_GEOMETRY_TYPES = (
    "POINT",
    "LINE",
    "POLYGON",
    "MULTIPOLYGON",
    "MULTILINESTRING",
    "LINESTRING",
    "NONE",
)
VALID_SOCRATA_FORMATS = ("csv", "geojson")

# Create schema
class GeometryType(BaseModel):
    SRS: str
    type: Literal[VALID_GEOMETRY_TYPES]


class Url(BaseModel):
    path: str  # Specify field name and data type
    subpath: str = ""  # Set default value


class Socrata(BaseModel):
    uid: str
    format: Literal[
        VALID_SOCRATA_FORMATS
    ]  # Use Literal[tuple(dtype)] to define specific, valid values


class SourceSection(BaseModel):
    url: Url = None  # Pass another schema as a data type
    socrata: Socrata = None
    script: str = None
    geometry: GeometryType
    options: List[str] = []  # Use List[dtype] for a list field value


class DestinationSection(BaseModel):
    name: str
    geometry: GeometryType
    options: List[str] = []
    fields: List[str] = []
    sql: str = None


class InfoSection(BaseModel):
    info: str = None
    url: str = None
    dependents: List[str] = None


class Dataset(BaseModel):
    name: str
    version: str
    acl: Literal[VALID_ACL_VALUES]
    source: SourceSection
    destination: DestinationSection
    info: InfoSection = None


class Validator:
    """
    Validator takes as input the path of a configuration file
    and will run the necessary checks to determine wether the structure
    and values of the files are valid according to the requirements of
    the library.
    """

    def __init__(self, f):
        self.__unparsed_file = f

    def __call__(self):
        assert self.tree_is_valid
        assert self.dataset_name_matches
        assert self.has_only_one_source

    # Check that the tree structure fits the specified schema
    @property
    def tree_is_valid(self) -> bool:
        return True

    # Check that the dataset name matches with destination name
    @property
    def dataset_name_matches(self):
        return True

    # Check that source has only one source from either url, socrata or script
    @property
    def has_only_one_source(self):
        return True

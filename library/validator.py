import yaml
from typing import Literal, List
from pydantic import BaseModel, ValidationError, validator
from functools import cached_property

VALID_ACL_VALUES = ('public-read', 'private')
VALID_GEOMETRY_TYPES = ('POINT', 'LINE', 'POLYGON', 'MULTIPOLYGON', 'MULTILINESTRING', 'LINESTRING', 'NONE')
VALID_SOCRATA_FORMATS = ('csv', 'geojson')

# Create schema
class GeometryType(BaseModel):
    SRS: str
    type: Literal[VALID_GEOMETRY_TYPES]

class Url(BaseModel):
    path: str # Specify field name and data type
    subpath: str = "" # Set default value

class Socrata(BaseModel):
    uid: str
    format: Literal[VALID_SOCRATA_FORMATS] # Use Literal[tuple(dtype)] to define specific, valid values

class SourceSection(BaseModel):
    url: Url = None # Pass another schema as a data type
    socrata: Socrata = None
    script: str = None
    geometry: GeometryType
    options: List[str] = [] # Use List[dtype] for a list field value

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

    def __init__(self, path):
        self.path = path

    @cached_property
    def __file(self):
        with open(self.path, 'r') as stream:
            y = yaml.load(stream, Loader=yaml.FullLoader)
            return y

    def tree_is_valid(self) -> bool:
        if(self.__file['dataset'] == None):
            return False

        try:
            input_ds = Dataset(**self.__file['dataset'])          

        except ValidationError as e:
            print(e.json())
            return False       
        
        return True

    # Check that source name matches filename and destination
    def dataset_name_matches(self, name, file) -> bool:
        dataset = file['dataset']
        return (dataset['name'] == name) and (dataset['name'] == dataset['destination']['name'])

    # Check that source has only one source from either url, socrata or script
    def has_only_one_source(self, file):
        dataset = file['dataset']
        source_fields = list(dataset['source'].keys())
        # In other words: if url is in source, socrata or script cannot be.
        # If url is NOT in source. Only one from socrata or url can be. (XOR operator ^)
        return \
        (('socrata' not in source_fields) and ('script' not in source_fields)) \
        if ('url' in source_fields) \
        else (('socrata' in source_fields) ^ ('script' in source_fields)) 

    def validate_file(self, path):

        # Check if path ends with a .yml file
        extension = path.split('/')[-1].split('.')[-1]
        assert extension in ['yml', 'yaml'], 'Invalid file type'

        f = self.__load_file(path)
        name = path.split('/')[-1].split('.')[0]

        # TODO: Validate tree structure
        assert self.tree_is_valid(f), 'Wrong fields'
        assert self.dataset_name_matches(name, f), 'Dataset name must match file and destination name'
        assert self.has_only_one_source(f), 'Source can only have one property from either url, socrata or script' 
                
        return True   


        
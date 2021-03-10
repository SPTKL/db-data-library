from pathlib import Path
from library.validator import Validator
import yaml

v = Validator()

with open(f"{Path(__file__).parent}/data/test_none.yml", 'r') as stream:
    f = yaml.load(stream, Loader=yaml.FullLoader)

def test_dataset_name_matches():
    assert v.dataset_name_matches('test_none', f)

def test_has_url_or_socrata():
    assert v.has_url_or_socrata(f)

def test_tree_structure():
    assert v.tree_is_valid(f)

def test_validate_file():
    v.validate_file(f"{Path(__file__).parent}/data/nypl_libraries.yml")
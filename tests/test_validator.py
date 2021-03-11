from pathlib import Path
from library.validator import Validator
import yaml

v = Validator(f"{Path(__file__).parent}/data/test_none.yml")

def test_tree_structure():
    assert v.tree_is_valid
    
def test_dataset_name_matches():
    assert v.dataset_name_matches('test_none')

def test_has_only_one_source():
    assert v.has_only_one_source

def test_validate_file():
    assert v.file_is_valid

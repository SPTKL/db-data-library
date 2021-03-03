from pathlib import Path
from library.validator import Validator
import yaml

v = Validator()

with open(f"{Path(__file__).parent}/data/url.yml", 'r') as stream:
    f = yaml.load(stream, Loader=yaml.FullLoader)

def test_dataset_name_matches():
    assert v.dataset_name_matches(f, 'url')
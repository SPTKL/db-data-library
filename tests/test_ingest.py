from library.ingest import Ingestor
from . import test_root_path
import os

def test_ingest_translate_csv():
    ingestor = Ingestor()
    ingestor.translate_csv(f'{test_root_path}/data/nypl_libraries.yml')
    assert os.path.isfile(".library/datasets/nypl_libraries/20210122/nypl_libraries.csv")

def test_ingest_translate_pgdump():
    ingestor = Ingestor()
    ingestor.translate_pgdump(f'{test_root_path}/data/nypl_libraries.yml')
    assert os.path.isfile(".library/datasets/nypl_libraries/20210122/nypl_libraries.sql")
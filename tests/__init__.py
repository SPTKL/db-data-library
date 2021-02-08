import os
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from sqlalchemy import create_engine

# Load environmental variables
load_dotenv()

recipe_engine = os.environ["RECIPE_ENGINE"]
pg = create_engine(recipe_engine)

console = Console()
test_root_path = Path(__file__).parent
template_path = f"{Path(__file__).parent.parent}/library/templates"

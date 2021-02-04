from pathlib import Path

from rich.console import Console

console = Console()
test_root_path = Path(__file__).parent
template_path = f"{Path(__file__).parent.parent}/library/templates"

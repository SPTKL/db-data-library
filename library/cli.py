import os
import time
from typing import Optional

import typer

from .archive import Archive

app = typer.Typer()

# fmt: off
@app.command()
def archive(
    path: str = typer.Option(None, "--path", "-f", help="Path to config yml"),
    output_format: str = typer.Option("pgdump", "--output-format", "-o", help="csv, geojson, shapefile, pgdump and postgres"),
    push: bool = typer.Option(False, "--s3", "-s", help="Push to s3"),
    clean: bool = typer.Option(False, "--clean", "-c", help="Remove temporary files"),
    latest: bool = typer.Option(False, "--latest", "-l", help="Tag with latest"),
    name: str = typer.Option(None, "--name", "-n", help="Name of the dataset, if supplied, \"path\" will ignored"),
    compress: bool = typer.Option(False, "--compress", help="Compress output"),
    inplace: bool = typer.Option(False, "--inplace", help="Only keeping zipped file"),
    postgres_url: str = typer.Option(None, "--postgres-url", help="Postgres connection url"),
    version: str = typer.Option(None, "--version", "-v", help="Custom version input"),
) -> None:
# fmt: on
    """
    Archive a dataset from source to destination
    """
    if not name and not path:
        message = typer.style("\nPlease specify dataset NAME or PATH to configuration\n", fg=typer.colors.RED)
        typer.echo(message)
    else:
        a = Archive()
        a(
            path=path,
            output_format=output_format,
            push=push,
            clean=clean,
            latest=latest,
            name=name,
            compress=compress,
            postgres_url=postgres_url,
            version=version,
        )


def run() -> None:
    """Run commands."""
    app()

import os
import time
from typing import Optional

import typer

from . import aws_access_key_id, aws_s3_bucket, aws_s3_endpoint, aws_secret_access_key
from .archive import Archive
from .s3 import S3

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
            inplace=inplace,
            postgres_url=postgres_url,
            version=version,
        )

# fmt: off
@app.command()
def delete(
    name: str = typer.Option(None, "--name", "-n", help="Name of the dataset to remove"),
    version: str = typer.Option(None, "--version", "-v", help="Version of dataset to remove. \
        If not specified, all versions of a particular dataset will be deleted"),
    extension: str = typer.Option(None, "--extension", "-e", help="Extension of file to remove. \
        If not specified, all files of a particular version will be deleted"),
    key: str = typer.Option(None, "--key", "-k", help="Full key of dataset to remove. \
        If provided, will take precedent over the other 3 optional arguments"),
) -> None:
# fmt: on
    """
    Delete a file from s3 library
    """
    s3 = S3(aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket)
    if key:
        typer.echo(f"Deleting: {key}")
        s3.rm(key)
    elif name:
        keys = s3.ls(f"datasets/{name}/")
        if version:
            keys = [k for k in keys if (k.split("/")[2] == version)]
            if extension:
                keys = [k for k in keys if (k.split(".")[1] == extension)]
        message = "\n\t".join(keys)
        typer.echo(f"Deleting:\n\t{message}")
        s3.rm(*keys)

def run() -> None:
    """Run commands."""
    app()

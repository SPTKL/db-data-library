import time
import typer
import os

app = typer.Typer()


@app.command()
def ingest(name: str, config: str):
    """
    ingest a dataset from source to destination
    """
    typer.echo(f"ingesting {name} using {config} ...")


@app.command()
def show(name: str):
    """
    show versions available for given dataset
    """
    typer.echo(f"showing {name} ...")


@app.command()
def load(name: str):
    """
    load a dataset from s3/database to a build database
    """
    typer.echo(f"loading {name} to database ...")


def run() -> None:
    """Run commands."""
    app()

from pathlib import Path
import click

from doclint.services.process_python import process


def output_error(text: str):
    click.secho(text, fg="red", err=True)


def output_warning(text: str):
    click.secho(text, fg="yellow", err=True)


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def analyse_file(filename: str):
    """Analyse the complexity of a Python file's docstrings."""
    path = Path(filename)
    output_value = process(path, output_error, output_warning)
    exit(output_value)


def main():
    analyse_file()

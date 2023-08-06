# -*- coding: utf-8 -*-

"""Console script for ml-ml_handy."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for ml-ml_handy."""
    click.echo("Replace this message by putting your code into "
               "ml-ml_handy.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

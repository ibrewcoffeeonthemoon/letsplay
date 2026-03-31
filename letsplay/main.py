import importlib.metadata as meta

import typer

from .steam import app as steam

NAME = 'letsplay'


app = typer.Typer(
    name=NAME,
    no_args_is_help=True,
    help='A game launcher automation tool for Steam (potentially any other game launcher)',
)


@app.command(help='show version info')
def version() -> None:
    print(f'v{meta.version(NAME)}')


app.add_typer(steam)

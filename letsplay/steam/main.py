import typer

app = typer.Typer()


@app.command(
    no_args_is_help=True,
    help='Launch steam games',
)
def steam() -> None:
    pass

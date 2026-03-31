from typing import Annotated

import typer
from typer import Argument, Option

app = typer.Typer()


@app.command(
    no_args_is_help=True,
    help='Launch steam games',
)
def steam(
    app_id: Annotated[int, Argument(help='The Steam App ID of the game to launch')],
    show_steam: Annotated[bool, Option('--show-steam', help='Show steam window')] = False,
    mangohud: Annotated[bool, Option('--mangohud', help='Enable MangoHUD overlay')] = False,
    launch_options: Annotated[str, Option('--launch-options', '-l', help='Additional Steam launch arguments')] = '',
) -> None:
    # command to use
    cmd = ' '.join((part for part in (
        'mangohud' if mangohud else '',
        'steam',
        '' if show_steam else '-silent',
        f'-applaunch {app_id}',
    ) if part))
    print(f'{cmd=}')
    print(f'{launch_options=}')

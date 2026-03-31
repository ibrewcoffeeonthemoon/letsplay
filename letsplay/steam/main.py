import os
from typing import Annotated

import typer
from typer import Argument, Option

from .config import SteamLocalConfig

app = typer.Typer()


@app.command(
    no_args_is_help=True,
    help='Launch steam games',
)
def steam(
    app_id: Annotated[int, Argument(help='The Steam App ID of the game to launch')],
    show_steam: Annotated[bool, Option('--show-steam', help='Show steam window')] = False,
    mangohud: Annotated[bool, Option('--mangohud', help='Enable MangoHUD overlay using the prefix method')] = False,
    launch_options: Annotated[str | None, Option('--launch-options', '-l', help='Additional Steam launch arguments')] = None,
) -> None:
    # preprocess
    _app_id = str(app_id)

    # modify steam local config
    with SteamLocalConfig(_app_id) as cfg:
        if launch_options:
            cfg.set_launch_options(launch_options)

    # run the game
    cmd = [part for part in (
        'mangohud' if mangohud else None,
        'steam',
        None if show_steam else '-silent',
        '-applaunch', _app_id,
    ) if part is not None]
    # replace the python process with the game process
    os.execvp(cmd[0], cmd)

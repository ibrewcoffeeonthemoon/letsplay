from typing import Annotated, Literal

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
    mangohud: Annotated[Literal['env', 'cmd'] | None, Option('--mangohud', help='Enable MangoHUD overlay')] = None,
    launch_options: Annotated[str | None, Option('--launch-options', '-l', help='Additional Steam launch arguments')] = None,
) -> None:
    # 1. kill all
    # pkill -e -f "steam|gamescope|steamvr|wine"

    # modify steam local config
    with SteamLocalConfig(app_id) as cfg:
        if launch_options:
            cfg.set_launch_options('some new launch options')

    # 3. command to use
    cmd = ' '.join((part for part in (
        'mangohud' if mangohud == 'cmd' else 'MANGOHUD=1' if mangohud == 'env' else '',
        'steam',
        '' if show_steam else '-silent',
        f'-applaunch {app_id}',
    ) if part))
    print(f'{cmd=}')
    print(f'{launch_options=}')
    # execute this command

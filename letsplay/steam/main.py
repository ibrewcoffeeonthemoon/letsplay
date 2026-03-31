from typing import Annotated, Literal

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
    mangohud: Annotated[Literal['env', 'cmd'] | None, Option('--mangohud', help='Enable MangoHUD overlay')] = None,
    launch_options: Annotated[str | None, Option('--launch-options', '-l', help='Additional Steam launch arguments')] = None,
) -> None:
    # 1. kill all
    # pkill -e -f "steam|gamescope|steamvr|wine"

    # 2. launch_options
    if launch_options:
        # change launch options in steam config:
        # ~/.local/share/Steam/userdata/1441367642/config/localconfig.vdf
        pass

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

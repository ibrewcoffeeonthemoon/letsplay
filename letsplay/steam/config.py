import shutil
import subprocess
from pathlib import Path
from typing import Any, Self

import vdf  # type: ignore


class SteamLocalConfig:
    def __init__(self, app_id: str) -> None:
        self._app_id = app_id

    def __enter__(self) -> Self:
        # kill steam
        self._kill_steam_related_apps()
        # load config data
        self._path = self._resolve_path()
        self._data = self._load()
        return self

    def __exit__(self, *_) -> None:
        self._save()

    def _kill_steam_related_apps(self) -> None:
        # cmd: pkill -e -f "steam|gamescope|steamvr|wine"
        subprocess.run(['pkill', 'steam|gamescope|wine'])

    def _resolve_path(self) -> Path:
        base_path = Path('~/.local/share/Steam/userdata/').expanduser()
        user_config_paths = sorted([
            p / 'config/localconfig.vdf'
            for p in base_path.iterdir()
            if p.is_dir() and p.name.isdigit() and p.name != '0'
        ], key=lambda p: p.stat().st_mtime)
        return user_config_paths[-1]

    def _load(self) -> dict[str, Any]:
        with open(self._path) as f:
            return vdf.load(f)

    def _save(self) -> None:
        # create backup
        shutil.copy2(self._path, self._path.with_suffix(self._path.suffix + '.bak'))
        # write file
        with open(self._path, 'w') as f:
            vdf.dump(self._data, f, pretty=True)

    def set_launch_options(self, val: str) -> None:
        apps = self._data['UserLocalConfigStore']['Software']['Valve']['Steam']['apps']
        app = apps[self._app_id]
        app['LaunchOptions'] = val

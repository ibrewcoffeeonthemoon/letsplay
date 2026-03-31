import shutil
from pathlib import Path
from typing import Any, Self

import rich
import vdf


class SteamLocalConfig:
    def __init__(self, app_id: int) -> None:
        self._app_id = str(app_id)

    def __enter__(self) -> Self:
        self.path = self._resolve_path()
        self.data = self._load()
        return self

    def __exit__(self, *_) -> None:
        # self._save()
        pass

    def _resolve_path(self) -> Path:
        base_path = Path('~/.local/share/Steam/userdata/').expanduser()
        user_config_paths = sorted([
            p / 'config/localconfig.vdf'
            for p in base_path.iterdir()
            if p.is_dir() and p.name.isdigit() and p.name != '0'
        ], key=lambda p: p.stat().st_mtime)
        return user_config_paths[-1]

    def _load(self) -> dict[str, Any]:
        with open(self.path) as f:
            return vdf.load(f)

    def _save(self) -> None:
        shutil.copy2(self.path, self.path.with_suffix(self.path.suffix + '.bak'))
        with open(self.path, 'w') as f:
            vdf.dump(self.data, f, pretty=True)

    def set_launch_options(self, val: str) -> None:
        apps = self.data['UserLocalConfigStore']['Software']['Valve']['Steam']['apps']
        app = apps[self._app_id]
        app['LaunchOptions'] = val

from pathlib import Path
from typing import Any, Self

import rich
import vdf


class SteamLocalConfig:
    def __init__(self) -> None:
        self.path = self._resolve_path()
        self.data = self._load()

    def __enter__(self) -> Self:
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
        if self.data is None:
            rich.print('[red]Invalid data, abort saving to config file[/]')
            return
        with open(self.path, 'w') as f:
            vdf.dump(self.data, f, pretty=True)

    def set_launch_option(self, app_id: int, val: str) -> None:
        breakpoint()

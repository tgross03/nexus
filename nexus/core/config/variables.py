# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (c) 2026 Tom Groß


from pathlib import Path
from typing import Any

from mergedeep import merge

from .toml import TOMLConfiguration


class VariableLibrary:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        self._path: Path = Path.home() / ".nexus/config/variables.toml"
        self._config = TOMLConfiguration(self._path, create_if_not_exists=True)

        self.generate(regenerate=False)

    def generate(self, regenerate: bool = False) -> None:
        self._path.parent.mkdir(exist_ok=True, parents=True)

        if regenerate:
            self._path.unlink(missing_ok=True)

        if not self.exists():
            self._path.touch()

        current_content = self._config.asdict()

        content = {
            "cli": {
                "color_palette": "latte",
                "rich": {"palette": "solarized", "style": "box"},
            },
            "exceptions": {
                "show_locals": False,
            },
        }

        self._config.dump(
            content if regenerate else dict(merge({}, content, current_content))
        )

    @classmethod
    def get_config(cls) -> TOMLConfiguration:
        instance = cls()
        return instance._config

    @classmethod
    def get_path(cls) -> Path:
        instance = cls()
        return instance._path

    @classmethod
    def get_variable(cls, key: str) -> Any:
        instance = cls()
        return instance._config[key]

    @classmethod
    def set_variable(cls, key: str, value: Any) -> None:
        instance = cls()
        instance._config[key] = value

    @classmethod
    def exists(cls) -> bool:
        instance = cls()
        return instance._config.exists()

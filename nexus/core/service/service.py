import uuid
from os import PathLike
from pathlib import Path

from nexus.core.bot.manager import BotManager
from nexus.core.config import TOMLConfiguration
from nexus.core.module.manager import ModuleManager
from nexus.core.plugin.manager import PluginManager
from nexus.core.service.register import ServiceRegister


class Service:
    def __init__(
        self,
        name: str,
        parent_dir: PathLike | str,
    ) -> None:
        self._name: str = name
        self._root_dir: Path = Path(parent_dir) / self._name
        self._uuid: uuid.UUID | None = None

        self._main_config: TOMLConfiguration = TOMLConfiguration(
            self._root_dir / "nexus.toml"
        )

        if "uuid" in self._main_config:
            self._uuid = uuid.UUID(str(self._main_config["uuid"]))

        self._bot_config: TOMLConfiguration = TOMLConfiguration(
            self._root_dir / "bots.toml"
        )
        self._module_config: TOMLConfiguration = TOMLConfiguration(
            self._root_dir / "modules.toml"
        )
        self._plugin_config: TOMLConfiguration = TOMLConfiguration(
            self._root_dir / "plugins.toml"
        )

        self._bot_manager: BotManager = BotManager(bot_config=self._bot_config)
        self._module_manager: ModuleManager = ModuleManager(
            module_config=self._module_config
        )
        self._plugin_manager: PluginManager = PluginManager(
            plugin_config=self._plugin_config
        )

    def reset_config(self) -> None:
        self._main_config.dump({"uuid": str(self._uuid)})

    def exists(self) -> bool:
        return self._root_dir.exists() and self._root_dir.is_dir()

    def is_valid(self) -> bool:
        return (
            self.exists()
            and self._main_config.exists()
            and self._bot_config.exists()
            and self._module_config.exists()
            and self._plugin_config.exists()
            and (self._root_dir / "plugins").exists()
            and (self._root_dir / "config").exists()
            and (self._root_dir / "config/modules").exists()
            and (self._root_dir / "config/plugins").exists()
        )

    def initialize(self) -> None:
        self._uuid = uuid.uuid4()

        self._root_dir.mkdir()
        (self._root_dir / "plugins").mkdir()
        (self._root_dir / "config").mkdir()

        (self._root_dir / "config/modules").mkdir()
        (self._root_dir / "config/plugins").mkdir()

        self._main_config.create()

        self._bot_config.create()
        self._module_config.create()
        self._plugin_config.create()

        self.reset_config()

        self._bot_manager.reset_config()
        self._module_manager.reset_config()
        self._plugin_manager.reset_config()
        ServiceRegister().register(self)

    @classmethod
    def from_path(cls, path: PathLike | str) -> "Service":
        path = Path(path)
        return cls(name=path.name, parent_dir=path.parent)

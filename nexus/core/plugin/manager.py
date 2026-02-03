from nexus.core.config.toml import TOMLConfiguration


class PluginManager:
    def __init__(self, plugin_config: TOMLConfiguration) -> None:
        self._plugin_config: TOMLConfiguration = plugin_config

    def reset_config(self) -> None:
        self._plugin_config.dump(
            {
                "git": [],
                "local": [],
                "pypi": [],
            }
        )

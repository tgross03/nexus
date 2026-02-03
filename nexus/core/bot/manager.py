from nexus.core.config.toml import TOMLConfiguration


class BotManager:
    def __init__(self, bot_config: TOMLConfiguration) -> None:
        self._bot_configuration: TOMLConfiguration = bot_config

    def reset_config(self) -> None:
        self._bot_configuration.dump(
            {
                "bots": [],
            }
        )

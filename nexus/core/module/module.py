from nexus.core.bot import Bot
from nexus.core.config.toml import TOMLConfiguration


class Module:
    def __init__(self, name: str, optional: bool, config: TOMLConfiguration) -> None:
        self._name: str = name
        self._optional: bool = optional
        self._enabled: bool = False

        self._config: TOMLConfiguration = config
        self._bots: list[Bot] = []

    def reset_config(self) -> None:
        self._config.create()
        self._config.dump({})

    def is_optional(self) -> bool:
        return self._optional

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    def add_bot(self, bot: Bot) -> None:
        self._bots.append(bot)

    def remove_bot(self, bot: Bot) -> None:
        self._bots.remove(bot)

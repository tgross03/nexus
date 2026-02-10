from discord import Client, Intents


class Bot(Client):
    def __init__(self, name: str, intents: list[str], default_intents: bool) -> None:

        self.name: str = name

        self._include_default_intents: bool = default_intents
        self._intents: list[str] = intents

        super().__init__(intents=self.get_intents())

    def get_intents(self) -> Intents:
        intents = Intents.default() if self._include_default_intents else Intents.none()

        for intent in self._intents:
            target_value = True

            # Check if intent is negated
            if intent.startswith("!"):
                target_value = False
                intent = intent.removeprefix("!")

            intent = intent.lower()

            if intent not in Intents.VALID_FLAGS:
                raise ValueError(f"The intent '{intent}' does not exist!")

            setattr(intents, intent, target_value)

        return intents

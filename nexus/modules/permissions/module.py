from nexus.core.config.toml import TOMLConfiguration
from nexus.core.module import module


class Module(module.Module):
    def __init__(self, config: TOMLConfiguration) -> None:
        super().__init__(name="Permissions", optional=True, config=config)

    def enable(self) -> None:
        pass

    def disable(self) -> None:
        pass

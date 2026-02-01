__all__ = ["InvalidConfigurationError"]


class InvalidConfigurationError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

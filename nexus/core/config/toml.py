import tomllib
from enum import Enum
from os import PathLike
from pathlib import Path

import tomli_w

from nexus.core.exceptions.generic import InvalidConfigurationError

__all__ = ["TOMLConfiguration", "MissingKeyPolicy"]


class MissingKeyPolicy(Enum):
    ERROR = 1
    RETURN_NONE = 2


class TOMLConfiguration:
    def __init__(
        self,
        path: PathLike,
        create_if_not_exists: bool = False,
        missing_key_policy: MissingKeyPolicy = MissingKeyPolicy.ERROR,
    ):
        """
        Initializes a new TOML configuration.

        Parameters
        ----------

        path : PathLike
            The path to the toml file.

        create_if_not_exists : bool, optional
            Whether to create the corresponding file if it does not exist.
            Default is ``False``.

        missing_key_policy : MissingKeyPolicy | str, optional
            The policy to react to missing keys.
            Default is ``MissingKeyPolicy.ERROR`` meaning that an error will be raised.

        """

        self._path: Path = Path(path)

        if self._path.suffix != ".toml":
            raise InvalidConfigurationError(
                "The given file has an incorrect file suffix "
                f"(is '{self._path.suffix}')! Has to be 'toml'"
            )

        if not self.exists() and create_if_not_exists:
            self._path.mkdir(exist_ok=True, parents=True)
            self._path.touch(exist_ok=True)

        self._missing_key_policy: MissingKeyPolicy = (
            missing_key_policy
            if isinstance(missing_key_policy, MissingKeyPolicy)
            else MissingKeyPolicy[missing_key_policy]
        )

    def exists(self) -> bool:
        """
        Checks whether the file exists.

        Returns
        -------

        bool : Whether the file exists.
        """
        return self._path.exists() and self._path.is_file()

    def __getitem__(self, key: str) -> object:
        content = self.asdict()

        keys = key.split(".")

        for key in keys:
            if not isinstance(content, dict) or key not in content:
                return self._handle_missing_key(key=key)

            content = content[key]

        return content

    def _handle_missing_key(self, key: str) -> None:
        match self._missing_key_policy:
            case MissingKeyPolicy.ERROR:
                raise KeyError(f"Invalid key: '{key}'")
            case MissingKeyPolicy.RETURN_NONE:
                return None

    def __setitem__(self, key: str, value: object) -> None:
        content = self.asdict()

        keys = key.split(".")

        content_dict = content
        for kidx, key in zip(range(len(keys)), keys):
            if not isinstance(content_dict, dict) or key not in content_dict:
                raise KeyError(f"Invalid key: '{key}'")

            if kidx == len(keys) - 1:
                if (
                    isinstance(content_dict[key], dict) and not isinstance(value, dict)
                ) or (
                    isinstance(value, dict) and not isinstance(content_dict[key], dict)
                ):
                    raise TypeError(
                        "The type of the value that to be set must be the "
                        "same of the current value!"
                    )

                content_dict[key] = value
            else:
                content_dict = content_dict[key]

        with open(self._path, "wb") as tomlf:
            tomli_w.dump(content, tomlf)

    def __contains__(self, key: str) -> bool:
        content = self.asdict()
        keys = key.split(".")

        for key in keys:
            if key not in content:
                return False

            content = content[key]

        return True

    def asdict(self) -> dict:
        """
        Provides the content of the TOML file as a dictionary.

        Returns
        -------

        dict : The content of the TOML file.
        """
        with open(self._path, "rb") as tomlf:
            content = tomllib.load(tomlf)

        return content

    def dump(self, content: dict) -> None:
        """
        Dumps the given dictionary as content into the TOML file.

        Parameters
        ----------

        content : dict
            The content to dump into the file.
        """
        with open(self._path, "wb") as tomlf:
            tomli_w.dump(content, tomlf)

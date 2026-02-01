# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (c) 2026 Tom Groß

from nexus.cli.colors import RESET, get_default_palette

palette = get_default_palette()

__all__ = ["print_error_message", "ConfirmInput"]


def print_error_message(error: Exception, debug: bool) -> None:
    """
    Print error messages depending on the debug mode.
    If the debug mode is enabled, the exception is raised,
    resulting in a stack trace. Otherwise, an error message is printed.

    Parameters
    ----------

    error: Exception
        The exception to raise / print.

    debug: bool
        Whether debug mode is enabled.

    """
    if debug:
        raise error
    else:
        print(f"{palette.red}ERROR: {palette.maroon}{error.args[0]}{RESET}")


class ConfirmInput:
    def __init__(self, message: str, default_value: bool) -> None:
        self.message: str = message
        self.default_value: bool = default_value

    def _get_default_input(self) -> str:
        if self.default_value:
            return "y"
        else:
            return "n"

    def _get_suffix(self) -> str:
        true_str = "Y" if self.default_value else "y"
        false_str = "N" if not self.default_value else "n"
        return f"({true_str}/{false_str})"

    def _get_prompt(self) -> str:
        return f"{self.message} {self._get_suffix()} "

    def prompt(self) -> bool:
        confirmation = False
        valid_input = False

        while not valid_input:
            in_value = input(self._get_prompt())

            if in_value.lower() != "y" and in_value.lower() != "n" and in_value != "":
                print(
                    f"{palette.maroon}You have type y, n or nothing to proceed!{RESET}"
                )
                continue

            confirmation = (in_value or self._get_default_input().lower()) == "y"
            valid_input = True

        return confirmation

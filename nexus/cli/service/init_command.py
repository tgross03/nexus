from pathlib import Path

import rich_click as click

from nexus.cli.elements import print_error_message
from nexus.core.service.service import Service


@click.command("init", help="Initializes a new service.")
@click.argument("name", type=str)
@click.option(
    "--path",
    "-p",
    help=(
        "The parent directory at which to initialize the service. "
        "The directory structure will be 'PARENT_DIR/<name>'"
    ),
    default=Path.cwd(),
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
)
@click.option(
    "--import-config",
    help="The path to a valid export config. If none is given, an empty service will be created.",
    default=None,
    type=click.Path(exists=True, dir_okay=False, file_okay=True, path_type=Path),
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    help="Activate the debug log for the command "
    "to print full error traces in case of a problem.",
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Sets the verbosity level of the output.",
)
def init(
    name: str, path: Path, import_config: Path | None, debug: bool, verbose: int
) -> None:
    service = Service(name=name, parent_dir=path)
    try:
        service.initialize(verbose=verbose)
    except Exception as e:
        return print_error_message(error=e, debug=debug)

    return None

from pathlib import Path

import rich_click as click

from nexus.core.exceptions.services import ServiceExistsError
from nexus.core.service.register import ServiceRegister
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
def init(name: str, path: Path, import_config: Path | None) -> None:
    try:
        ServiceRegister().get_service_by_name(name=name)
        raise ServiceExistsError(
            "There is already a service with this name! Service names have to be unique."
        )
    except KeyError:
        pass

    service = Service(name=name, parent_dir=path)
    service.initialize()

    return None

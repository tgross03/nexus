import rich_click as click

from .init_command import init


@click.group(
    name="service", help="Actions related to initializing and managing services."
)
def command():
    pass


command.add_command(init)

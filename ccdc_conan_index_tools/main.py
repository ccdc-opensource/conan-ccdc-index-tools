from dataclasses import dataclass
from pathlib import Path
import click
from .commands.info import info
from .commands.build import build


@dataclass
class CliContext(object):
    index: click.Path


@click.group()
@click.option(
    "--index",
    envvar="LOCAL_CONAN_INDEX",
    help="Index folder",
    default=".",
    type=click.Path(),
)
@click.pass_context
def cli(ctx, index):
    ctx.obj = CliContext(index=index)


cli.add_command(info)
cli.add_command(build)

if __name__ == "__main__":
    cli()

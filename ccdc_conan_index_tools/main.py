from dataclasses import dataclass
from pathlib import Path
import click
from .commands.info import info
from .commands.build import build
from .commands.publish import publish
from .package_index import PackageIndex


@dataclass
class CliContext(object):
    index: PackageIndex
    conan_logging_level: str
    conan_user_home: Path


@click.group()
@click.option(
    "--index",
    envvar="LOCAL_CONAN_INDEX",
    help="Index folder",
    default=".",
    type=click.Path(),
)
@click.option(
    "--conan-logging-level",
    envvar="CONAN_LOGGING_LEVEL",
    help="Sets logging level for conan cli",
    type=click.Choice(
        ["critical", "error", "warning", "warn", "info", "debug"], case_sensitive=False
    ),
    default="critical",
)
@click.pass_context
def cli(ctx, index, conan_logging_level):
    try:
        package_index = PackageIndex(index)
    except FileNotFoundError as e:
        raise click.UsageError(f"Cannot find a valid package index in {index}: {e}")

    ctx.obj = CliContext(
        index=package_index,
        conan_logging_level=conan_logging_level,
        conan_user_home=None,
    )


cli.add_command(info)
cli.add_command(build)
cli.add_command(publish)

if __name__ == "__main__":
    cli()

from dataclasses import dataclass
from pathlib import Path
import asyncclick as click
from ccdc_conan_index_tools.commands.info import info
from ccdc_conan_index_tools.commands.build import build
from ccdc_conan_index_tools.commands.publish import publish
from ccdc_conan_index_tools.package_index import PackageIndex

# if 'CCDC_USERNAME' in os.environ:
#     artifactory_user = os.environ['CCDC_USERNAME']
# elif 'USER' in os.environ:
#     artifactory_user = os.environ['USER']
# elif 'USERNAME' in os.environ:
#     artifactory_user = os.environ['USERNAME']
# artifactory_api_key = os.environ["ARTIFACTORY_API_KEY"]


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


def main():
    cli()


if __name__ == "__main__":
    main()

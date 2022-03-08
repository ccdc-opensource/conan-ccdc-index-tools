import click
import os
import yaml
import json

default_index = os.environ.get("CCDC_CONAN_INDEX", None)


@click.group()
@click.option("--index", envvar="CCDC_CONAN_INDEX", help="Index folder", default=".")
@click.pass_context
def cli(ctx, index):
    ctx.obj = dict()
    ctx.obj["index"] = index
    pass


@cli.command()
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
)
@click.pass_context
def list(ctx, format):
    from ccdc_conan_index_tools.package_index import PackageIndex

    index = ctx.obj["index"]

    try:
        packages = PackageIndex(index).package_names
        if format == "yaml":
            click.echo(yaml.dump(packages))
        elif format == json:
            click.echo(json.dumps(packages))
    except FileNotFoundError as e:
        raise click.UsageError(f"Cannot find a valid package index in {index}: {e}")


if __name__ == "__main__":
    cli()

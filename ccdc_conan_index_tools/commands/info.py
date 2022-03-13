import click
import yaml
import json


@click.group()
def info():
    pass


@info.command()
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
)
@click.pass_context
def package(ctx, format):
    from ccdc_conan_index_tools.package_index import PackageIndex

    index = ctx.obj.index

    try:
        packages = PackageIndex(index).package_names
        if format == "yaml":
            click.echo(yaml.dump(packages))
        elif format == "json":
            click.echo(json.dumps(packages))
    except FileNotFoundError as e:
        raise click.UsageError(f"Cannot find a valid package index in {index}: {e}")


@info.command()
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
)
@click.argument("package-name", required=False)
@click.pass_context
def licence(ctx, format, package_name):
    from ccdc_conan_index_tools.package_index import PackageIndex
    from ccdc_conan_index_tools.conan_commands import (
        get_remote_package_licence,
        get_local_package_licence,
    )

    try:
        index = PackageIndex(ctx.obj.index)
    except FileNotFoundError as e:
        raise click.UsageError(f"Cannot find a valid package index in {index}: {e}")
    licences = {}
    package_names = index.package_names
    if package_name and package_name not in package_names:
        raise click.UsageError(f"{package_name} is not in the index")
    if package_name:
        package_names = [package_name]
    for package in package_names:
        definitions = index.definitions_for(package)
        if definitions.local_recipe:
            for version in definitions.versions:
                licence = get_local_package_licence(
                    conanfile_directory=definitions.recipe_path_for_version(version)
                )
                licences[f"{package}/{version}"] = licence
        else:
            for version in definitions.versions:
                licence = get_remote_package_licence(
                    package=package,
                    version=version,
                    remote=definitions.source_repository,
                )
                licences[f"{package}/{version}"] = licence

    if format == "yaml":
        click.echo(yaml.dump(licences))
    elif format == "json":
        click.echo(json.dumps(licences))

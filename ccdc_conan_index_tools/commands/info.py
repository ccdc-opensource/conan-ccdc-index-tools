import asyncclick as click
import yaml
import json
import sys


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
async def package(ctx, format):
    from ccdc_conan_index_tools.package_index import PackageIndex

    index = ctx.obj.index
    packages = index.package_names
    if format == "yaml":
        print(yaml.dump(packages))
    elif format == "json":
        print(json.dumps(packages))


@info.command()
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
)
@click.argument("package-name", required=False)
@click.pass_context
async def licence(ctx, format, package_name):
    from ccdc_conan_index_tools.conan_commands import (
        get_remote_package_licence,
        get_local_package_licence,
    )

    index = ctx.obj.index
    package_names = index.package_names
    if package_name and package_name not in package_names:
        raise click.UsageError(f"{package_name} is not in the index")
    if package_name:
        package_names = [package_name]
    if format == "json":
        sys.stdout.write("{")
    first = True
    for package in package_names:
        definitions = index.definitions_for(package)
        if definitions.local_recipe:
            for version in definitions.versions:
                licence = await get_local_package_licence(
                    conanfile_directory=definitions.recipe_path_for_version(version),
                    conan_user_home=ctx.obj.conan_user_home,
                    conan_logging_level=ctx.obj.conan_logging_level,
                )
                if format == "yaml":
                    sys.stdout.write(f"{package}/{version}: {licence}\n")
                elif format == "json":
                    if not first:
                        sys.stdout.write(", ")
                    sys.stdout.write(f'"{package}/{version}": {json.dumps(licence)}')
        else:
            for version in definitions.versions:
                licence = await get_remote_package_licence(
                    package=package,
                    version=version,
                    remote=definitions.source_repository,
                    conan_user_home=ctx.obj.conan_user_home,
                    conan_logging_level=ctx.obj.conan_logging_level,
                )
                if format == "yaml":
                    sys.stdout.write(f"{package}/{version}: {licence}\n")
                elif format == "json":
                    if not first:
                        sys.stdout.write(", ")
                    sys.stdout.write(f'"{package}/{version}": {json.dumps(licence)}')
        first = False
        if format == "json":
            sys.stdout.flush()
    if format == "json":
        print("}")
    sys.stdout.flush()

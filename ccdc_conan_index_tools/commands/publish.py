import asyncclick as click
from ccdc_conan_index_tools.build_definition import PackageBuildDefinitions
from ccdc_conan_index_tools.conan_commands import (
    publish_local_recipe,
    publish_remote_recipe,
)


@click.group()
def publish():
    pass


@publish.command()
@click.option("--destination-repository")
@click.argument("package-name", required=False)
@click.argument("package-version", required=False)
@click.pass_context
async def recipe(ctx, destination_repository, package_name, package_version):
    index = ctx.obj.index
    for package_name in [package_name] if package_name else index.package_names:
        definitions = index.definitions_for(package_name)
        versions = [package_version] if package_version else definitions.versions
        for version in versions:
            if definitions.local_recipe:
                print(f"Publishing local recipe {package_name}/{version}@")
                await publish_local_recipe(
                    definitions.recipe_path_for_version(version),
                    package_name,
                    version,
                    destination_repository=destination_repository,
                    conan_logging_level=ctx.obj.conan_logging_level,
                    conan_user_home=ctx.obj.conan_user_home,
                )
            else:
                print(
                    f"Publishing recipe {package_name}/{version}@ from {definitions.source_repository}"
                )
                await publish_remote_recipe(
                    package_name,
                    version,
                    definitions.source_repository,
                    destination_repository=destination_repository,
                    conan_logging_level=ctx.obj.conan_logging_level,
                    conan_user_home=ctx.obj.conan_user_home,
                )


@publish.command()
@click.option("--destination-repository")
@click.option("--build-type")
@click.option("--platform-combination")
@click.argument("package-name", required=True)
@click.argument("package-version", required=False)
@click.pass_context
def package(ctx, destination_repository, package_name, package_version):
    index = ctx.obj.index

import asyncclick as click
from ccdc_conan_index_tools.conan_commands import build_all_locally


@click.command()
@click.option("--build-type")
@click.option("--platform-combination")
@click.argument("package-name", required=True)
@click.argument("package-version", required=False)
@click.pass_context
async def build(ctx, build_type, platform_combination, package_name, package_version):
    index = ctx.obj.index

    definitions = index.definitions_for(package_name)
    if not definitions:
        raise click.UsageError(f"Cannot find {package_name} in index {ctx.obj.index}")

    if package_version:
        if package_version not in definitions.versions:
            raise click.UsageError(
                f"Cannot find {package_name} version {package_version} in {index}"
            )
        versions = [package_version]
    else:
        versions = definitions.versions
    if build_type:
        if build_type not in definitions.build_types:
            raise click.UsageError(
                f"Cannot find build type {build_type} for {package_name} in {index}"
            )
        build_types = [build_type]
    else:
        build_types = definitions.build_types
    if platform_combination:
        platform_combinations = [
            c
            for c in definitions.package_platform_combinations
            if c.name == platform_combination
        ]
        if not platform_combinations:
            raise click.UsageError(
                f"Cannot find any valid platform combinations for {package_name} in {index}"
            )
    else:
        platform_combinations = definitions.package_platform_combinations
    await build_all_locally(
        definitions=definitions,
        versions=versions,
        build_types=build_types,
        platform_combinations=platform_combinations,
    )

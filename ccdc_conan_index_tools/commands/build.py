import asyncclick as click
from ccdc_conan_index_tools.conan_commands import build_all_locally
from ccdc_conan_index_tools.logging import log_section


@click.command()
@click.option("--build-type")
@click.option(
    "--platform-combination",
    envvar="LCI_PLATFORM_COMBINATION",
)
@click.option(
    "--require-combination/--no-require-combination",
    default=False,
    help="Default is to not require a platform combination",
)
@click.option("--from-package", help="Build from a certain package in sequence")
@click.argument("package-name", required=False)
@click.argument("package-version", required=False)
@click.pass_context
async def build(
    ctx,
    build_type,
    platform_combination,
    require_combination,
    from_package,
    package_name,
    package_version,
):
    index = ctx.obj.index
    if package_name:
        sequence = [package_name]
    else:
        sequence = index.build_sequence
    if from_package:
        idx = sequence.index(from_package)
        sequence = sequence[idx:]

    for package_name in sequence:
        with log_section(f"Build of {package_name}"):
            definitions = index.definitions_for(package_name)
            if not definitions:
                raise click.UsageError(
                    f"Cannot find {package_name} in index {ctx.obj.index.directory}"
                )

            if package_version:
                if package_version not in definitions.versions:
                    raise click.UsageError(
                        f"Cannot find {package_name} version {package_version} in {index.directory}"
                    )
                versions = [package_version]
            else:
                versions = definitions.versions
            if build_type:
                if build_type not in definitions.build_types:
                    raise click.UsageError(
                        f"Cannot find build type {build_type} for {package_name} in {index.directory}"
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
                if require_combination and not platform_combinations:
                    raise click.UsageError(
                        f"Cannot find any valid platform combinations for {package_name} in {index.directory}"
                    )
            else:
                platform_combinations = definitions.package_platform_combinations
            await build_all_locally(
                definitions=definitions,
                versions=versions,
                build_types=build_types,
                platform_combinations=platform_combinations,
            )

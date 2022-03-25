import subprocess
import shutil
import os
from .build_definition import PackageBuildDefinitions, PlatformCombination
from click import echo

class ConanCommandException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def conan_command():
    return shutil.which("conan")


def get_conan_output(
    command_args,
    conan_user_home=None,
    conan_logging_level=None,
    macos_deployment_target=None,
    force_single_cpu_core=False,
    conan_username=None,
    conan_password=None,
):
    env = dict(os.environ)
    env.update({
        "NO_COLOR": "1",
        "CONAN_NON_INTERACTIVE": "1",
    })
    if conan_user_home:
        env["CONAN_USER_HOME"] = conan_user_home
    if conan_logging_level:
        env["CONAN_LOGGING_LEVEL"] = conan_logging_level
    if macos_deployment_target:
        env["MACOSX_DEPLOYMENT_TARGET"] = macos_deployment_target
    if force_single_cpu_core:
        env["CONAN_CPU_COUNT"] = "1"
    if conan_username:
        env["CONAN_LOGIN_USERNAME"] = conan_username
    if conan_password:
        env["CONAN_PASSWORD"] = conan_password

    ret = subprocess.run(
        args=[conan_command()] + command_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=env,
    )
    if ret.returncode != 0:
        raise ConanCommandException(
            f"Conan command {conan_command()} [{command_args}] returned {ret.returncode}\nStdout: {ret.stdout}\nStderr: {ret.stderr}"
        )
    return ret.stdout


def get_remote_package_licence(
    package, version, remote, conan_user_home=None, conan_logging_level=None
):
    ret = get_conan_output(
        ["inspect", "-r", remote, "-a", "license", f"{package}/{version}@"],
        conan_user_home=conan_user_home,
        conan_logging_level=conan_logging_level,
    )
    lines = [line for line in ret.splitlines() if "license: " in line]
    if not lines:
        return f"No License line in conan info for {package}/{version}@"
    return lines[0].replace("license: ", "")


def get_local_package_licence(
    conanfile_directory,
    conan_user_home=None,
    conan_logging_level=None,
):
    ret = get_conan_output(
        ["inspect", "-a", "license", conanfile_directory],
        conan_user_home=conan_user_home,
        conan_logging_level=conan_logging_level,
    )
    lines = [line for line in ret.splitlines() if "license: " in line]
    if not lines:
        return f"No license line in conan info for conanfile in {conanfile_directory}"
    return lines[0].replace("license: ", "")


def publish_local_recipe(
    conanfile_directory,
    package_name,
    package_version,
    destination_repository=None,
    conan_user_home=None,
    conan_logging_level=None,
):
    output = get_conan_output(
        ["export", conanfile_directory, f"{package_name}/{package_version}@"],
        conan_user_home=conan_user_home,
        conan_logging_level=conan_logging_level,
    )
    if destination_repository:
        output += "\n"
        output += get_conan_output(
            [
                "upload",
                f"{package_name}/{package_version}@",
                f"--remote={ destination_repository }",
                "--confirm",
            ],
            conan_user_home=conan_user_home,
            conan_logging_level=conan_logging_level,
        )


def publish_remote_recipe(
    package_name,
    package_version,
    source_repository,
    destination_repository=None,
    conan_user_home=None,
    conan_logging_level=None,
):
    output = get_conan_output(
        [
            "download",
            f"{package_name}/{package_version}@",
            f"--remote={ source_repository }",
            "--recipe",
        ],
        conan_user_home=conan_user_home,
        conan_logging_level=conan_logging_level,
    )
    if destination_repository:
        output += "\n"
        output += get_conan_output(
            [
                "upload",
                f"{package_name}/{package_version}@",
                f"--remote={ destination_repository }",
                "--confirm",
            ],
            conan_user_home=conan_user_home,
            conan_logging_level=conan_logging_level,
        )


def build_all_locally(
    definitions: PackageBuildDefinitions,
    versions: list,
    build_types: list,
    platform_combinations: list,
):
    for version in versions:
        for platform_combination in platform_combinations:
            # Pre-add any required packages
            if platform_combination.uses_yum and definitions.centos_yum_preinstall:
                all_yum = " ".join(definitions.centos_yum_preinstall)
                print(f"Installing {all_yum} with yum")
                subprocess.check_call(
                    ["sudo", "yum", "install", "-y"] + definitions.centos_yum_preinstall
                )

            if platform_combination.uses_brew:
                if definitions.macos_brew_preinstall:
                    all_brew = " ".join(definitions.macos_brew_preinstall)
                    print(f"Installing {all_brew} with brew")
                    subprocess.check_call(
                        ["brew", "install"] + definitions.macos_brew_preinstall
                    )
                if platform_combination.macos_xcode_version:
                    print(
                        f"sudo xcode-select -s /Applications/Xcode_{ platform_combination.macos_xcode_version }.app/Contents/Developer"
                    )
                    subprocess.check_call(
                        [
                            "sudo",
                            "xcode-select",
                            "-s",
                            f"/Applications/Xcode_{ platform_combination.macos_xcode_version }.app/Contents/Developer",
                        ]
                    )
            for build_type in build_types:
                build_locally(
                    definitions=definitions,
                    version=version,
                    build_type=build_type,
                    combination=platform_combination,
                )


def build_locally(
    definitions: PackageBuildDefinitions,
    version: str,
    build_type: str,
    combination: PlatformCombination,
):
    build_profile = combination.build_profile
    if build_type == "Debug":
        target_profile = combination.target_profile + "-debug"
    else:
        target_profile = combination.target_profile + "-release"

    conan_install_args = [
        "install",
        f"{definitions.name}/{version}@",
        "--profile:build",
        build_profile,
        "--profile:host",
        target_profile,
    ]

    additional_profiles = []
    additional_profiles.extend(
        definitions.additional_profiles_for_all_platform_combinations
    )
    if definitions.use_release_zlib_profile:
        if "msvc16" in target_profile:
            additional_profiles.append("windows-msvc16-release-zlib")
    for additional_profile in additional_profiles:
        conan_install_args += ["--profile", additional_profile]

    conan_install_args += [
        # f"--remote={ definitions.source_repository }",
        f"--build={ definitions.name }",
        "-s",
        f"build_type={ build_type }",
    ]

    for override in definitions.require_override:
        conan_install_args += ["--require-override", override]

    echo(f"Installing {definitions.name}/{version}@ in configuration {build_type}, combination {combination.name}")
    get_conan_output(
        conan_install_args,
        conan_user_home=None,
        conan_logging_level=None,
        macos_deployment_target=combination.macos_deployment_target,
        force_single_cpu_core=definitions.force_single_cpu_core_for_debug_builds,
    )

    if definitions.local_recipe:
        echo(f"Testing {definitions.name}/{version}@ in configuration {build_type}, combination {combination.name}")
        conan_test_args = [
            "test",
            f"{definitions.recipe_path_for_version(version)}/test_package",
            f"{definitions.name}/{version}@",
            "--profile:build",
            build_profile,
            "--profile:host",
            target_profile,
        ]
        for additional_profile in additional_profiles:
            conan_test_args += ["--profile", additional_profile]
        conan_test_args += [
            "-s",
            f"build_type={ build_type }",
        ]
        get_conan_output(
            conan_test_args,
            conan_user_home=None,
            conan_logging_level=None,
            macos_deployment_target=combination.macos_deployment_target,
            force_single_cpu_core=definitions.force_single_cpu_core_for_debug_builds,
        )

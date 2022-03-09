import os
from ccdc_conan_index_tools.build_definition import PackageBuildDefinitions

recipe_loading_dir = os.path.join(os.path.dirname(__file__), "recipe_loading")
defaults = os.path.join(recipe_loading_dir, "index-defaults.yml")


def test_read_recipe_mostly_defaults():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "sample1.yml"
    )
    assert definitions.name == "sample1"
    assert not definitions.local_recipe
    assert definitions.source_repository == "public-conan-center"
    assert definitions.versions == ["10.12.1"]
    assert definitions.build_types == ["Release", "Debug", "RelWithDebInfo"]
    assert not definitions.header_only
    assert definitions.macos_deployment_target is None
    assert len(definitions.centos_yum_preinstall) == 0
    assert len(definitions.macos_brew_preinstall) == 0
    assert len(definitions.require_override) == 0
    assert not definitions.force_single_cpu_core_for_debug_builds
    assert not definitions.use_release_zlib_profile
    assert len(definitions.additional_profiles_for_all_platform_combinations) == 0
    assert not definitions.split_by_build_type
    assert (
        definitions.conan_config_git_source
        == "https://github.com/ccdc-opensource/conan-ccdc-common-configuration.git"
    )
    assert definitions.conan_config_git_branch == "main"


def test_read_recipe_header_only():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "header-only.yml"
    )
    assert definitions.name == "header-only"
    assert definitions.source_repository == "public-conan-center"
    assert definitions.header_only
    assert not definitions.split_by_build_type


def test_read_recipe_build_types():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "build-types.yml"
    )
    assert definitions.name == "build-types"
    assert not definitions.local_recipe
    assert definitions.build_types == ["Release"]


def test_read_recipe_macos_deployment_target():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "macos-dep-target.yml"
    )
    assert definitions.name == "macos-dep-target"
    assert definitions.macos_deployment_target == "10.15"


def test_read_recipe_centos_yum_preinstall():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "centos-yum-preinstall.yml"
    )
    assert definitions.name == "centos-yum-preinstall"
    assert definitions.centos_yum_preinstall == ["which"]


def test_read_recipe_macos_brew_preinstall():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "macos-brew-preinstall.yml"
    )
    assert definitions.name == "macos-brew-preinstall"
    assert definitions.macos_brew_preinstall == ["python3"]


def test_read_recipe_require_override():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "require-override.yml"
    )
    assert definitions.name == "require-override"
    assert definitions.require_override == ["expat/2.4.6@"]


def test_read_recipe_force_single_cpu_core_for_debug_builds():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "force-single-core-for-debug-builds.yml"
    )
    assert definitions.name == "force-single-core-for-debug-builds"
    assert definitions.force_single_cpu_core_for_debug_builds


def test_read_recipe_use_release_zlib_profile():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "use-release-zlib-profile.yml"
    )
    assert definitions.name == "use-release-zlib-profile"
    assert definitions.use_release_zlib_profile


def test_read_recipe_additional_profiles():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "additional-profiles.yml"
    )
    assert definitions.name == "additional-profiles"
    assert definitions.additional_profiles_for_all_platform_combinations == [
        "weird-customisation"
    ]


def test_read_recipe_all_combinations():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "combinations-all.yml"
    )
    assert definitions.name == "combinations-all"
    assert len(definitions.default_platform_combinations) == 3
    assert len(definitions.all_package_platform_combinations) == 3
    assert (
        definitions.default_platform_combinations
        == definitions.all_package_platform_combinations
    )
    # there's a limit in the defaults
    assert len(definitions.package_platform_combinations) == 2


def test_read_recipe_limit_combinations():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "combinations-limit.yml"
    )
    assert definitions.name == "combinations-limit"
    assert (
        definitions.default_platform_combinations
        != definitions.package_platform_combinations
    )
    assert len(definitions.package_platform_combinations) == 2
    assert definitions.package_platform_combinations[0].name == "combi-2"
    assert definitions.package_platform_combinations[1].name == "combi-3"


def test_read_recipe_override_combinations():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "combinations-override.yml"
    )
    assert definitions.name == "combinations-override"
    # there's a limit in the defaults
    assert (
        definitions.default_platform_combinations
        != definitions.all_package_platform_combinations
    )
    assert len(definitions.package_platform_combinations) == 1
    assert definitions.package_platform_combinations[0].name == "combi-2"


def test_read_recipe_override_limit_combinations():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "combinations-limit-override.yml"
    )
    assert definitions.name == "combinations-limit-override"
    assert (
        definitions.default_platform_combinations
        != definitions.package_platform_combinations
    )
    assert len(definitions.package_platform_combinations) == 1
    assert definitions.package_platform_combinations[0].name == "override-2"


def test_read_recipe_override_git_config():
    definitions = PackageBuildDefinitions.from_yaml(
        defaults, recipe_loading_dir, "git-config.yml"
    )
    assert definitions.name == "git-config"
    assert (
        definitions.conan_config_git_source
        == "https://github.com/ccdc-opensource/conan-alternative-configuration.git"
    )
    assert definitions.conan_config_git_branch == "patch-1"


def test_read_local_recipe_one_version():
    definitions = PackageBuildDefinitions.from_local_recipe_directory(
        defaults, os.path.join(recipe_loading_dir, "local-recipe-one-version")
    )
    assert definitions.name == "local-recipe-one-version"
    assert definitions.local_recipe
    assert definitions.source_repository is None
    assert definitions.versions == ["one version"]
    assert definitions.recipe_path_for_version("one version").endswith("all")
    assert definitions.build_types == ["Release", "Debug", "RelWithDebInfo"]
    assert not definitions.header_only
    assert definitions.macos_deployment_target is None
    assert len(definitions.centos_yum_preinstall) == 0
    assert len(definitions.macos_brew_preinstall) == 0
    assert len(definitions.require_override) == 0
    assert not definitions.force_single_cpu_core_for_debug_builds
    assert not definitions.use_release_zlib_profile
    assert len(definitions.additional_profiles_for_all_platform_combinations) == 0
    assert not definitions.split_by_build_type


def test_read_local_recipe_header_only():
    definitions = PackageBuildDefinitions.from_local_recipe_directory(
        defaults,
        os.path.join(recipe_loading_dir, "local-header-only-recipe-one-version"),
    )
    assert definitions.name == "local-header-only-recipe-one-version"
    assert definitions.local_recipe
    assert definitions.header_only


def test_read_local_recipe_needs_artifactory_api_key():
    definitions = PackageBuildDefinitions.from_local_recipe_directory(
        defaults, os.path.join(recipe_loading_dir, "local-needs-artifactory-api-key")
    )
    assert definitions.name == "local-needs-artifactory-api-key"
    assert definitions.needs_artifactory_api_key


def test_read_local_recipe_additional_profiles():
    definitions = PackageBuildDefinitions.from_local_recipe_directory(
        defaults,
        os.path.join(
            recipe_loading_dir, "local-recipe-additional-profiles-for-all-platforms"
        ),
    )
    assert definitions.name == "local-recipe-additional-profiles-for-all-platforms"
    assert definitions.additional_profiles_for_all_platform_combinations == [
        "static-library"
    ]


def test_read_local_recipe_build_types_zlib_profile():
    definitions = PackageBuildDefinitions.from_local_recipe_directory(
        defaults,
        os.path.join(recipe_loading_dir, "local-recipe-build-types-zlib-profile"),
    )
    assert definitions.name == "local-recipe-build-types-zlib-profile"
    assert definitions.use_release_zlib_profile
    assert definitions.build_types == ["Release", "Debug"]


def test_read_local_recipe_complex():
    definitions = PackageBuildDefinitions.from_local_recipe_directory(
        defaults,
        os.path.join(recipe_loading_dir, "local-recipe-complex"),
    )
    assert definitions.name == "local-recipe-complex"
    assert definitions.versions == ["3.7.0.8"]
    assert definitions.macos_deployment_target == "10.13"
    assert definitions.additional_profiles_for_all_platform_combinations == [
        "povray-options"
    ]
    assert definitions.build_types == ["Release"]
    assert len(definitions.all_package_platform_combinations) == 2


def test_read_local_recipe_multi_folders():
    definitions = PackageBuildDefinitions.from_local_recipe_directory(
        defaults, os.path.join(recipe_loading_dir, "local-recipe-multi-folders")
    )
    assert definitions.name == "local-recipe-multi-folders"
    assert definitions.local_recipe
    assert definitions.versions == ["3.0.1", "1.1.1k", "1.1.1l", "1.1.1m"]
    assert definitions.recipe_path_for_version("3.0.1").endswith("3.x.x")
    assert definitions.recipe_path_for_version("1.1.1k").endswith("all")
    assert definitions.recipe_path_for_version("1.1.1l").endswith("all")
    assert definitions.recipe_path_for_version("1.1.1m").endswith("all")
    assert definitions.build_types == ["Release", "Debug", "RelWithDebInfo"]


def test_read_local_recipe_split_by_build_type():
    definitions = PackageBuildDefinitions.from_local_recipe_directory(
        defaults, os.path.join(recipe_loading_dir, "local-recipe-split-by-build-type")
    )
    assert definitions.name == "local-recipe-split-by-build-type"
    assert definitions.use_release_zlib_profile
    assert definitions.build_types == ["Release", "Debug"]
    assert definitions.split_by_build_type

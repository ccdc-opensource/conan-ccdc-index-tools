import os
from typing import Dict, List


def _listify(inp):
    if inp is None:
        return None
    if type(inp) == list:
        return inp
    return [inp]


class PlatformCombination:
    def __init__(self, yaml_dict: dict):
        self._name = yaml_dict["name"]
        self._build_profile = yaml_dict["build_profile"]
        self._target_profile = yaml_dict["target_profile"]

    def __eq__(self, other):
        return (
            self._name == other._name
            and self._build_profile == other._build_profile
            and self._target_profile == other._target_profile
        )

    @property
    def name(self):
        return self._name

    @property
    def build_profile(self):
        return self._build_profile

    @property
    def target_profile(self):
        return self._target_profile


class PackageBuildDefinitions:
    def __init__(
        self,
        name: str,
        local_recipe: bool,
        source_repository: str,
        versions: List,
        header_only: bool,
        build_types: List,
        macos_deployment_target: str,
        centos_yum_preinstall: List,
        macos_brew_preinstall: List,
        require_override: List,
        force_single_cpu_core_for_debug_builds: bool,
        use_release_zlib_profile: bool,
        additional_profiles_for_all_platform_combinations: List,
        default_platform_combinations: List,
        package_platform_combinations: List,
        limit_to_platform_combinations: List,
        needs_artifactory_api_key: bool,
        local_recipe_paths_by_version: Dict,
        split_by_build_type: bool,
        conan_config_git_source: str,
        conan_config_git_branch: str,
    ):
        self._name = name
        self._local_recipe = local_recipe
        self._source_repository = source_repository
        self._versions = versions
        self._header_only = header_only
        self._build_types = build_types
        self._macos_deployment_target = macos_deployment_target
        self._centos_yum_preinstall = centos_yum_preinstall
        self._macos_brew_preinstall = macos_brew_preinstall
        self._require_override = require_override
        self._force_single_cpu_core_for_debug_builds = (
            force_single_cpu_core_for_debug_builds
        )
        self._use_release_zlib_profile = use_release_zlib_profile
        self._additional_profiles_for_all_platform_combinations = (
            additional_profiles_for_all_platform_combinations
        )
        self._default_platform_combinations = default_platform_combinations
        self._package_platform_combinations = package_platform_combinations
        self._limit_to_platform_combinations = limit_to_platform_combinations
        self._needs_artifactory_api_key = needs_artifactory_api_key
        self._local_recipe_paths_by_version = local_recipe_paths_by_version
        self._split_by_build_type = split_by_build_type
        self._conan_config_git_source = conan_config_git_source
        self._conan_config_git_branch = conan_config_git_branch

    @property
    def name(self):
        return self._name

    @property
    def local_recipe(self):
        return self._local_recipe

    @property
    def source_repository(self):
        return self._source_repository

    @property
    def versions(self):
        return self._versions

    @property
    def header_only(self):
        return self._header_only

    @property
    def build_types(self):
        return self._build_types

    @property
    def macos_deployment_target(self):
        return self._macos_deployment_target

    @property
    def centos_yum_preinstall(self):
        return self._centos_yum_preinstall

    @property
    def macos_brew_preinstall(self):
        return self._macos_brew_preinstall

    @property
    def require_override(self):
        return self._require_override

    @property
    def force_single_cpu_core_for_debug_builds(self):
        return self._force_single_cpu_core_for_debug_builds

    @property
    def use_release_zlib_profile(self):
        return self._use_release_zlib_profile

    @property
    def additional_profiles_for_all_platform_combinations(self):
        return self._additional_profiles_for_all_platform_combinations

    @property
    def needs_artifactory_api_key(self):
        return self._needs_artifactory_api_key

    @property
    def split_by_build_type(self):
        return self._split_by_build_type

    @property
    def default_platform_combinations(self):
        return self._default_platform_combinations

    @property
    def all_package_platform_combinations(self):
        return (
            self._package_platform_combinations
            if self._package_platform_combinations
            else self._default_platform_combinations
        )

    @property
    def package_platform_combinations(self):
        if self._limit_to_platform_combinations:
            return [
                combination
                for combination in self.all_package_platform_combinations
                if combination.name in self._limit_to_platform_combinations
            ]
        else:
            return self.all_package_platform_combinations

    @property
    def conan_config_git_source(self):
        return self._conan_config_git_source

    @property
    def conan_config_git_branch(self):
        return self._conan_config_git_branch

    def recipe_path_for_version(self, v):
        if not self._local_recipe:
            return None
        return self._local_recipe_paths_by_version[v]

    @staticmethod
    def from_yaml(recipe_defaults, recipes_directory, yaml_file):
        import yaml

        name = os.path.splitext(yaml_file)[0]

        with open(os.path.join(recipe_defaults), "r") as f:
            d = yaml.safe_load(f)
        with open(os.path.join(recipes_directory, yaml_file), "r") as f:
            r = yaml.safe_load(f)

        def _read_default_and_override(field, default=None):
            return r.get(field, d.get(field, default))

        versions = [v for v in _read_default_and_override("versions")]
        header_only = _read_default_and_override("header_only")
        source_repository = _read_default_and_override("source_repository")
        build_types = _read_default_and_override("build_types")
        macos_deployment_target = _read_default_and_override("macos_deployment_target")
        centos_yum_preinstall = _listify(
            _read_default_and_override("centos_yum_preinstall")
        )
        macos_brew_preinstall = _listify(
            _read_default_and_override("macos_brew_preinstall")
        )
        require_override = _listify(_read_default_and_override("require_override"))
        force_single_cpu_core_for_debug_builds = _read_default_and_override(
            "force_single_cpu_core_for_debug_builds"
        )
        use_release_zlib_profile = _read_default_and_override(
            "use_release_zlib_profile"
        )
        additional_profiles_for_all_platform_combinations = _listify(
            _read_default_and_override(
                "additional_profiles_for_all_platform_combinations"
            )
        )
        default_platform_combinations = [
            PlatformCombination(c) for c in d.get("platform_combinations", [])
        ]
        package_platform_combinations = [
            PlatformCombination(c)
            for c in _read_default_and_override("platform_combinations")
        ]
        limit_to_platform_combinations = _listify(
            _read_default_and_override("limit_to_platform_combinations")
        )
        needs_artifactory_api_key = _read_default_and_override(
            "needs_artifactory_api_key"
        )
        split_by_build_type = _read_default_and_override("split_by_build_type")
        conan_config_git_source = _read_default_and_override("conan_config_git_source")
        conan_config_git_branch = _read_default_and_override("conan_config_git_branch")


        recipe = PackageBuildDefinitions(
            name=name,
            local_recipe=False,
            source_repository=source_repository,
            versions=versions,
            header_only=header_only,
            build_types=build_types,
            macos_deployment_target=macos_deployment_target,
            centos_yum_preinstall=centos_yum_preinstall,
            macos_brew_preinstall=macos_brew_preinstall,
            require_override=require_override,
            force_single_cpu_core_for_debug_builds=force_single_cpu_core_for_debug_builds,
            use_release_zlib_profile=use_release_zlib_profile,
            additional_profiles_for_all_platform_combinations=additional_profiles_for_all_platform_combinations,
            default_platform_combinations=default_platform_combinations,
            package_platform_combinations=package_platform_combinations,
            limit_to_platform_combinations=limit_to_platform_combinations,
            needs_artifactory_api_key=needs_artifactory_api_key,
            local_recipe_paths_by_version=None,
            split_by_build_type=split_by_build_type,
            conan_config_git_source=conan_config_git_source,
            conan_config_git_branch=conan_config_git_branch,
        )
        return recipe

    @staticmethod
    def from_local_recipe_directory(recipe_defaults, recipe_directory):
        import yaml

        name = os.path.basename(recipe_directory)
        config_yaml_file = os.path.join(recipe_directory, "config.yml")

        with open(os.path.join(recipe_defaults), "r") as f:
            d = yaml.safe_load(f)
        with open(os.path.join(recipe_directory, config_yaml_file), "r") as f:
            r = yaml.safe_load(f)

        def _read_default_and_override(field, default=None):
            return r.get(field, d.get(field, default))

        versions = [v for v in _read_default_and_override("versions")]
        header_only = _read_default_and_override("header_only")
        build_types = _read_default_and_override("build_types")
        macos_deployment_target = _read_default_and_override("macos_deployment_target")
        centos_yum_preinstall = _listify(
            _read_default_and_override("centos_yum_preinstall")
        )
        macos_brew_preinstall = _listify(
            _read_default_and_override("macos_brew_preinstall")
        )
        require_override = _listify(_read_default_and_override("require_override"))
        force_single_cpu_core_for_debug_builds = _read_default_and_override(
            "force_single_cpu_core_for_debug_builds"
        )
        use_release_zlib_profile = _read_default_and_override(
            "use_release_zlib_profile"
        )
        additional_profiles_for_all_platform_combinations = _listify(
            _read_default_and_override(
                "additional_profiles_for_all_platform_combinations"
            )
        )
        default_platform_combinations = [
            PlatformCombination(c) for c in d.get("platform_combinations", [])
        ]
        package_platform_combinations = [
            PlatformCombination(c)
            for c in _read_default_and_override("platform_combinations")
        ]
        limit_to_platform_combinations = _listify(
            _read_default_and_override("limit_to_platform_combinations")
        )
        needs_artifactory_api_key = _read_default_and_override(
            "needs_artifactory_api_key"
        )
        split_by_build_type = _read_default_and_override("split_by_build_type")

        local_recipe_paths_by_version = {
            v: os.path.join(recipe_directory, r["versions"][v]["folder"])
            for v in versions
        }
        conan_config_git_source = _read_default_and_override("conan_config_git_source")
        conan_config_git_branch = _read_default_and_override("conan_config_git_branch")

        recipe = PackageBuildDefinitions(
            name=name,
            local_recipe=True,
            source_repository=None,
            versions=versions,
            header_only=header_only,
            build_types=build_types,
            macos_deployment_target=macos_deployment_target,
            centos_yum_preinstall=centos_yum_preinstall,
            macos_brew_preinstall=macos_brew_preinstall,
            require_override=require_override,
            force_single_cpu_core_for_debug_builds=force_single_cpu_core_for_debug_builds,
            use_release_zlib_profile=use_release_zlib_profile,
            additional_profiles_for_all_platform_combinations=additional_profiles_for_all_platform_combinations,
            default_platform_combinations=default_platform_combinations,
            package_platform_combinations=package_platform_combinations,
            limit_to_platform_combinations=limit_to_platform_combinations,
            needs_artifactory_api_key=needs_artifactory_api_key,
            local_recipe_paths_by_version=local_recipe_paths_by_version,
            split_by_build_type=split_by_build_type,
            conan_config_git_source=conan_config_git_source,
            conan_config_git_branch=conan_config_git_branch,
        )
        return recipe

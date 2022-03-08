# CCDC conan index tools

Python tools and scripts for dealing with conan-ccdc-index

## Usage

Create a venv then, in the venv

`python -m pip install -U pip setuptools`
`python -m pip install -e .`
`python -m pip install -e '.[testing]'`

## Ideas

List all package names
`cit list`

Build a single version of package foo in a single platform configuration and type
`cit pkgbuild --build-type Release --platform-configuration native-centos7-gcc10-x86_64 foo 1.2.3`

Build all versions of package foo in a single platform configuration and type
`cit pkgbuild --build-type Release --platform-configuration native-centos7-gcc10-x86_64 foo`

Build all versions of foo in a single platform configuration in all specified types (Release, Debug etc)
`cit pkgbuild --build-type Release --platform-configuration native-centos7-gcc10-x86_64 foo`

Increase logging level
`cit pkgbuild --build-type Release --platform-configuration native-centos7-gcc10-x86_64 --conan-logging-level foo`

Publish recipes for all versions of foo
`cit publish recipe --destination-repository pr-repo-1234 foo`


    parser.add_argument('--destination-repository',
                        help='where the build goes', default='ccdc-3rdparty-conan')
    parser.add_argument('--macos-brew-preinstall',
                        help='install brew packages', action='append')
    parser.add_argument('--centos-yum-preinstall',
                        help='install yum packages', action='append')
    parser.add_argument('--macos-deployment-target',
                        help='minimum supported macos version', default='10.13')
    parser.add_argument('--macos-xcode-version',
                        help='xcode version')
    parser.add_argument('--windows-bash-path',
                        help='workaround for recipes needing specific path to bash')
    parser.add_argument('--conan-logging-level', help='', default='info')
    parser.add_argument(
        '--workaround-autotools-windows-debug-issue', help='', action='store_true')
    parser.add_argument('--use-release-zlib-profile',
                        help='', action='store_true')
    parser.add_argument('--additional-profiles-for-all-platforms',
                        help='Use additional profiles', action='append')
    parser.add_argument(
        '--local-recipe', help='directory that contains conanfile.py')
    parser.add_argument(
        '--really-upload', help='really upload to artifactory', action='store_true')
    parser.add_argument('--require-override',
                        help='override requirements for specific package', action='append')
    parser.add_argument('--configuration-branch',
                        help='Branch of ccdc-opensource/conan-ccdc-common-configuration to use', default='main')
    parser.add_argument('--configuration-local-directory',
                        help='checkout of ccdc-opensource/conan-ccdc-common-configuration to use')

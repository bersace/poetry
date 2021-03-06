# Change Log

## [Unreleased]

### Added

- Added packaging support (sdist and pure-python wheel).
- Added the `build` command.
- Added support for extras definition.
- Added support for dependencies extras specification.

### Changes

- Dependencies system constraints are now respected when installing packages.


## [0.3.0] - 2018-03-05

### Added

- Added `show` command. 
- Added the `--dry-run` option to the `add` command.

### Changed

- Changed the `poetry.toml` file for the new, standardized `pyproject.toml`.
- Dependencies of each package is now stored in the lock file.
- Improved TOML file management.
- Dependency resolver now respects the root package python version requirements.

### Fixed

- Fixed the `add` command for packages with dots in their names.


## [0.2.0] - 2018-03-01

### Added

- Added `remove` command.
- Added basic support for VCS (git) dependencies.
- Added support for private repositories.

### Changed

- Changed `poetry.lock` format.

### Fixed

- Fixed dependencies solving that would lead to dependencies not being written to lock.


## [0.1.0] - 2018-02-28

Initial release



[Unreleased]: https://github.com/sdispater/poetry/compare/0.3.0...master
[0.3.0]: https://github.com/sdispater/poetry/releases/tag/0.3.0
[0.2.0]: https://github.com/sdispater/poetry/releases/tag/0.2.0
[0.1.0]: https://github.com/sdispater/poetry/releases/tag/0.1.0

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.4] - 2020-06-27
### Changed
- Updated dependencies
- Docker with no-root user
- Docker working directory change from /usr/dev to /tmp


## [0.0.3] - 2020-06-25
### Changed
- Better handling of yaml attribute parsing

## [0.0.2] - 2020-06-25
### Added
- Command to output docker images from Helm Chart files
- Command to output resources used from Helm Chart files

### Changed
- Better abstraction of code to avoid further code duplication

## [0.0.1] - 2020-06-24
### Added
- Command to output kubernetes components used from Helm Chart files


[Unreleased]: https://github.com/nichelia/dok8s/compare/0.0.4...HEAD
[0.0.4]: https://github.com/nichelia/dok8s/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/nichelia/dok8s/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/nichelia/dok8s/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/nichelia/dok8s/releases/tag/0.0.1

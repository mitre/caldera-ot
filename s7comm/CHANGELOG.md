# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-03

### Added

- Initial release of the S7comm plugin.
- Six abilities mapped to MITRE ATT&CK for ICS: read data block, write data block,
  read CPU state, stop CPU, start CPU and read System Status List (SZL).
- Generic `s7comm_cli` payload (python-snap7) with a PyInstaller build, a
  cross-platform build/release workflow, and unit tests driving a local snap7 server.
- "S7comm Sample Facts" fact source and a payload registry for the Linux, Windows and
  macOS binaries.
- A GUI panel (splash service plus Magma Vue view) listing the plugin's abilities.
- An output parser that turns data block reads into `s7comm.db.*` facts.
- Fieldmanual documentation in `docs/s7comm.md`.

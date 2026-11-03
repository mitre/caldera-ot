# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-03

### Added

- Initial release of the M-Bus plugin.
- Five abilities mapped to MITRE ATT&CK for ICS: ping address, scan bus, read meter,
  application reset and broadcast reset (DoS).
- Generic `mbus_cli` payload (hand-built M-Bus framing with pyMeterBus decoding) with
  a PyInstaller build, a cross-platform build/release workflow, and unit tests driving
  a local M-Bus server.
- "M-Bus Sample Facts" fact source and a payload registry for the Linux, Windows and
  macOS binaries.
- A GUI panel (splash service plus Magma Vue view) listing the plugin's abilities.
- An output parser that turns meter reads into `mbus.record.*` facts.
- Fieldmanual documentation in `docs/mbus.md`.

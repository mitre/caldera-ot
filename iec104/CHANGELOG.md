# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-03

### Added

- Initial release of the IEC 104 plugin.
- Six abilities mapped to MITRE ATT&CK for ICS: station interrogation (C_IC_NA_1),
  counter interrogation (C_CI_NA_1), single command (C_SC_NA_1), double command
  (C_DC_NA_1), set-point command (C_SE_NC_1) and clock synchronization (C_CS_NA_1).
- "IEC 104 Sample Facts" fact source, and a payload registry for the `iec104_cli`
  Linux and Windows binaries (`c104` has no maintained macOS build).
- A GUI panel (splash service plus Magma Vue view) listing the plugin's abilities.
- An output parser that turns interrogation results into `iec104.point.*` facts,
  wired into both interrogation abilities.
- Fieldmanual documentation in `docs/iec104.md`.

### Notes

- The `iec104_cli` payload source, build tooling, unit tests and build/release
  workflow live in the separate `iec104-payloads` repository, under GPL-3.0; the
  compiled payloads are distributed from that repository's releases and are installed
  into this plugin's `payloads/` directory.

# NOTICE

mbus, an M-Bus (Meter-Bus) plugin for MITRE Caldera.

Copyright (c) 2026 Asher Davila and Malav Vyas.

Licensed under the Apache License, Version 2.0 (see `LICENSE`).

## Third-party components

The `mbus_cli` payload uses:

- **pyMeterBus**, an M-Bus implementation used to decode read responses, licensed
  under the **BSD-3-Clause** license. https://github.com/ganehag/pyMeterBus

M-Bus framing itself is built by hand in this project (no third-party protocol code).
BSD-3-Clause is permissive, so the plugin and its payload share a single Apache-2.0
repository (as MITRE's `modbus` plugin does with BSD `pymodbus`).

- **PyInstaller** is used only as a build tool; its bootloader exception permits
  distributing the resulting binaries under this project's license.

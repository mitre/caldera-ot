# NOTICE

opcua, an OPC-UA plugin for MITRE Caldera.

Copyright (c) 2026 Asher Davila and Malav Vyas.

Licensed under the Apache License, Version 2.0 (see `LICENSE`).

## Third-party components

The `opcua_cli` payload links against:

- **asyncua** (FreeOpcUa), an OPC-UA implementation, licensed under the **GNU LGPL
  v3.0 or later**. https://github.com/FreeOpcUa/opcua-asyncio

The payload binaries bundle the LGPL `asyncua` package. LGPL permits this so long as
the library remains replaceable; PyInstaller ships it as separate bundled modules,
preserving that. This is why the plugin and its payload share a single Apache-2.0
repository (as MITRE's `modbus` plugin does with BSD `pymodbus`).

- **PyInstaller** is used only as a build tool; its bootloader exception permits
  distributing the resulting binaries under this project's license.

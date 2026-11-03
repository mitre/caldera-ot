# NOTICE

s7comm, an S7comm (Siemens S7) plugin for MITRE Caldera.

Copyright (c) 2026 Asher Davila and Malav Vyas.

Licensed under the Apache License, Version 2.0 (see `LICENSE`).

## Third-party components

The `s7comm_cli` payload links against:

- **python-snap7** and the **snap7** native library, which implement the S7
  protocol. The snap7 library is licensed under the **GNU LGPL v3.0**.
  https://github.com/gijzelaerr/python-snap7 · https://snap7.sourceforge.net/

The payload binaries bundle the LGPL `snap7` shared library. LGPL permits this so
long as the library remains replaceable; PyInstaller ships it as a separate bundled
shared object, preserving that. This is why the plugin and its payload can share a
single Apache-2.0 repository (as the Apache-licensed `modbus` plugin does with the
BSD `pymodbus`), rather than the separate-payloads-repo model used for GPL libraries.

- **PyInstaller** is used only as a build tool; its bootloader exception permits
  distributing the resulting binaries under this project's license.

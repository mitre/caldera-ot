# NOTICE

iec104, an IEC 60870-5-104 plugin for MITRE Caldera.

Copyright (c) 2026 Asher Davila and Malav Vyas.

Licensed under the Apache License, Version 2.0 (see `LICENSE`).

## Payload

The abilities in this plugin invoke the `iec104_cli` payload as a separate process.
The payload's source code, build tooling and compiled binaries are developed and
distributed separately, under **GPL-3.0**, because the payload wraps the GPL-3.0
`c104` library:

- payload repository: https://github.com/AsherDLL/iec104-payloads
- `c104`, a Python IEC 60870-5-104 implementation, GPL-3.0:
  https://github.com/Fraunhofer-FIT-DIEN/iec104-python

No `c104` code is contained in this repository.

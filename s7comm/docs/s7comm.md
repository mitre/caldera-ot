# S7comm Plugin

The S7comm plugin emulates adversary actions over the **Siemens S7 (S7comm)**
protocol (ISO-on-TCP, port 102), used by S7-300/400/1200/1500 PLCs.

All abilities call a single generic payload, `s7comm_cli` (built on python-snap7),
parameterized entirely through facts, so they work against any S7 CPU.

## Command reference

Linux executor shown; Windows uses `s7comm_cli.exe`, macOS `s7comm_cli_darwin`.

| Ability | Command |
|---|---|
| Read Data Block | `s7comm_cli #{s7comm.server.ip} --rack #{s7comm.rack} --slot #{s7comm.slot} --port #{s7comm.server.port} read-db #{s7comm.db.number} #{s7comm.db.start} #{s7comm.db.size} --as real` |
| Write Data Block | `s7comm_cli … write-db #{s7comm.db.number} #{s7comm.db.start} --real #{s7comm.write.value}` |
| Read CPU State | `s7comm_cli … cpu-state` |
| Stop CPU | `s7comm_cli … cpu-stop` |
| Start CPU | `s7comm_cli … cpu-start` |
| Read System Status List | `s7comm_cli … read-szl #{s7comm.szl.id}` |

`write-db` also accepts `--int`, `--dint`, `--byte`, `--hex`; `read-db` accepts
`--as hex|real|int`.

## ATT&CK for ICS coverage

| Technique | Abilities |
|---|---|
| [T0801 Monitor Process State](https://attack.mitre.org/techniques/T0801/) | Read Data Block, Read CPU State |
| [T0836 Modify Parameter](https://attack.mitre.org/techniques/T0836/) | Write Data Block |
| [T0816 Device Restart/Shutdown](https://attack.mitre.org/techniques/T0816/) | Stop CPU, Start CPU |
| [T0846 Remote System Discovery](https://attack.mitre.org/techniques/T0846/) | Read System Status List |

## Facts

| Fact | Description |
|---|---|
| `s7comm.server.ip` | PLC IP address / hostname |
| `s7comm.server.port` | S7 TCP port (102) |
| `s7comm.rack` / `s7comm.slot` | CPU rack / slot (e.g. 0 / 1) |
| `s7comm.db.number` | data block number |
| `s7comm.db.start` / `s7comm.db.size` | DB byte offset / length to read |
| `s7comm.write.value` | value to write (REAL) |
| `s7comm.szl.id` | SZL id, e.g. `0x0011` |

## Payload

`s7comm_cli` wraps python-snap7 (which bundles the LGPL `snap7` library). Exit code
`0` = ok, `1` = request failed/unsupported on target, `2` = connection/argument
error. Built for Linux (glibc >= 2.35), Windows, and macOS by the release CI.

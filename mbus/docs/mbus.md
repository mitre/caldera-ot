# M-Bus Plugin

The M-Bus plugin emulates adversary actions over **Meter-Bus (M-Bus, EN 13757)**,
used to read utility meters (heat, water, gas, electricity), typically reached over a
serial bus or a **TCP/M-Bus gateway** (port 5000).

All abilities call a single generic payload, `mbus_cli`, parameterized through facts,
so they work against any M-Bus meter or gateway.

## Command reference

Linux executor shown; Windows uses `mbus_cli.exe`, macOS `mbus_cli_darwin`.

| Ability | Command |
|---|---|
| Ping Address | `mbus_cli #{mbus.server.ip} --port #{mbus.server.port} ping #{mbus.address}` |
| Scan Bus | `mbus_cli … scan --start #{mbus.scan.start} --end #{mbus.scan.end}` |
| Read Meter | `mbus_cli … read #{mbus.address}` |
| Application Reset | `mbus_cli … app-reset #{mbus.address}` |
| Broadcast Reset (DoS) | `mbus_cli … broadcast-reset` |

## ATT&CK for ICS coverage

| Technique | Abilities |
|---|---|
| [T0846 Remote System Discovery](https://attack.mitre.org/techniques/T0846/) | Ping Address, Scan Bus |
| [T0801 Monitor Process State](https://attack.mitre.org/techniques/T0801/) | Read Meter |
| [T0816 Device Restart/Shutdown](https://attack.mitre.org/techniques/T0816/) | Application Reset |
| [T0814 Denial of Service](https://attack.mitre.org/techniques/T0814/) | Broadcast Reset (DoS) |

## Facts

| Fact | Description |
|---|---|
| `mbus.server.ip` | meter / TCP-gateway IP address |
| `mbus.server.port` | M-Bus/TCP port (5000) |
| `mbus.address` | M-Bus primary address (0-250) |
| `mbus.scan.start` / `mbus.scan.end` | address range for a scan |

## Payload

`mbus_cli` builds M-Bus frames by hand and decodes read responses with pyMeterBus
(BSD-3-Clause). Exit code `0` = ok, `1` = request failed, `2` = connection/argument
error. Built for Linux (glibc >= 2.35), Windows, and macOS by the release CI.

# OPC-UA Plugin

The OPC-UA plugin emulates adversary actions over **OPC Unified Architecture**
(OPC-UA, `opc.tcp`, default port 4840), the vendor-neutral protocol widely used for
IT/OT data exchange and increasingly for control.

All abilities call a single generic payload, `opcua_cli` (built on asyncua),
parameterized through facts, so they work against any OPC-UA server.

## Command reference

Linux executor shown; Windows uses `opcua_cli.exe`, macOS `opcua_cli_darwin`.

| Ability | Command |
|---|---|
| Browse Address Space | `opcua_cli #{opcua.server.endpoint} --port #{opcua.server.port} browse --node #{opcua.browse.node} --depth #{opcua.browse.depth}` |
| Read Node | `opcua_cli … read #{opcua.node.id}` |
| Write Node | `opcua_cli … write #{opcua.node.id} #{opcua.write.value} --type #{opcua.write.type}` |
| Read Endpoints | `opcua_cli … endpoints` |
| Call Method | `opcua_cli … call-method #{opcua.method.object} #{opcua.method.node}` |

`endpoint` may be a bare host/IP (combined with `--port`) or a full
`opc.tcp://host:port` URL. `write --type` is `bool|int|float|string`. Authentication
is anonymous by default; `--user`/`--password` are available on the payload.

## ATT&CK for ICS coverage

| Technique | Abilities |
|---|---|
| [T0846 Remote System Discovery](https://attack.mitre.org/techniques/T0846/) | Browse Address Space, Read Endpoints |
| [T0801 Monitor Process State](https://attack.mitre.org/techniques/T0801/) | Read Node |
| [T0836 Modify Parameter](https://attack.mitre.org/techniques/T0836/) | Write Node |
| [T0871 Execution through API](https://attack.mitre.org/techniques/T0871/) | Call Method |

## Facts

| Fact | Description |
|---|---|
| `opcua.server.endpoint` | server host/IP (or full `opc.tcp://` URL) |
| `opcua.server.port` | OPC-UA port (4840) |
| `opcua.browse.node` | start node id for browse (e.g. `i=85`, the Objects folder) |
| `opcua.browse.depth` | browse recursion depth |
| `opcua.node.id` | node id to read/write (e.g. `ns=2;i=9`) |
| `opcua.write.value` / `opcua.write.type` | value and type (`bool\|int\|float\|string`) |
| `opcua.method.object` / `opcua.method.node` | object and method node ids for a call |

## Payload

`opcua_cli` wraps asyncua (LGPL-3.0). Exit code `0` = ok, `1` = request failed,
`2` = connection/argument error. Built for Linux (glibc >= 2.35), Windows, macOS by
the release CI.

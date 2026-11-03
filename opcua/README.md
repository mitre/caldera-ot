# Caldera for OT plugin: OPC-UA

A [Caldera for OT](https://github.com/mitre/caldera-ot) plugin supplying
[Caldera](https://github.com/mitre/caldera) with **OPC Unified Architecture**
(OPC-UA) protocol TTPs mapped to MITRE ATT&CK® for ICS. This is part of a series of
plugins that provide added threat emulation capability for Operational Technology
(OT) environments.

OPC-UA is the vendor-neutral, service-oriented protocol used across modern IT/OT
environments, carried over `opc.tcp` (TCP/4840). Abilities are driven by a generic
command-line client (`opcua_cli`), so they work against any OPC-UA server: the
endpoint and node ids are supplied as facts.

Full OPC-UA plugin [documentation](docs/opcua.md) can be viewed as part of
fieldmanual, once the Caldera server is running.

## Abilities

| Ability | Tactic | Technique |
|---|---|---|
| OPC-UA - Read Endpoints | Discovery | T0846 Remote System Discovery |
| OPC-UA - Browse Address Space | Discovery | T0846 Remote System Discovery |
| OPC-UA - Read Node | Collection | T0801 Monitor Process State |
| OPC-UA - Write Node | Impair Process Control | T0836 Modify Parameter |
| OPC-UA - Call Method | Execution | T0871 Execution through API |

## Installation

To run Caldera along with the OPC-UA plugin:
1. Download Caldera as detailed in the [Installation Guide](https://github.com/mitre/caldera)
2. Install this plugin into Caldera's plugin directory as `caldera/plugins/opcua`.
   Clone the [Caldera for OT](https://github.com/mitre/caldera-ot) collection and
   move the `opcua` directory into place:
```
git clone https://github.com/mitre/caldera-ot.git --recursive
mv caldera-ot/opcua <caldera>/plugins/opcua
```
3. Enable the opcua plugin. To do this, add `- opcua` to the list of enabled plugins
   in either `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure
   mode)

### Version

This plugin has been tested with Caldera v5.0.0.

### Payload Compatibility

This plugin uses pre-compiled binaries (payloads) that are delivered and executed on
the target device by the Caldera agent. To execute, the payloads must be compatible
with the target device operating system. The Linux payload (`opcua_cli`) ships in
[`payloads/`](payloads/); the Windows (`opcua_cli.exe`) and macOS
(`opcua_cli_darwin`) payloads are produced by the build workflow in
[`.github/workflows/ci.yaml`](.github/workflows/ci.yaml) and published as release
assets. The Linux payload is built on Ubuntu 22.04 (`glibc` 2.35), so it requires
`glibc` 2.35 or greater; rebuilding it on an older distribution lowers that floor.
For more information on compatibility, see the
[fieldmanual documentation](docs/opcua.md#payload) and the
[source README](src/README.md).

### Payload Source Code

For additional information on the OPC-UA plugin payload source code, please see the
[source directory](src/), which contains additional licensing and build guidance.

## Usage

1. Install and enable the plugin as described [above](#installation).
2. Optionally, create a fact source to store attributes of the target system. An
   example is provided [here](./data/sources/0d1360b8-4b30-438f-a67b-e20c6b5b5787.yml).
3. Start the Caldera server.
4. Create a new Operation, optionally using the fact source from step 2.
5. Use "Add Potential Link" to run a specific ability from this plugin. Fact values
   can be entered manually, or selected from a fact source.

The abilities read the following facts:

| Fact | Example | Description |
|---|---|---|
| `opcua.server.endpoint` | `10.0.0.5` | server host/IP, or a full `opc.tcp://` URL |
| `opcua.server.port` | `4840` | OPC-UA port |
| `opcua.browse.node` | `"i=85"` | start node id for a browse (`i=85` is Objects) |
| `opcua.browse.depth` | `1` | browse recursion depth |
| `opcua.node.id` | `"ns=2;i=9"` | node id to read or write |
| `opcua.write.value` / `opcua.write.type` | `0` / `float` | value and type (`bool`, `int`, `float`, `string`) |
| `opcua.method.object` / `opcua.method.node` | `"i=85"` / `"i=85"` | object and method node ids for a call |

The browse ability parses the payload's output into `opcua.node.*` facts, so
discovered nodes can seed later abilities.

## Authors

This plugin was contributed by **Asher Davila** and **Malav Vyas**.

## License

Apache-2.0. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).

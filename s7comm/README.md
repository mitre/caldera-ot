# Caldera for OT plugin: S7comm

A [Caldera for OT](https://github.com/mitre/caldera-ot) plugin supplying
[Caldera](https://github.com/mitre/caldera) with **Siemens S7 (S7comm)** protocol
TTPs mapped to MITRE ATT&CK® for ICS. This is part of a series of plugins that
provide added threat emulation capability for Operational Technology (OT)
environments.

S7comm is the protocol used to program and control Siemens SIMATIC S7-300/400/1200/1500
PLCs, carried over ISO-on-TCP (TCP/102). Abilities are driven by a generic
command-line client (`s7comm_cli`), so they work against any S7 CPU: the target
address, rack/slot and data block numbers are supplied as facts.

Full S7comm plugin [documentation](docs/s7comm.md) can be viewed as part of
fieldmanual, once the Caldera server is running.

## Abilities

| Ability | Tactic | Technique |
|---|---|---|
| S7comm - Read Data Block | Collection | T0801 Monitor Process State |
| S7comm - Read CPU State | Collection | T0801 Monitor Process State |
| S7comm - Read System Status List | Discovery | T0846 Remote System Discovery |
| S7comm - Write Data Block | Impair Process Control | T0836 Modify Parameter |
| S7comm - Stop CPU | Inhibit Response Function | T0816 Device Restart/Shutdown |
| S7comm - Start CPU | Execution | T0816 Device Restart/Shutdown |

## Installation

To run Caldera along with the S7comm plugin:
1. Download Caldera as detailed in the [Installation Guide](https://github.com/mitre/caldera)
2. Install this plugin into Caldera's plugin directory as `caldera/plugins/s7comm`.
   Clone the [Caldera for OT](https://github.com/mitre/caldera-ot) collection and
   move the `s7comm` directory into place:
```
git clone https://github.com/mitre/caldera-ot.git --recursive
mv caldera-ot/s7comm <caldera>/plugins/s7comm
```
3. Enable the s7comm plugin. To do this, add `- s7comm` to the list of enabled plugins
   in either `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure
   mode)

### Version

This plugin has been tested with Caldera v5.0.0.

### Payload Compatibility

This plugin uses pre-compiled binaries (payloads) that are delivered and executed on
the target device by the Caldera agent. To execute, the payloads must be compatible
with the target device operating system. The Linux payload (`s7comm_cli`) ships in
[`payloads/`](payloads/); the Windows (`s7comm_cli.exe`) and macOS
(`s7comm_cli_darwin`) payloads are produced by the build workflow in
[`.github/workflows/ci.yaml`](.github/workflows/ci.yaml) and published as release
assets. The Linux payload is built on Ubuntu 22.04 (`glibc` 2.35), so it requires
`glibc` 2.35 or greater; rebuilding it on an older distribution lowers that floor.
For more information on compatibility, see the
[fieldmanual documentation](docs/s7comm.md#payload) and the
[source README](src/README.md).

### Payload Source Code

For additional information on the S7comm plugin payload source code, please see the
[source directory](src/), which contains additional licensing and build guidance.

## Usage

1. Install and enable the plugin as described [above](#installation).
2. Optionally, create a fact source to store attributes of the target system. An
   example is provided [here](./data/sources/d3815829-4a3c-4c47-be8d-409f79cc09ea.yml).
3. Start the Caldera server.
4. Create a new Operation, optionally using the fact source from step 2.
5. Use "Add Potential Link" to run a specific ability from this plugin. Fact values
   can be entered manually, or selected from a fact source.

The abilities read the following facts:

| Fact | Example | Description |
|---|---|---|
| `s7comm.server.ip` | `10.0.0.5` | PLC IP address or hostname |
| `s7comm.server.port` | `102` | S7 (ISO-on-TCP) port |
| `s7comm.rack` / `s7comm.slot` | `0` / `1` | CPU rack / slot |
| `s7comm.db.number` | `1` | data block number |
| `s7comm.db.start` / `s7comm.db.size` | `0` / `4` | DB byte offset / length to read |
| `s7comm.write.value` | `0.0` | value to write (REAL) |
| `s7comm.szl.id` | `"0x0011"` | System Status List id |

The read-data-block ability parses the payload's output into `s7comm.db.*` facts, so
collected values can seed later abilities.

## Authors

This plugin was contributed by **Asher Davila** and **Malav Vyas**.

## License

Apache-2.0. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).

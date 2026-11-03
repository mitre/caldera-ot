# Caldera for OT plugin: M-Bus

A [Caldera for OT](https://github.com/mitre/caldera-ot) plugin supplying
[Caldera](https://github.com/mitre/caldera) with **Meter-Bus (M-Bus, EN 13757)**
protocol TTPs mapped to MITRE ATT&CK® for ICS. This is part of a series of plugins
that provide added threat emulation capability for Operational Technology (OT)
environments.

M-Bus is the European standard for reading utility meters (heat, gas, water,
electricity). This plugin reaches the bus over an M-Bus/TCP gateway (TCP/5000).
Abilities are driven by a generic command-line client (`mbus_cli`), so they work
against any M-Bus meter or gateway: the primary address and port are supplied as
facts.

Full M-Bus plugin [documentation](docs/mbus.md) can be viewed as part of fieldmanual,
once the Caldera server is running.

## Abilities

| Ability | Tactic | Technique |
|---|---|---|
| M-Bus - Ping Address | Discovery | T0846 Remote System Discovery |
| M-Bus - Scan Bus | Discovery | T0846 Remote System Discovery |
| M-Bus - Read Meter | Collection | T0801 Monitor Process State |
| M-Bus - Application Reset | Inhibit Response Function | T0816 Device Restart/Shutdown |
| M-Bus - Broadcast Reset (DoS) | Inhibit Response Function | T0814 Denial of Service |

## Installation

To run Caldera along with the M-Bus plugin:
1. Download Caldera as detailed in the [Installation Guide](https://github.com/mitre/caldera)
2. Install this plugin into Caldera's plugin directory as `caldera/plugins/mbus`.
   Clone the [Caldera for OT](https://github.com/mitre/caldera-ot) collection and
   move the `mbus` directory into place:
```
git clone https://github.com/mitre/caldera-ot.git --recursive
mv caldera-ot/mbus <caldera>/plugins/mbus
```
3. Enable the mbus plugin. To do this, add `- mbus` to the list of enabled plugins
   in either `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure
   mode)

### Version

This plugin has been tested with Caldera v5.0.0.

### Payload Compatibility

This plugin uses pre-compiled binaries (payloads) that are delivered and executed on
the target device by the Caldera agent. To execute, the payloads must be compatible
with the target device operating system. The Linux payload (`mbus_cli`) ships in
[`payloads/`](payloads/); the Windows (`mbus_cli.exe`) and macOS (`mbus_cli_darwin`)
payloads are produced by the build workflow in
[`.github/workflows/ci.yaml`](.github/workflows/ci.yaml) and published as release
assets. The Linux payload is built on Ubuntu 22.04 (`glibc` 2.35), so it requires
`glibc` 2.35 or greater; rebuilding it on an older distribution lowers that floor.
For more information on compatibility, see the
[fieldmanual documentation](docs/mbus.md#payload) and the
[source README](src/README.md).

### Payload Source Code

For additional information on the M-Bus plugin payload source code, please see the
[source directory](src/), which contains additional licensing and build guidance.

## Usage

1. Install and enable the plugin as described [above](#installation).
2. Optionally, create a fact source to store attributes of the target system. An
   example is provided [here](./data/sources/838e222e-cab6-407f-a277-5755f0f7caf1.yml).
3. Start the Caldera server.
4. Create a new Operation, optionally using the fact source from step 2.
5. Use "Add Potential Link" to run a specific ability from this plugin. Fact values
   can be entered manually, or selected from a fact source.

The abilities read the following facts:

| Fact | Example | Description |
|---|---|---|
| `mbus.server.ip` | `10.0.0.5` | meter or M-Bus/TCP gateway IP address |
| `mbus.server.port` | `5000` | M-Bus/TCP port |
| `mbus.address` | `1` | M-Bus primary address (0-250) |
| `mbus.scan.start` / `mbus.scan.end` | `1` / `5` | address range for a bus scan |

The read-meter ability parses the payload's output into `mbus.record.*` facts, so
collected meter records can seed later abilities.

### A note on "M-Bus - Broadcast Reset"

The broadcast reset ability sends an application reset to the M-Bus broadcast address,
which resets every device on the bus at once. It is mapped to T0814 Denial of Service
and is disruptive by design; use it only against targets you are authorized to test.

## Authors

This plugin was contributed by **Asher Davila** and **Malav Vyas**.

## License

Apache-2.0. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).

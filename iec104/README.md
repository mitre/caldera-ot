# Caldera for OT plugin: IEC 104

A [Caldera for OT](https://github.com/mitre/caldera-ot) plugin supplying
[Caldera](https://github.com/mitre/caldera) with **IEC 60870-5-104** (IEC 104)
telecontrol protocol TTPs mapped to MITRE ATT&CK® for ICS. This is part of a series
of plugins that provide added threat emulation capability for Operational Technology
(OT) environments.

IEC 104 carries telecontrol traffic over TCP/2404 between control centers and
outstations (RTUs/PLCs), and is widely deployed in electric power and other utility
SCADA systems. Abilities are driven by a generic command-line master (`iec104_cli`),
so they work against any conforming outstation: the common address and information
object addresses are supplied as facts.

Full IEC 104 plugin [documentation](docs/iec104.md) can be viewed as part of
fieldmanual, once the Caldera server is running.

## Abilities

| Ability | IEC 104 ASDU | Tactic | Technique |
|---|---|---|---|
| IEC 104 - Station Interrogation | C_IC_NA_1 | Collection | T0861 Point & Tag Identification |
| IEC 104 - Counter Interrogation | C_CI_NA_1 | Collection | T0861 Point & Tag Identification |
| IEC 104 - Single Command | C_SC_NA_1 | Impair Process Control | T0855 Unauthorized Command Message |
| IEC 104 - Double Command | C_DC_NA_1 | Impair Process Control | T0855 Unauthorized Command Message |
| IEC 104 - Set Point Command | C_SE_NC_1 | Impair Process Control | T0836 Modify Parameter |
| IEC 104 - Clock Synchronization | C_CS_NA_1 | Impair Process Control | T0855 Unauthorized Command Message |

## Installation

To run Caldera along with the IEC 104 plugin:
1. Download Caldera as detailed in the [Installation Guide](https://github.com/mitre/caldera)
2. Install this plugin into Caldera's plugin directory as `caldera/plugins/iec104`.
   Clone the [Caldera for OT](https://github.com/mitre/caldera-ot) collection and
   move the `iec104` directory into place:
```
git clone https://github.com/mitre/caldera-ot.git --recursive
mv caldera-ot/iec104 <caldera>/plugins/iec104
```
3. Download the required compiled payload(s) from the [__Releases__](https://github.com/AsherDLL/iec104-payloads/releases)
   section of the `iec104-payloads` repository. The downloadable payloads are
   available under the __Assets__ header of the latest release.
4. Save the downloaded payload file(s) in the `caldera/plugins/iec104/payloads`
   directory of your Caldera installation.
5. Enable the iec104 plugin. To do this, add `- iec104` to the list of enabled plugins
   in either `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure
   mode)

### Version

This plugin has been tested with Caldera v5.0.0.

### Payload Compatibility

This plugin uses pre-compiled binaries (payloads) that are delivered and executed on
the target device by the Caldera agent. To execute, the payloads must be compatible
with the target device operating system. Linux and Windows payloads are published;
macOS is not, because the `c104` library has no maintained macOS build. The
published Linux payload is built on the `ubuntu-22.04` runner (`glibc` 2.35), so it
requires `glibc` 2.35 or greater; rebuilding the payload on an older distribution
lowers that floor. For more information on compatibility, see the
[fieldmanual documentation](docs/iec104.md#payloads).

### Plugin Payload Source Code

For additional information on the IEC 104 plugin payload source code, please see the
[`iec104-payloads`](https://github.com/AsherDLL/iec104-payloads) repository. That
repository also carries the payload's build tooling, unit tests and build/release
workflow.

## Usage

1. Install and enable the plugin as described [above](#installation).
2. Optionally, create a fact source to store attributes of the target system. An
   example is provided [here](./data/sources/9b542028-e4cc-49bf-b590-b423a88e9239.yml).
3. Start the Caldera server.
4. Create a new Operation, optionally using the fact source from step 2.
5. Use "Add Potential Link" to run a specific ability from this plugin. Fact values
   can be entered manually, or selected from a fact source.

The abilities read the following facts:

| Fact | Example | Description |
|---|---|---|
| `iec104.server.ip` | `10.0.0.5` | outstation IP address or hostname |
| `iec104.server.port` | `2404` | IEC 104 TCP port |
| `iec104.common_address` | `1` | ASDU common address of the target station |
| `iec104.command.ioa` | `100` | information object address for single/double commands |
| `iec104.command.value` | `"ON"` | `ON` or `OFF` (quote the value in YAML) |
| `iec104.setpoint.ioa` | `100` | information object address for set-point commands |
| `iec104.setpoint.value` | `12.5` | set-point value |

The interrogation abilities parse the payload's output into `iec104.point.ioa` /
`iec104.point.value` facts, so discovered points can seed later abilities.

## Authors

This plugin was contributed by **Asher Davila** and **Malav Vyas**.

## License

Apache-2.0. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md). The `iec104_cli`
payload is distributed separately under GPL-3.0, because it wraps the GPL-3.0 `c104`
library; see the [`iec104-payloads`](https://github.com/AsherDLL/iec104-payloads)
repository.

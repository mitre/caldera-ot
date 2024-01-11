# MITRE Caldera™ for OT Plugins

A collection of plugins that extend [MITRE Caldera™](https://github.com/mitre/caldera) to the Operational Technology (OT) environment.

It is built on the [MITRE ATT&CK® for ICS framework](https://attack.mitre.org/matrices/ics/).

This repository contains all the Caldera for OT plugins as git submodules. As described in each individual plugin README, it is also possible to `git clone` a specific protocol plugin directly into the Caldera `plugins` directory, following the "Installation" guidance.

## Install Caldera for OT Plugins

To install all the Caldera for OT plugins, use the recursive flag while cloning this repository:

`git clone https://github.com/mitre/caldera-ot.git --recursive`

Note, that after performing the `git clone`, you will still need to:

1. Ensure the plugin(s) of interest are moved into the `caldera/plugins` directory of your caldera instance
2. Enable the plugin(s) by adding their names to the `conf/local.yml` or `conf/default.yml` (if running Caldera in insecure mode)

For example, 
```
- bacnet
- dnp3
- modbus
- profinet
- iec61850
```

The OT plugins can also be setup individually:
* [bacnet](https://github.com/mitre/bacnet#readme)
* [dnp3](https://github.com/mitre/dnp3#readme)
* [modbus](https://github.com/mitre/modbus#readme)
* [profinet](https://github.com/mitre/profinet#readme)
* [iec61850](https://github.com/mitre/iec61850#readme)


## What are the Caldera for OT plugins?

The Caldera for OT plugins unify and expose open-source OT protocol libraries in the form of protocol specific plugins:
* `bacnet` - for the Building Automation and Control Networks (BACnet) protocol
* `dnp3` - for the Distributed Network Protocol 3 (DNP3)
* `modbus` - for the Modbus protocol
* `profinet` - for the Profinet protocol - *Basic Discovery and Configuration Protocol (DCP) only*
* `iec61850` - for the IEC 61850 series of communication protocols - *Manufacturing Message Specification (MMS) only*

Each plugin contains the following documentation:
* High-level README.md
* Source code specific README.md (located under `/src`)
* Caldera Field Manual documentation (located under `/docs`)

### What is the motivation for the plugins?

The Caldera for OT plugins enable adversary emulation in the OT environment, which supports traditional Caldera [use cases](https://caldera.mitre.org/). For example, training and testing of operators and defenses.

Also see our presentation on [Emulating Adversary Actions in the Operational Environment with Caldera (TM) for OT](https://speakerdeck.com/bjeffries/emulating-adversary-actions-in-the-operational-environment-with-caldera-for-ot).

## Contact

Please reach out to OT@mitre.org with comments, questions, and to discuss collaboration opportunities.

The Caldera for OT team can also be reached on the official [Caldera slack](https://join.slack.com/t/mitre-caldera/shared_invite/zt-rvngjjpw-OQHAqpUT87DcyClTosF8dQ).
# Caldera for OT Plugins

A collection of plugins that extend [Caldera](https://github.com/mitre/caldera) to the Operational Technology (OT) environment.

This repository contains all the Caldera for OT plugins as git submodules. As described in each individual plugin README, it is also possible to `git clone` a specific protocol plugin directly into the Caldera `plugins` directory, following the "Installation" guidance.

## Install Caldera for OT Plugins

To install all the Caldera for OT plugins, use the recursive flag while cloning this repo:

`git clone https://github.com/mitre/caldera-ot.git --recursive`

Or, setup a specific plugin individually: 
* [bacnet](https://github.com/mitre/bacnet)
* [dnp3](https://github.com/mitre/dnp3)
* [modbus](https://github.com/mitre/modbus)


## What are the Caldera for OT plugins?

The Caldera for OT plugins unify and expose open-source OT protocol libraries in the form of protocol specific plugins:
* `bacnet` - for the Building Automation and Control Networks (BACnet) protocol
* `dnp3` - for the Distributed Network Protocol 3 (DNP3)
* `modbus` - for the Modbus protocol

Each plugin contains the following documentation:
* High-level README.md
* Source code specific README.md (located under `/src`)
* Caldera Field Manual documentation (located under `/docs`)

### What is the motivation for the plugins?

The Caldera for OT plugins enable adversary emulation in the OT environment, which supports traditional Caldera [use cases](https://caldera.mitre.org/). For example, training and testing of operators and defenses.

Also see our presentation on [Emulating Adversary Actions in the Operational Environment with Caldera (TM) for OT](https://speakerdeck.com/bjeffries/emulating-adversary-actions-in-the-operational-environment-with-caldera-for-ot).

## Contact

Please reach out to OT@mitre.org with comments, questions, and to discuss collaboration opportunities.

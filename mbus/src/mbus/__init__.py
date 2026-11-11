# SPDX-License-Identifier: Apache-2.0
"""A small M-Bus (Meter-Bus) client action library.

Speaks M-Bus over TCP with hand-built frames (the protocol's frames are simple) and
uses pyMeterBus to decode read responses. Exposes MBusClient with the discrete
master actions: ping, scan, read, application reset, and broadcast reset.
"""
from .client import MBusClient, MBusError
from .version import __version__

__all__ = ["MBusClient", "MBusError", "__version__"]

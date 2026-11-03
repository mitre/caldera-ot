# SPDX-License-Identifier: Apache-2.0
"""A small S7comm (Siemens S7) client action library built on python-snap7.

Exposes S7Client, a thin wrapper turning the snap7 client API into the discrete
actions an operator drives from the command line: read/write data blocks, read CPU
state, stop/start the CPU, and read system status lists (SZL).
"""
from .client import S7Client, S7Error
from .version import __version__

__all__ = ["S7Client", "S7Error", "__version__"]

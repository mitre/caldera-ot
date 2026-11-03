# SPDX-License-Identifier: Apache-2.0
"""A small OPC-UA client action library built on asyncua.

Exposes OPCUAClient, a thin wrapper that turns the asyncua client API into the
discrete actions an operator drives from the command line: browse the address
space, read/write a node value, list endpoints, and call a method.
"""
from .client import OPCUAClient, OPCUAError, parse_bool
from .version import __version__

__all__ = ["OPCUAClient", "OPCUAError", "parse_bool", "__version__"]

# SPDX-License-Identifier: Apache-2.0
"""Unit tests for the opcua_cli action library.

Stands up a local asyncua server with a writable variable and drives it with
OPCUAClient, asserting browse/read/write reach it. Tests fail without the client
logic.
"""
import asyncio

import pytest
from asyncua import Server

from uaclient import OPCUAClient, OPCUAError, parse_bool

URL = "opc.tcp://127.0.0.1:14840"


async def _scenario():
    server = Server()
    await server.init()
    server.set_endpoint(URL)
    idx = await server.register_namespace("test")
    obj = await server.nodes.objects.add_object(idx, "Thing")
    var = await obj.add_variable(idx, "Speed", 1007.0)
    await var.set_writable()
    node = var.nodeid.to_string()

    async with server:
        async with OPCUAClient(URL) as c:
            assert await c.read(node) == pytest.approx(1007.0)
            await c.write(node, "1410", "float")  # Stuxnet-style over-speed
            assert await c.read(node) == pytest.approx(1410.0)
            names = [n for _, n in await c.browse(obj.nodeid.to_string(), 1)]
            assert "Speed" in names
            eps = await c.endpoints()
            assert eps and eps[0][0].startswith("opc.tcp://")
    return True


def test_browse_read_write_endpoints():
    assert asyncio.run(_scenario())


def test_parse_bool():
    assert parse_bool("true") is True and parse_bool("OFF") is False
    with pytest.raises(ValueError):
        parse_bool("maybe")


def test_bad_endpoint_raises():
    async def _bad():
        async with OPCUAClient("opc.tcp://no.such.host.invalid.:4840", timeout=2.0):
            pass
    with pytest.raises(OPCUAError):
        asyncio.run(_bad())

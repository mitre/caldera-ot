# SPDX-License-Identifier: Apache-2.0
"""OPC-UA client actions, backed by asyncua.

Transport-only: it takes node ids / values and has no knowledge of any particular
device, so it works against any OPC-UA server. All methods are async; the CLI wraps
them in asyncio.run().
"""
from asyncua import Client, ua

VARIANT_TYPES = {
    "bool": ua.VariantType.Boolean,
    "int": ua.VariantType.Int64,
    "float": ua.VariantType.Double,
    "string": ua.VariantType.String,
}


class OPCUAError(Exception):
    """Raised on connection failure or a rejected request."""


def parse_bool(value):
    s = str(value).strip().lower()
    if s in ("true", "on", "1"):
        return True
    if s in ("false", "off", "0"):
        return False
    raise ValueError(f"expected true/false (got {value!r})")


def _coerce(value, kind):
    if kind == "bool":
        return parse_bool(value)
    if kind == "int":
        return int(value)
    if kind == "float":
        return float(value)
    return str(value)


class OPCUAClient:
    def __init__(self, url, username=None, password=None, timeout=10.0):
        self.url = url
        self._client = Client(url, timeout=float(timeout))
        if username:
            self._client.set_user(username)
        if password:
            self._client.set_password(password)

    async def __aenter__(self):
        try:
            await self._client.connect()
        except Exception as exc:
            raise OPCUAError(f"could not connect to {self.url}: {exc}") from exc
        return self

    async def __aexit__(self, *_exc):
        try:
            await self._client.disconnect()
        except Exception:
            pass

    async def browse(self, nodeid=None, depth=1):
        root = self._client.get_node(nodeid) if nodeid else self._client.nodes.objects
        found = []
        await self._walk(root, int(depth), found)
        return found

    async def _walk(self, node, depth, found):
        for child in await node.get_children():
            try:
                name = (await child.read_browse_name()).Name
            except Exception:
                name = "?"
            found.append((child.nodeid.to_string(), name))
            if depth > 1:
                await self._walk(child, depth - 1, found)

    async def read(self, nodeid):
        return await self._client.get_node(nodeid).read_value()

    async def write(self, nodeid, value, kind):
        variant = ua.Variant(_coerce(value, kind), VARIANT_TYPES[kind])
        await self._client.get_node(nodeid).write_value(ua.DataValue(variant))
        return True

    async def endpoints(self):
        eps = await self._client.get_endpoints()
        out = []
        for e in eps:
            out.append((e.EndpointUrl,
                        e.SecurityPolicyUri.split("#")[-1],
                        e.SecurityMode.name if hasattr(e.SecurityMode, "name")
                        else str(e.SecurityMode)))
        return out

    async def call_method(self, parent_nodeid, method_nodeid, args):
        parent = self._client.get_node(parent_nodeid)
        cast = []
        for a in args:
            for conv in (int, float):
                try:
                    cast.append(conv(a))
                    break
                except ValueError:
                    continue
            else:
                cast.append(a)
        return await parent.call_method(self._client.get_node(method_nodeid), *cast)

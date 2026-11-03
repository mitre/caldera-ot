# SPDX-License-Identifier: Apache-2.0
"""opcua_cli - a command-line OPC-UA client for adversary emulation.

A generic client that speaks OPC-UA to any server. Transport-only (node ids /
values); the meaning of each node belongs to the target. Driven from Caldera
abilities, one subcommand per action.

    opcua_cli <endpoint> <action> [args]
    endpoint = opc.tcp://host:port  (or just host, with --port)
"""
import argparse
import asyncio
import logging
import sys

from uaclient import OPCUAClient, OPCUAError, __version__

# Keep stdout clean for parsers: silence asyncua's informational logging.
logging.getLogger("asyncua").setLevel(logging.CRITICAL)


def _build_parser():
    p = argparse.ArgumentParser(
        prog="opcua_cli",
        description="OPC-UA action library v%s" % __version__)
    p.add_argument("endpoint", help="opc.tcp://host:port, or a bare host/IP")
    p.add_argument("-p", "--port", type=int, default=4840,
                   help="port when endpoint is a bare host (default 4840)")
    p.add_argument("--user", help="username (default anonymous)")
    p.add_argument("--password", help="password")
    p.add_argument("--timeout", type=float, default=10.0)
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="action", required=True, metavar="action")

    s = sub.add_parser("browse", help="browse the address space")
    s.add_argument("--node", help="start node id (default the Objects folder)")
    s.add_argument("--depth", type=int, default=1, help="recursion depth (default 1)")

    s = sub.add_parser("read", help="read a node value")
    s.add_argument("node")

    s = sub.add_parser("write", help="write a node value")
    s.add_argument("node")
    s.add_argument("value")
    s.add_argument("--type", dest="kind", choices=("bool", "int", "float", "string"),
                   default="float", help="value type (default float)")

    sub.add_parser("endpoints", help="list the server's endpoints")

    s = sub.add_parser("call-method", help="call a method on an object node")
    s.add_argument("object")
    s.add_argument("method")
    s.add_argument("args", nargs="*")
    return p


async def _run(args):
    if args.endpoint.startswith("opc.tcp://"):
        url = args.endpoint
    else:
        url = "opc.tcp://%s:%d" % (args.endpoint, args.port)
    async with OPCUAClient(url, args.user, args.password, args.timeout) as c:
        if args.action == "browse":
            print("[*] Browse %s" % (args.node or "Objects"))
            nodes = await c.browse(args.node, args.depth)
            for nid, name in nodes:
                print("node %s = %s" % (nid, name))
            return True
        if args.action == "read":
            print("[*] Read %s" % args.node)
            print("value %s = %s" % (args.node, await c.read(args.node)))
            return True
        if args.action == "write":
            print("[*] Write %s = %s (%s)" % (args.node, args.value, args.kind))
            return await c.write(args.node, args.value, args.kind)
        if args.action == "endpoints":
            print("[*] Endpoints")
            for url_, policy, mode in await c.endpoints():
                print("endpoint %s | %s | %s" % (url_, policy, mode))
            return True
        if args.action == "call-method":
            print("[*] Call method %s on %s" % (args.method, args.object))
            result = await c.call_method(args.object, args.method, args.args)
            print("result = %s" % (result,))
            return True
        return False


def main(argv=None):
    args = _build_parser().parse_args(argv)
    try:
        ok = asyncio.run(_run(args))
    except OPCUAError as exc:
        print("[!] %s" % exc, file=sys.stderr)
        return 2
    except (ValueError, KeyError) as exc:
        print("[!] %s" % exc, file=sys.stderr)
        return 2
    except Exception as exc:
        print("[!] %s" % exc, file=sys.stderr)
        return 1
    if ok:
        print("[+] %s: ok" % args.action)
        return 0
    print("[!] %s: failed" % args.action, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

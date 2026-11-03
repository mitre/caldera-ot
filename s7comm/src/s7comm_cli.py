# SPDX-License-Identifier: Apache-2.0
"""s7comm_cli - a command-line S7comm (Siemens S7) client for adversary emulation.

A generic client that speaks S7comm to any S7 PLC or snap7 outstation. Transport-only
(numeric DB numbers / offsets / values); the meaning of each block belongs to the
target device. Driven from Caldera abilities, one subcommand per action.

    s7comm_cli <host> [--rack 0] [--slot 1] [--port 102] <action> [args]
"""
import argparse
import sys

from s7comm import S7Client, S7Error, __version__
from s7comm.client import decode_values, encode_value


def _build_parser():
    p = argparse.ArgumentParser(
        prog="s7comm_cli",
        description="S7comm (Siemens S7) action library v%s" % __version__)
    p.add_argument("host", help="target PLC IP address or hostname")
    p.add_argument("--rack", type=int, default=0, help="CPU rack (default 0)")
    p.add_argument("--slot", type=int, default=1, help="CPU slot (default 1)")
    p.add_argument("-p", "--port", type=int, default=102, help="S7 TCP port (default 102)")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="action", required=True, metavar="action")

    s = sub.add_parser("read-db", help="read a data block (S7 Read Var)")
    s.add_argument("db", type=int)
    s.add_argument("start", type=int)
    s.add_argument("size", type=int)
    s.add_argument("--as", dest="kind", choices=("hex", "real", "int"), default="hex",
                   help="interpret the bytes (default hex)")

    s = sub.add_parser("write-db", help="write a data block (S7 Write Var)")
    s.add_argument("db", type=int)
    s.add_argument("start", type=int)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--real", type=float, help="write a 4-byte REAL")
    g.add_argument("--int", type=int, dest="intval", help="write a 2-byte INT")
    g.add_argument("--dint", type=int, help="write a 4-byte DINT")
    g.add_argument("--byte", type=int, help="write a single byte")
    g.add_argument("--hex", dest="hexval", help="write raw hex bytes")

    sub.add_parser("cpu-state", help="read the CPU run/stop state")
    sub.add_parser("cpu-stop", help="stop the CPU (S7 PLC Stop)")
    s = sub.add_parser("cpu-start", help="start the CPU (S7 PLC Start)")
    s.add_argument("--hot", action="store_true", help="hot start instead of cold")

    s = sub.add_parser("read-szl", help="read a System Status List (SZL)")
    s.add_argument("szl_id", help="SZL id, e.g. 0x0011 (module id) or 0x001c")
    s.add_argument("--index", default=0)
    return p


def _run(args):
    client = S7Client(host=args.host, rack=args.rack, slot=args.slot, port=args.port)
    client.connect()
    try:
        if args.action == "read-db":
            print("[*] Read DB%d offset %d (%d bytes)" % (args.db, args.start, args.size))
            blob = client.read_db(args.db, args.start, args.size)
            for off, val in decode_values(blob, args.kind):
                print("db%d.%d = %s" % (args.db, args.start + off, val))
            if args.kind != "hex":
                print("raw: %s" % blob.hex())
            return True
        if args.action == "write-db":
            if args.real is not None:
                kind, value = "real", args.real
            elif args.intval is not None:
                kind, value = "int", args.intval
            elif args.dint is not None:
                kind, value = "dint", args.dint
            elif args.byte is not None:
                kind, value = "byte", args.byte
            else:
                kind, value = "hex", args.hexval
            data = encode_value(kind, value)
            print("[*] Write DB%d offset %d = %s (%s) [%s]"
                  % (args.db, args.start, value, kind, data.hex()))
            return client.write_db(args.db, args.start, data)
        if args.action == "cpu-state":
            state = client.cpu_state()
            print("[*] CPU state")
            print("cpu.state = %s" % state)
            return True
        if args.action == "cpu-stop":
            print("[*] CPU stop (S7 PLC Stop)")
            return client.cpu_stop()
        if args.action == "cpu-start":
            print("[*] CPU %s start" % ("hot" if args.hot else "cold"))
            return client.cpu_start(cold=not args.hot)
        if args.action == "read-szl":
            szl_id = int(str(args.szl_id), 0)
            print("[*] Read SZL 0x%04x" % szl_id)
            szl = client.read_szl(szl_id, int(str(args.index), 0))
            raw = bytes(getattr(szl, "data", szl) or b"")
            print("szl.%04x = %s" % (szl_id, raw.hex()[:120]))
            return True
        return False
    finally:
        client.close()


def main(argv=None):
    args = _build_parser().parse_args(argv)
    try:
        ok = _run(args)
    except (S7Error, ValueError) as exc:
        print("[!] %s" % exc, file=sys.stderr)
        return 2
    except Exception as exc:  # snap7 request errors (e.g. unsupported on target)
        print("[!] %s" % exc, file=sys.stderr)
        return 1
    if ok:
        print("[+] %s: ok" % args.action)
        return 0
    print("[!] %s: failed" % args.action, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

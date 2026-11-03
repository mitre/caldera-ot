# SPDX-License-Identifier: Apache-2.0
"""mbus_cli - a command-line M-Bus (Meter-Bus) client for adversary emulation.

A generic client that speaks M-Bus over TCP to any meter or TCP/M-Bus gateway.
Transport-only (numeric primary addresses); the meaning of each meter's records
belongs to the device. Driven from Caldera abilities, one subcommand per action.

    mbus_cli <host> [--port 5000] <action> [args]
"""
import argparse
import sys

from mbus import MBusClient, MBusError, __version__


def _build_parser():
    p = argparse.ArgumentParser(
        prog="mbus_cli",
        description="M-Bus (Meter-Bus) action library v%s" % __version__)
    p.add_argument("host", help="meter/gateway IP address or hostname")
    p.add_argument("-p", "--port", type=int, default=5000,
                   help="M-Bus/TCP port (default 5000)")
    p.add_argument("--timeout", type=float, default=10.0)
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="action", required=True, metavar="action")

    s = sub.add_parser("ping", help="probe a primary address (SND_NKE -> ACK)")
    s.add_argument("address", type=int)

    s = sub.add_parser("scan", help="ping a range of primary addresses")
    s.add_argument("--start", type=int, default=1)
    s.add_argument("--end", type=int, default=250)

    s = sub.add_parser("read", help="read a meter's data (REQ_UD2)")
    s.add_argument("address", type=int)

    s = sub.add_parser("app-reset", help="application reset (SND_UD, CI 0x50)")
    s.add_argument("address", type=int)

    sub.add_parser("broadcast-reset",
                   help="broadcast SND_NKE (0xFF) - re-init all slaves (DoS)")
    return p


def _run(args):
    with MBusClient(args.host, args.port, args.timeout) as c:
        if args.action == "ping":
            print("[*] Ping address %d" % args.address)
            ok = c.ping(args.address)
            print("device %d = %s" % (args.address, "present" if ok else "no response"))
            return ok
        if args.action == "scan":
            print("[*] Scan addresses %d-%d" % (args.start, args.end))
            present = c.scan(args.start, args.end)
            for addr in present:
                print("device %d = present" % addr)
            print("[*] %d device(s) found" % len(present))
            return True
        if args.action == "read":
            print("[*] Read meter %d" % args.address)
            frame, records = c.read(args.address)
            if not frame:
                return False
            for i, (value, unit) in enumerate(records):
                try:  # pyMeterBus returns Decimal/float; show it compactly
                    shown = "%g" % float(value)
                except (TypeError, ValueError):
                    shown = value
                print("record %d = %s %s" % (i, shown, unit or ""))
            if not records:
                print("raw = %s" % frame.hex())
            return frame[:1] == bytes([0x68])
        if args.action == "app-reset":
            print("[*] Application reset address %d" % args.address)
            return c.application_reset(args.address)
        if args.action == "broadcast-reset":
            print("[*] Broadcast reset (SND_NKE to 0xFF)")
            return c.broadcast_reset()
        return False


def main(argv=None):
    args = _build_parser().parse_args(argv)
    try:
        ok = _run(args)
    except MBusError as exc:
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

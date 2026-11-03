# SPDX-License-Identifier: Apache-2.0
"""Unit tests for the mbus_cli action library.

Stands up a tiny in-process M-Bus/TCP server that answers SND_NKE with an ACK and
REQ_UD2 with a canned RSP_UD telegram, then drives it with MBusClient.
"""
import socket
import threading

import pytest

from mbus import MBusClient, MBusError
from mbus.client import long_frame, short_frame

# A real RSP_UD telegram captured from an M-Bus water meter (4 data records).
RSP_UD = bytes.fromhex(
    "682323680801724e61bc00414d0107000000000413d21b000004480e10000002597706023b0000ff16")


@pytest.fixture(scope="module")
def server():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(5)
    srv.settimeout(0.5)
    port = srv.getsockname()[1]
    running = {"on": True}

    def handle(conn):
        with conn:
            while running["on"]:
                try:
                    data = conn.recv(256)
                except OSError:
                    return
                if not data:
                    return
                if data[0] == 0x10:            # short frame
                    c = data[1]
                    if c in (0x5B, 0x7B):       # REQ_UD2 -> data
                        conn.sendall(RSP_UD)
                    else:                       # SND_NKE / other -> ACK
                        conn.sendall(b"\xe5")
                elif data[0] == 0x68:          # long frame -> ACK
                    conn.sendall(b"\xe5")

    def accept_loop():
        while running["on"]:
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            threading.Thread(target=handle, args=(conn,), daemon=True).start()

    t = threading.Thread(target=accept_loop, daemon=True)
    t.start()
    yield {"port": port}
    running["on"] = False
    srv.close()


def test_frame_builders():
    assert short_frame(0x40, 1) == bytes([0x10, 0x40, 0x01, 0x41, 0x16])
    lf = long_frame(0x53, 1, 0x50)
    assert lf[0] == 0x68 and lf[-1] == 0x16


def test_ping_and_scan(server):
    with MBusClient("127.0.0.1", server["port"]) as c:
        assert c.ping(1) is True
        assert c.scan(1, 3) == [1, 2, 3]


def test_read_decodes_records(server):
    with MBusClient("127.0.0.1", server["port"]) as c:
        frame, records = c.read(1)
        assert frame[:1] == bytes([0x68])
        assert len(records) >= 1
        assert any(u == "m^3" for _v, u in records)  # pyMeterBus decoded the volume


def test_application_reset(server):
    with MBusClient("127.0.0.1", server["port"]) as c:
        assert c.application_reset(1) is True


def test_unresolvable_host_raises():
    with pytest.raises(MBusError):
        MBusClient("no.such.host.invalid.")

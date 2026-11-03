# SPDX-License-Identifier: Apache-2.0
"""Unit tests for the s7comm_cli action library.

Stands up a local snap7 server with a data block and drives it with S7Client,
asserting the read/write actions actually reach the block. Tests fail without the
client logic.
"""
import ctypes
import struct
import time

import pytest
import snap7
from snap7.server import Server
from snap7.type import SrvArea

from s7comm import S7Client, S7Error
from s7comm.client import decode_values, encode_value

PORT = 1102
DB = 1


@pytest.fixture(scope="module")
def server():
    srv = Server()
    buf = (ctypes.c_ubyte * 32)()
    struct.pack_into(">f", buf, 0, 1007.0)  # DB1.0 = REAL 1007.0
    srv.register_area(SrvArea.DB, DB, buf)
    srv.start(tcp_port=PORT)
    time.sleep(0.5)
    yield {"srv": srv, "buf": buf}
    srv.stop()
    srv.destroy()


@pytest.fixture
def client(server):
    c = S7Client(host="127.0.0.1", rack=0, slot=1, port=PORT)
    c.connect()
    yield c
    c.close()


def test_encode_decode_roundtrip():
    assert encode_value("real", 1.5) == struct.pack(">f", 1.5)
    assert encode_value("int", -3) == struct.pack(">h", -3)
    assert decode_values(struct.pack(">f", 2.5), "real")[0][1] == 2.5


def test_read_db(server, client):
    blob = client.read_db(DB, 0, 4)
    assert struct.unpack(">f", blob)[0] == pytest.approx(1007.0)


def test_write_db_reaches_block(server, client):
    client.write_db(DB, 0, encode_value("real", 1410.0))  # Stuxnet-style over-speed
    time.sleep(0.2)
    # Verify via a protocol read-back (independent of snap7's buffer internals).
    blob = client.read_db(DB, 0, 4)
    assert struct.unpack(">f", blob)[0] == pytest.approx(1410.0)


def test_unresolvable_host_raises():
    with pytest.raises(S7Error):
        S7Client(host="no.such.host.invalid.")

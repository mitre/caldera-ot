# SPDX-License-Identifier: Apache-2.0
"""S7comm (Siemens S7) client actions, backed by python-snap7.

Transport-only: it takes numeric DB numbers / offsets / values and has no knowledge
of any particular device, so it works against any S7 PLC or snap7 outstation.
"""
import socket
import struct

import snap7


class S7Error(Exception):
    """Raised on connection failure or a rejected S7 request."""


def encode_value(kind, value):
    """Encode a scalar into big-endian S7 bytes (S7 is big-endian)."""
    if kind == "real":
        return struct.pack(">f", float(value))
    if kind == "int":
        return struct.pack(">h", int(value))
    if kind == "dint":
        return struct.pack(">i", int(value))
    if kind == "byte":
        return bytes([int(value) & 0xFF])
    if kind == "hex":
        return bytes.fromhex(str(value).replace(" ", ""))
    raise ValueError(f"unknown value kind {kind!r}")


def decode_values(blob, kind):
    """Decode raw bytes into a list of (offset, value) for display/parsing."""
    out = []
    if kind == "real":
        for off in range(0, len(blob) - 3, 4):
            out.append((off, round(struct.unpack_from(">f", blob, off)[0], 4)))
    elif kind == "int":
        for off in range(0, len(blob) - 1, 2):
            out.append((off, struct.unpack_from(">h", blob, off)[0]))
    else:  # hex / raw
        out.append((0, blob.hex()))
    return out


class S7Client:
    def __init__(self, host, rack=0, slot=1, port=102, timeout=10.0):
        # snap7's native layer wants a numeric address; resolve hostnames.
        try:
            self.host = socket.gethostbyname(host)
        except socket.gaierror as exc:
            raise S7Error(f"cannot resolve host {host!r}: {exc}") from exc
        self.rack = int(rack)
        self.slot = int(slot)
        self.port = int(port)
        self._client = snap7.client.Client()

    def connect(self):
        try:
            self._client.connect(self.host, self.rack, self.slot, self.port)
        except Exception as exc:  # snap7 raises its own exception types
            raise S7Error(f"could not connect to {self.host}:{self.port} "
                          f"(rack {self.rack}, slot {self.slot}): {exc}") from exc
        if not self._client.get_connected():
            raise S7Error(f"connection to {self.host}:{self.port} not established")
        return True

    def close(self):
        try:
            self._client.disconnect()
        except Exception:
            pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *_exc):
        self.close()

    # -- data blocks ----------------------------------------------------------
    def read_db(self, db, start, size):
        return bytes(self._client.db_read(int(db), int(start), int(size)))

    def write_db(self, db, start, data):
        self._client.db_write(int(db), int(start), bytearray(data))
        return True

    # -- cpu control ----------------------------------------------------------
    def cpu_state(self):
        return self._client.get_cpu_state()

    def cpu_stop(self):
        self._client.plc_stop()
        return True

    def cpu_start(self, cold=True):
        if cold:
            self._client.plc_cold_start()
        else:
            self._client.plc_hot_start()
        return True

    def read_szl(self, szl_id, index=0):
        return self._client.read_szl(int(szl_id), int(index))

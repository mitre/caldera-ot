# SPDX-License-Identifier: Apache-2.0
"""M-Bus (EN 13757) master actions over TCP.

Frames are built by hand (M-Bus framing is small and well-defined); read responses
are decoded with pyMeterBus when available. Transport-only: it takes numeric primary
addresses and has no knowledge of any particular meter, so it works against any
M-Bus device or TCP/M-Bus gateway.
"""
import socket

try:
    import meterbus
except Exception:  # pragma: no cover - decoding is optional
    meterbus = None

START_SHORT = 0x10
START_LONG = 0x68
STOP = 0x16
ACK = 0xE5
BROADCAST = 0xFF

C_SND_NKE = 0x40   # initialize / link reset
C_SND_UD = 0x53    # send user data (write)
C_REQ_UD2 = 0x5B   # request class-2 data (read)
CI_APPLICATION_RESET = 0x50


class MBusError(Exception):
    """Raised on connection failure or a malformed exchange."""


def _checksum(payload):
    return sum(payload) & 0xFF


def short_frame(c_field, address):
    return bytes([START_SHORT, c_field, address, _checksum([c_field, address]), STOP])


def long_frame(c_field, address, ci_field, data=b""):
    payload = bytes([c_field, address, ci_field]) + data
    length = len(payload)
    return (bytes([START_LONG, length, length, START_LONG]) + payload
            + bytes([_checksum(payload), STOP]))


class MBusClient:
    def __init__(self, host, port=5000, timeout=10.0):
        try:
            self.host = socket.gethostbyname(host)
        except socket.gaierror as exc:
            raise MBusError(f"cannot resolve host {host!r}: {exc}") from exc
        self.port = int(port)
        self.timeout = float(timeout)
        self._sock = None

    def connect(self):
        try:
            self._sock = socket.create_connection((self.host, self.port), self.timeout)
        except OSError as exc:
            raise MBusError(f"could not connect to {self.host}:{self.port}: {exc}") from exc
        self._sock.settimeout(self.timeout)
        return True

    def close(self):
        try:
            self._sock.close()
        except Exception:
            pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *_exc):
        self.close()

    def _send(self, frame, bufsize=512):
        self._sock.sendall(frame)
        try:
            return self._sock.recv(bufsize)
        except socket.timeout:
            return b""

    # -- actions --------------------------------------------------------------
    def ping(self, address):
        """SND_NKE -> expect ACK (0xE5): is a device answering at this address?"""
        return self._send(short_frame(C_SND_NKE, address), 8)[:1] == bytes([ACK])

    def scan(self, start, end):
        present = []
        for addr in range(int(start), int(end) + 1):
            if self.ping(addr):
                present.append(addr)
        return present

    def read(self, address):
        """SND_NKE then REQ_UD2 -> RSP_UD; returns (raw_frame, [(value, unit), ...])."""
        self._send(short_frame(C_SND_NKE, address), 8)   # init the link
        frame = self._send(short_frame(C_REQ_UD2, address))
        records = []
        if meterbus is not None and frame[:1] == bytes([START_LONG]):
            try:
                telegram = meterbus.load(frame)
                for rec in getattr(telegram, "records", []):
                    records.append((getattr(rec, "value", None),
                                    getattr(rec, "unit", None)))
            except Exception:
                pass
        return frame, records

    def application_reset(self, address):
        """SND_UD with CI = application reset (0x50) -> ACK."""
        frame = long_frame(C_SND_UD, address, CI_APPLICATION_RESET)
        return self._send(frame, 8)[:1] == bytes([ACK])

    def broadcast_reset(self):
        """Broadcast SND_NKE (address 0xFF): re-initialize every slave at once.

        Sent to all devices, this is a denial-of-service primitive against an M-Bus
        segment / gateway. No reply is expected.
        """
        self._sock.sendall(short_frame(C_SND_NKE, BROADCAST))
        return True

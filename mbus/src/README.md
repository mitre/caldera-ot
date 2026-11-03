# mbus_cli, payload source

`mbus_cli` is a command-line M-Bus (Meter-Bus) client used by the Caldera `mbus`
plugin abilities. It builds M-Bus frames by hand and decodes read responses with
[pyMeterBus](https://pypi.org/project/pyMeterBus/).

## Actions

```
mbus_cli <host> [--port 5000] <action>

  ping <address>                     SND_NKE -> ACK (device present?)
  scan [--start 1] [--end 250]       ping a range of addresses
  read <address>                     REQ_UD2 -> RSP_UD, decoded records
  app-reset <address>                SND_UD (CI 0x50) application reset
  broadcast-reset                    broadcast SND_NKE (0xFF) - re-init all (DoS)
```

Exit `0` = ok, `1` = request failed, `2` = connect/arg error.

## Build

```
make build/local      # -> dist/mbus_cli  (needs Python 3.10+)
make update           # copy dist/* into ../payloads/
make build/linux      # reproducible Docker build (Linux)
make build/windows    # reproducible Docker build (Windows)
```

The Linux binary is built against glibc 2.35 (runs on glibc >= 2.35); Windows/macOS
binaries come from the release CI.

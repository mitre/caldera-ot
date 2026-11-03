# s7comm_cli, payload source

`s7comm_cli` is a command-line Siemens S7 (S7comm) client used by the Caldera
`s7comm` plugin abilities. It wraps [python-snap7](https://pypi.org/project/python-snap7/)
and exposes one subcommand per action.

## Actions

```
s7comm_cli <host> [--rack 0] [--slot 1] [--port 102] <action>

  read-db <db> <start> <size> [--as hex|real|int]      S7 Read Var
  write-db <db> <start> (--real F|--int N|--dint N|--byte N|--hex HH)   S7 Write Var
  cpu-state                                            read CPU run/stop state
  cpu-stop                                             S7 PLC Stop
  cpu-start [--hot]                                    S7 PLC Cold/Hot Start
  read-szl <szl_id> [--index N]                        read a System Status List
```

Exit `0` = ok, `1` = request failed/unsupported on target, `2` = connect/arg error.

## Build

```
make build/local      # -> dist/s7comm_cli  (needs Python 3.10+)
make update           # copy dist/* into ../payloads/
make build/linux      # reproducible Docker build (Linux)
make build/windows    # reproducible Docker build (Windows)
```

The spec bundles the native `snap7` shared library (`collect_all('snap7')`). The
Linux binary is built against glibc 2.35 (runs on glibc >= 2.35); Windows/macOS
binaries come from the release CI.

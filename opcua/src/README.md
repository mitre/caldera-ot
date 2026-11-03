# opcua_cli, payload source

`opcua_cli` is a command-line OPC-UA client used by the Caldera `opcua` plugin
abilities. It wraps [asyncua](https://pypi.org/project/asyncua/) and exposes one
subcommand per action.

## Actions

```
opcua_cli <endpoint> [--port 4840] [--user U] [--password P] <action>

  browse [--node <id>] [--depth N]                   browse the address space
  read <node>                                        read a node value
  write <node> <value> [--type bool|int|float|string]  write a node value
  endpoints                                          list server endpoints
  call-method <object> <method> [args...]            call a method
```

`endpoint` may be a bare host/IP (with `--port`) or a full `opc.tcp://host:port` URL.
Exit `0` = ok, `1` = request failed, `2` = connect/arg error.

## Build

```
make build/local      # -> dist/opcua_cli  (needs Python 3.10+)
make update           # copy dist/* into ../payloads/
make build/linux      # reproducible Docker build (Linux)
make build/windows    # reproducible Docker build (Windows)
```

The spec collects asyncua (`collect_all` + submodules). The Linux binary is built
against glibc 2.35 (runs on glibc >= 2.35); Windows/macOS binaries come from the
release CI.

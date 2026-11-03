# SPDX-License-Identifier: Apache-2.0
# Build the s7comm_cli payload with PyInstaller.
#
#   make build/local     build for the host platform
#   make build/linux     build a Linux binary in a pinned Docker image
#   make build/windows   build a Windows binary in a pinned Docker image
#   make update          copy freshly built binaries into ../payloads
#   make clean

PYI := pyinstaller --clean s7comm_cli.spec
DOCKER_LINUX := batonogov/pyinstaller-linux:latest
DOCKER_WINDOWS := batonogov/pyinstaller-windows:latest

.PHONY: build/local build/linux build/windows update clean

build/local:
	pip install -r requirements.txt pyinstaller
	$(PYI)

build/linux:
	docker run --rm --volume "$(CURDIR):/src/" --entrypoint /bin/sh $(DOCKER_LINUX) \
		-c "pip install -r requirements.txt && $(PYI)"

build/windows:
	docker run --rm --volume "$(CURDIR):/src/" --entrypoint /bin/sh $(DOCKER_WINDOWS) \
		-c "pip install -r requirements.txt && $(PYI)"

update:
	cp dist/* ../payloads/

clean:
	rm -rf build dist __pycache__ s7comm/__pycache__

# SPDX-License-Identifier: Apache-2.0
from app.utility.base_world import BaseWorld
from plugins.opcua.app.opcua_svc import OPCUAService

name = 'OPCUA'
description = ('The OPC-UA plugin for Caldera provides adversary emulation abilities '
              'specific to the OPC Unified Architecture protocol.')
address = '/plugin/opcua/gui'
access = BaseWorld.Access.RED


async def enable(services):
    opcua_svc = OPCUAService(services, name, description)
    app = services.get('app_svc').application
    app.router.add_route('GET', '/plugin/opcua/gui', opcua_svc.splash)
    app.router.add_route('GET', '/plugin/opcua/data', opcua_svc.plugin_data)

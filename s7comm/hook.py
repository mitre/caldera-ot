# SPDX-License-Identifier: Apache-2.0
from app.utility.base_world import BaseWorld
from plugins.s7comm.app.s7comm_svc import S7commService

name = 'S7comm'
description = ('The S7comm plugin for Caldera provides adversary emulation abilities '
              'specific to the Siemens S7 (S7comm) protocol.')
address = '/plugin/s7comm/gui'
access = BaseWorld.Access.RED


async def enable(services):
    s7comm_svc = S7commService(services, name, description)
    app = services.get('app_svc').application
    app.router.add_route('GET', '/plugin/s7comm/gui', s7comm_svc.splash)
    app.router.add_route('GET', '/plugin/s7comm/data', s7comm_svc.plugin_data)

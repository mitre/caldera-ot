# SPDX-License-Identifier: Apache-2.0
from app.utility.base_world import BaseWorld
from plugins.mbus.app.mbus_svc import MBusService

name = 'MBus'
description = ('The M-Bus plugin for Caldera provides adversary emulation abilities '
              'specific to the Meter-Bus (M-Bus, EN 13757) protocol.')
address = '/plugin/mbus/gui'
access = BaseWorld.Access.RED


async def enable(services):
    mbus_svc = MBusService(services, name, description)
    app = services.get('app_svc').application
    app.router.add_route('GET', '/plugin/mbus/gui', mbus_svc.splash)
    app.router.add_route('GET', '/plugin/mbus/data', mbus_svc.plugin_data)

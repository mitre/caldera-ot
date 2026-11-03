# SPDX-License-Identifier: Apache-2.0
from app.utility.base_world import BaseWorld
from plugins.iec104.app.iec104_svc import IEC104Service

name = 'IEC104'
description = ('The IEC 104 plugin for Caldera provides adversary emulation abilities '
              'specific to the IEC 60870-5-104 telecontrol protocol.')
address = '/plugin/iec104/gui'
access = BaseWorld.Access.RED


async def enable(services):
    iec104_svc = IEC104Service(services, name, description)
    app = services.get('app_svc').application
    app.router.add_route('GET', '/plugin/iec104/gui', iec104_svc.splash)
    app.router.add_route('GET', '/plugin/iec104/data', iec104_svc.plugin_data)

# SPDX-License-Identifier: Apache-2.0
import logging

from aiohttp import web
from aiohttp_jinja2 import template


class S7commService:
    def __init__(self, services, name, description):
        self.name = name
        self.description = description
        self.services = services
        self.data_svc = services.get('data_svc')
        self.log = logging.getLogger('s7comm_svc')

    @template('s7comm.html')
    async def splash(self, request):
        return await self._get_plugin_data()

    async def plugin_data(self, request):
        return web.json_response(await self._get_plugin_data())

    async def _get_plugin_data(self):
        abilities = {
            a.ability_id: {
                'name': a.name,
                'tactic': a.tactic,
                'technique_id': a.technique_id,
                'technique_name': a.technique_name,
                'description': a.description.replace('\n', '<br>'),
            }
            for a in await self.data_svc.locate('abilities')
            if await a.which_plugin() == 's7comm'
        }
        return dict(name=self.name, description=self.description,
                    abilities=list(abilities.values()))

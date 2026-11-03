# SPDX-License-Identifier: Apache-2.0
import re

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

# Matches the payload's interrogation output lines, e.g. "point 100 = 31047".
POINT_RE = re.compile(r"^point\s+(\d+)\s*=\s*(.+)$")


class Parser(BaseParser):
    """Turn an interrogation's reported points into iec104.point.* facts.

    Each 'point <ioa> = <value>' line becomes a relationship linking the point's
    information object address to its value, so later abilities can reference
    discovered points.
    """

    def parse(self, blob):
        relationships = []
        for line in self.line(blob):
            match = POINT_RE.fullmatch(line.strip())
            if not match:
                continue
            facts = {
                'iec104.point.ioa': match.group(1),
                'iec104.point.value': match.group(2).strip(),
            }
            for mp in self.mappers:
                source = facts.get(mp.source)
                target = facts.get(mp.target)
                if mp.edge and (source is None or target is None):
                    continue
                relationships.append(Relationship(
                    source=Fact(mp.source, source),
                    edge=mp.edge,
                    target=Fact(mp.target, target),
                ))
        return relationships

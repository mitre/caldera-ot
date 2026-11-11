# SPDX-License-Identifier: Apache-2.0
import re

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

# Matches the payload's read output lines, e.g. "record 0 = 6.078 m^3".
RECORD_RE = re.compile(r"^record\s+\d+\s*=\s*(\S+)\s*(.*)$")


class Parser(BaseParser):
    """Turn read output into mbus.record.* facts (value -> unit)."""

    def parse(self, blob):
        relationships = []
        for line in self.line(blob):
            match = RECORD_RE.fullmatch(line.strip())
            if not match:
                continue
            facts = {
                'mbus.record.value': match.group(1),
                'mbus.record.unit': match.group(2).strip() or 'none',
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

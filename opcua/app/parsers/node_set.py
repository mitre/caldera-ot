# SPDX-License-Identifier: Apache-2.0
import re

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

# Matches the payload's browse output lines, e.g. "node ns=2;i=9 = Temperature".
NODE_RE = re.compile(r"^node\s+(\S+)\s*=\s*(.+)$")


class Parser(BaseParser):
    """Turn browse output into opcua.node.* facts (node id -> browse name)."""

    def parse(self, blob):
        relationships = []
        for line in self.line(blob):
            match = NODE_RE.fullmatch(line.strip())
            if not match:
                continue
            facts = {
                'opcua.node.id': match.group(1),
                'opcua.node.name': match.group(2).strip(),
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

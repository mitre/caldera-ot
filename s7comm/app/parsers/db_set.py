# SPDX-License-Identifier: Apache-2.0
import re

from app.objects.secondclass.c_fact import Fact
from app.objects.secondclass.c_relationship import Relationship
from app.utility.base_parser import BaseParser

# Matches the payload's read-db output lines, e.g. "db3.0 = 1410.0".
DB_RE = re.compile(r"^db(\d+)\.(\d+)\s*=\s*(.+)$")


class Parser(BaseParser):
    """Turn read-db output into s7comm.db.* facts (address -> value)."""

    def parse(self, blob):
        relationships = []
        for line in self.line(blob):
            match = DB_RE.fullmatch(line.strip())
            if not match:
                continue
            facts = {
                's7comm.db.address': f"{match.group(1)}.{match.group(2)}",
                's7comm.db.value': match.group(3).strip(),
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

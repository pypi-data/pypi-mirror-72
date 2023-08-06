# Copyright (C) 2020  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from .base import SCHEMA_URL, CandidateMessage, ELECTION_SCHEMA, CANDIDATE_SCHEMA


class NewCandidateV1(CandidateMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by Elections when a new candidate is added.
    """

    topic = "fedora_elections.candidate.new"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new candidate is added",
        "type": "object",
        "properties": {
            "agent": {"type": "string"},
            "election": ELECTION_SCHEMA,
            "candidate": CANDIDATE_SCHEMA,
        },
        "required": ["agent", "election", "candidate"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return (
            "New Candidate for Election: {election}\nBy: {agent}\nCandidate: {candidate}\n"
        ).format(
            election=self.body["election"]["shortdesc"],
            agent=self.body["agent"],
            candidate=self.body["candidate"]["name"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        if self.body["candidate"].get("fas_name"):
            msg = (
                '{agent} added candidate "{candidate_name}" ({candidate_fas_name}) '
                'for election "{title}" ({alias})'
            )
        else:
            msg = '{agent} added candidate "{candidate_name}" for election "{title}" ({alias})'
        return msg.format(
            agent=self.body["agent"],
            candidate_name=self.body["candidate"]["name"],
            candidate_fas_name=self.body["candidate"].get("fas_name"),
            title=self.body["election"]["shortdesc"],
            alias=self.body["election"]["alias"],
        )

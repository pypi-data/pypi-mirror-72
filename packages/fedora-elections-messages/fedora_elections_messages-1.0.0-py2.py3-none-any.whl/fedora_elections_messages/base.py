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

from fedora_messaging import message
from fedora_messaging.schema_utils import user_avatar_url


SCHEMA_URL = "http://fedoraproject.org/message-schema/"

ELECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "shortdesc": {"type": "string"},
        "alias": {"type": "string"},
        "description": {"type": "string"},
        "url": {"type": "string", "format": "uri"},
        "start_date": {"type": "string"},
        "end_date": {"type": "string"},
        "embargoed": {"type": "number"},
        "voting_type": {"type": "string"},
    },
    "required": [
        "shortdesc",
        "alias",
        "description",
        "url",
        "start_date",
        "end_date",
        "embargoed",
        "voting_type",
    ],
}

CANDIDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "fas_name": {"type": "string"},
        "url": {"type": "string", "format": "uri"},
    },
    "required": ["name", "url"],
}


class ElectionsMessage(message.Message):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by Elections.
    """

    @property
    def app_name(self):
        return "elections"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/elections.png"
        # return "https://elections.fedoraproject.org/static/images/elections_logo.png"

    @property
    def agent(self):
        return self.body.get("agent")

    @property
    def agent_avatar(self):
        return user_avatar_url(self.agent)

    @property
    def usernames(self):
        return [self.agent]

    @property
    def url(self):
        return self.body["election"]["url"]


class CandidateMessage(ElectionsMessage):
    @property
    def usernames(self):
        value = super().usernames
        candidate_fas_name = self.body["candidate"].get("fas_name")
        if candidate_fas_name:
            value.append(candidate_fas_name)
        value.sort()
        return value

    @property
    def candidate(self):
        return self.body["candidate"]

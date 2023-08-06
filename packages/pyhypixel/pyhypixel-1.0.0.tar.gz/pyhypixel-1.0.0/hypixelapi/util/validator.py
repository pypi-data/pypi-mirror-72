# A Python3 HypixelAPI wrapper
#     Copyright (C) 2020  Michele Viotto

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
A validator module to valide api keys, uuids and usernames
"""
import re
import requests

from hypixelapi.exceptions import ApiKeyNotValidException


UUID_MATCH = r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$'
USERNAME_MATCH = r'^\w{1,16}$'


def is_valid_api_key(api_key):
    if is_uuid(api_key):
        response = requests.get(f'https://api.hypixel.net/key?key={api_key}').json()
        if response['success']:
            return True

    raise ApiKeyNotValidException("Api Key is not valid")

def is_uuid(uuid):
    return (
        isinstance(uuid, str) and
        len(uuid) in (32, 36) and
        re.match(UUID_MATCH, uuid)
    )


def is_username(username):
    return (
        isinstance(username, str) and
        0 < len(username) <= 16 and
        re.match(USERNAME_MATCH, username)
    )

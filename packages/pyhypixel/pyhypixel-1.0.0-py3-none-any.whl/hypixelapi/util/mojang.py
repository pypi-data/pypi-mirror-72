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
import requests

from hypixelapi.exceptions import UsernameNotValidException


def get_uuid_by_name(username):
    response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
    if response.status_code == 204:
        raise UsernameNotValidException("Username is not valid.")

    response = response.json()

    return response['id']

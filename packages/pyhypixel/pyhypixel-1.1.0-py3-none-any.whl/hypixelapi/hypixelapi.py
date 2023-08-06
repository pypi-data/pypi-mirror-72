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
A Python HypixelAPI wrapper.
"""
from math import floor, sqrt

from .util import validator
from .util import mojang
from .util import general
from .util import GameType
from .exceptions import GameTypeNotValidException, GuildIdNotValidException


BASE_URL = 'https://api.hypixel.net/'


class HypixelAPI:
    """
    Represents the HypixelAPI object with general methods.
    """

    def __init__(self, api_key):
        self.set_api_key(api_key)


    def set_api_key(self, api_key):
        if validator.is_valid_api_key(api_key):
            self.api_key = api_key


    def get_api_key(self):
        """
        Returns a dict containing information regarding the api key.
        """
        response = general.do_request(BASE_URL, 'key', {'key': self.api_key})

        return response.json()['record']


    def get_player(self, player):
        """
        player: string username or uuid.
        """
        return Player(player, self.api_key)


    def get_guild_by_id(self, guild_id):
        """
        Returns a Guild instance
        """
        return Guild(guild_id, self.api_key)


    def get_guild_by_name(self, guild_name):
        """
        Returns a Guild instance
        """
        response = general.do_request(
            BASE_URL,
            'findGuild',
            {'key': self.api_key, 'byName': guild_name}
        ).json()

        return self.get_guild_by_id(response['guild'])


    def get_leaderboards(self, game_type=None):
        """
        Returns a dict containing leaderboards.
        game_type = None -> Every game
        game_type = GameType enum -> Specified game
        """
        response = general.do_request(BASE_URL, 'leaderboards', {'key': self.api_key}).json()

        if game_type is not None:
            if isinstance(game_type, GameType):
                return response['leaderboards'][game_type.name]

            raise GameTypeNotValidException("Game type is not an instance of GameType")

        return response['leaderboards']


    def get_boosters(self):
        """
        Returns Hypixel boosters
        """
        response = general.do_request(BASE_URL, 'boosters', {'key': self.api_key})

        return response.json()


    def get_player_count(self):
        """
        Returns current player count
        """
        response = general.do_request(BASE_URL, 'playerCount', {'key': self.api_key}).json()

        return response['playerCount']


    def get_game_counts(self, game_type=None):
        """
        Returns a dict containing game counts.
        game_type = None -> Every game
        game_type = GameType enum -> Specified game
        """
        response = general.do_request(BASE_URL, 'gameCounts', {'key': self.api_key}).json()

        if game_type is not None:
            if isinstance(game_type, GameType):
                return response['games'][game_type.name]

            raise GameTypeNotValidException("Game type is not an instance of GameType")

        return response['games']


    def get_watchdog_stats(self):
        """
        Returns dict containing statistics about Watchdog and staff bans
        """
        response = general.do_request(BASE_URL, 'watchdogstats', {'key': self.api_key}).json()

        return response


    def get_skyblock_auctions(self, page=0):
        """
        Returns a dict containing a page of max 1000 skyblock auctions
        if page doesn't exists returns a 'Page not found'
        """
        response = general.do_request(
            BASE_URL,
            'skyblock/auctions',
            {'key': self.api_key, 'page': page}
        ).json()

        if 'cause' in response:
            return response['cause']

        return response


    def get_skyblock_bazaar(self):
        """
        Returns a dict of products with their sell and buy summary and quick status
        """
        response = general.do_request(BASE_URL, 'skyblock/bazaar', {'key': self.api_key}).json()

        return response


    def get_skyblock_news(self):
        """
        Returns a dict containing skyblock news with a title, description and thread
        """
        response = general.do_request(BASE_URL, 'skyblock/news', {'key': self.api_key}).json()

        return response['items']


class Player:
    """
    Represents Hypixel Player object.
    """

    def __init__(self, player, api_key):
        if validator.is_uuid(player):
            self.uuid = player
        else:
            self.uuid = mojang.get_uuid_by_name(player)

        if validator.is_valid_api_key(api_key):
            self.api_key = api_key

        self.raw_player = self.get_raw_player()


    def get_name(self):
        """
        Returns player name.

        New in version 1.1.0
        """
        return self.raw_player['displayname']


    def get_achievements(self):
        """
        Returns a dict containing all the player achievements.

        New in version 1.1.0
        """
        return self.raw_player['achievements']


    def get_stats(self, game_type=None):
        """
        Args:
        game_type: if None returns all games, if GameType enum returns specified game.
        Returns a dict containing all the player stats.

        New in version 1.1.0
        """
        stats = self.raw_player['stats']

        if game_type is not None:
            if isinstance(game_type, GameType):
                return stats[game_type.db_name]

            raise GameTypeNotValidException("Game type is not an instance of GameType")

        return stats


    def get_exp(self):
        """
        Returns player exp

        New in version 1.1.0
        """
        return self.raw_player['networkExp']


    def get_level(self):
        """
        Returns player level.
        This is basically a copy of 
        https://github.com/Plancke/hypixel-php/blob/master/src/util/Leveling.php

        New in version 1.1.0
        """
        BASE = 10000
        GROWTH = 2500

        # Constants to generate the total amount of XP to complete a level
        HALF_GROWTH = 0.5 * GROWTH

        # Constants to look up the level from the total amount of XP
        REVERSE_PQ_PREFIX = -(BASE - HALF_GROWTH) / GROWTH
        REVERSE_CONST = REVERSE_PQ_PREFIX * REVERSE_PQ_PREFIX
        GROWTH_DIVIDES_2 = 2 / GROWTH

        exp = self.get_exp()

        if exp < 0:
            return 1

        return floor(1 + REVERSE_PQ_PREFIX + sqrt(REVERSE_CONST + GROWTH_DIVIDES_2 * exp))


    def get_friends(self):
        """
        Returns a dict containg a list of Player's friends.
        """
        response = general.do_request(BASE_URL, 'friends', {'key': self.api_key, 'uuid': self.uuid})
        return response.json()['records']


    def get_status(self):
        """
        Returns a dict containing player status.
        """
        response = general.do_request(BASE_URL, 'status', {'key': self.api_key, 'uuid': self.uuid})

        return response.json()['session']


    def get_recent_games(self):
        """
        Returns a dict containing a list of max 100 recent games (stored 3 days).
        """
        response = general.do_request(
            BASE_URL,
            'recentGames',
            {'key': self.api_key, 'uuid': self.uuid}
        )

        return response.json()['games']


    def get_skyblock_auctions(self):
        """
        Returns a dict containing a list of the current player auctions
        """
        response = general.do_request(
            BASE_URL,
            'skyblock/auction',
            {'key': self.api_key, 'uuid': self.uuid}
        ).json()

        return response['auctions']


    def get_skyblock_profiles(self):
        """
        Returns a dict containing a list of the current player skyblock's profiles
        """
        response = general.do_request(
            BASE_URL,
            'skyblock/profiles',
            {'key': self.api_key, 'uuid': self.uuid}
        ).json()

        return response['profiles']


    def get_guild(self):
        """
        Returns current player guild
        """
        response = general.do_request(
            BASE_URL,
            'findGuild',
            {'key': self.api_key, 'byUuid': self.uuid}
        ).json()

        return Guild(response['guild'], self.api_key)


    def get_raw_player(self):
        """
        Returns raw json of the player

        New in version 1.1.0
        """
        response = general.do_request(
            BASE_URL,
            'player',
            {'key': self.api_key, 'uuid': self.uuid}
        ).json()

        return response['player']


class Guild():
    """
    Represents Hypixel Guild object
    """

    def __init__(self, guild_id, api_key):
        if guild_id is not None:
            self.guild_id = guild_id
        else:
            raise GuildIdNotValidException("Guild id is not valid.")
        if validator.is_valid_api_key(api_key):
            self.api_key = api_key
        self.raw_guild = self.get_raw_guild()


    def get_id(self):
        """
        Returns guild id
        """
        return self.guild_id


    def get_name(self):
        """
        Returns guild name
        """
        return self.raw_guild['name']


    def get_description(self):
        """
        Returns guild description
        """
        if 'description' in self.raw_guild.keys():
            return self.raw_guild['description']

        return None


    def get_tag(self):
        """
        Returns guild tag
        """
        if 'tag' in self.raw_guild.keys():
            return self.raw_guild['tag']

        return None


    def get_members(self):
        """
        Returns a dict containing guild members
        """
        if 'members' in self.raw_guild.keys():
            return self.raw_guild['members']

        return None


    def get_achievements(self):
        """
        Returns a dict containing guild achievements and current progress
        """
        if 'achievements' in self.raw_guild.keys():
            return self.raw_guild['achievements']

        return None


    def get_ranks(self):
        """
        Returns a dict containing guild ranks
        """
        if 'ranks' in self.raw_guild.keys():
            return self.raw_guild['ranks']

        return None


    def get_exp(self):
        """
        Returns guild exp.

        New in version 1.1.0
        """
        return self.raw_guild['exp']


    def get_raw_guild(self):
        """
        Returns raw json of the guild
        """
        response = general.do_request(
            BASE_URL,
            'guild',
            {'key': self.api_key, 'id': self.guild_id}
        ).json()

        if 'cause' in response.keys():
            raise GuildIdNotValidException(response['cause'])

        if response['guild'] is None:
            raise GuildIdNotValidException("Guild id is not valid.")

        return response['guild']

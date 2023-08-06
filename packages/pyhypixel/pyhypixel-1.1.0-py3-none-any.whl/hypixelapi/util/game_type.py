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
from enum import Enum


class GameType(Enum):

    QUAKECRAFT = ("Quakecraft", "Quake", 2)
    WALLS = ("Walls", "Walls", 3)
    PAINTBALL = ("Paintball", "Paintball", 4)
    SURVIVAL_GAMES = ("Blitz Survival Games", "HungerGames", 5)
    TNTGAMES = ("The TNT Games", "TNTGames", 6)
    VAMPIREZ = ("VampireZ", "VampireZ", 7)
    WALLS3 = ("Mega Walls", "Walls3", 13)
    ARCADE = ("Arcade", "Arcade", 14)
    ARENA = ("Arena Brawl", "Arena", 17)
    MCGO = ("Cops and Crims", "MCGO", 21)
    UHC = ("UHC Champions", "UHC", 20)
    BATTLEGROUND = ("Warlords", "Battleground", 23)
    SUPER_SMASH = ("Smash Heroes", "SuperSmash", 24)
    GINGERBREAD = ("Turbo Kart Racers", "GingerBread", 25)
    HOUSING = ("Housing", "Housing", 26)
    SKYWARS = ("SkyWars", "SkyWars", 51)
    TRUE_COMBAT = ("Crazy Walls", "TrueCombat", 52)
    SPEED_UHC = ("Speed UHC", "SpeedUHC", 54)
    SKYCLASH = ("SkyClash", "SkyClash", 55)
    LEGACY = ("Classic Games", "Legacy", 56)
    PROTOTYPE = ("Prototype", "Prototype", 57)
    BEDWARS = ("Bed Wars", "Bedwars", 58)
    MURDER_MYSTERY = ("Murder Mystery", "MurderMystery", 59)
    BUILD_BATTLE = ("Build Battle", "BuildBattle", 60)
    DUELS = ("Duels", "Duels", 61)
    SKYBLOCK = ("SkyBlock", "SkyBlock", 63)
    PIT = ("Pit", "Pit", 64)


    def __init__(self, game_name, db_name, game_id):
        self.game_name = game_name
        self.db_name = db_name
        self.game_id = game_id

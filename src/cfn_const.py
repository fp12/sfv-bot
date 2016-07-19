from enum import Enum


PROBLEM_CHAR = '_'


class Character(Enum):
    Ryu = 0
    Dictator = 1
    ChunLi = 2
    Ken = 3
    Karin = 4
    Zangief = 5
    Dhalsim = 6
    Nash = 7
    Claw = 8
    Birdie = 10
    RMika = 11
    Rashid = 12
    Fang = 13
    Laura = 14
    Necalli = 15
    Cammy = 16
    Guile = 17
    Alex = 21


class WinTypes(Enum):
    NormalMove = 1
    CriticalArt = 2
    ExMove = 4
    ChipDamage = 5
    Perfect = 6
    Timeout = 7


class MatchTypes(Enum):
    Ranked = 0
    Casual = 1
    BattleLounge = 2


class Rank(Enum):
    Rookie = 0
    Bronze = 500
    SuperBronze = 1000
    UltraBronze = 1500
    Silver = 2000
    SuperSilver = 3000
    UltraSilver = 3500
    Gold = 4000
    SuperGold = 5500
    UltraGold = 6500
    Platinium = 7500
    SuperPlatinium = 10000
    UltraPlatinium = 12000
    Diamond = 14000
    SuperDiamond = 20000

    def __gt__(self, other_as_int):
        return self.value > other_as_int

    @classmethod
    def get(cls, league_points):
        previous_threshold = 0
        for points in cls.__members__.values():
            if points == league_points:
                return cls(points)
            elif points > league_points:
                return cls(previous_threshold)
            previous_threshold = points
        # get the last element
        return list(cls.__members__.values())[len(cls.__members__) - 1]

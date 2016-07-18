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

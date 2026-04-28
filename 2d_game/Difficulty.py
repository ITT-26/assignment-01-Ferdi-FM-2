from dataclasses import dataclass
from enum import IntEnum

#file for detemining difficulty and also adding shiptypes if needed  

@dataclass
class ShipType:
    pattern: list[str]
    hit_Points: int
    shoot_Chance: float

@dataclass
class Difficulty():
    enemy_pattern: list[int] #pattern of enemy strength(ship_type) from top to bottom
    enemy_speed: float
    tank_hitPoints_addition: int #additional hitpoints to the ones the tank already has
    fire_rate: float #Can shoot every x seconds (e.g. Firerate = 0.75 means able to shoot every 0.75s)

class DifficultySetting(IntEnum):
    EASY = 0
    DEFAULT = 1
    HARD = 2


BASIC_INVADER = ShipType(
     pattern= [
                "00111100",
                "01111110",
                "11111111",
                "11011011",
                "11111111",
                "00100100",
                "01000010",
                "10000001"
            ],
    hit_Points= 1,
    shoot_Chance= 0.025
)

ADVANCED_INVADER = ShipType(
    pattern=[
                "00111100",
                "11111111",
                "11111111",
                "11011011",
                "11111111",
                "00100100",
                "01000010",
                "00100100"
            ],
    hit_Points= 3,
    shoot_Chance= 0.035
)

STANDARD_TANK = ShipType(
     pattern=[
            "00011000",
            "00011000",
            "00111100",
            "11111111",
            "11111111",
            "11111111",
            "01000010",
            "00000000"
        ],
    hit_Points= 1,
    shoot_Chance= 1
)

LEVEL = {
     DifficultySetting.EASY: Difficulty(
          enemy_pattern=[0,0,0],
          enemy_speed=0.0125,
          tank_hitPoints_addition=3,
          fire_rate= 0.65
     ),
     DifficultySetting.DEFAULT:Difficulty(
          enemy_pattern=[0,1,0,0],
          enemy_speed=0.0125,
          tank_hitPoints_addition=2,
          fire_rate=0.75
     ),
     DifficultySetting.HARD:Difficulty(
          enemy_pattern=[0,1,0,1],
          enemy_speed=0.015,
          tank_hitPoints_addition=2,
          fire_rate=0.80
     ),
}

SHIPTYPES = {
     -1: STANDARD_TANK,
      0: BASIC_INVADER,
      1: ADVANCED_INVADER,  
}  
     


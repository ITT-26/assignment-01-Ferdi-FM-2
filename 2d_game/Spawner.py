from Elements import Invader, Tank, Bunker
from Difficulty import LEVEL, SHIPTYPES

class Spawner():
    def spawn_invaders(column_Count, level, batch, win, pixel_Size) -> list[Invader]:
        invaders = []
        for i in range(len(level.enemy_pattern)):
            for j in range(column_Count):
                invaders.append(
                    Invader(
                        pixel_Size*8 + j * ((win.width - pixel_Size*8*2) / column_Count), 
                        win.height - i * pixel_Size*10,
                        batch,
                        pixel_Size=pixel_Size,
                        ship_Type=  SHIPTYPES[level.enemy_pattern[i]]
                    )
                )
        invaders.reverse()
        return invaders
    
    def spawn_bunkers( batch, win, pixel_Size, tank) -> list[Bunker]:
        bunkers = []
        for i in range(5):
            bunkers.append(
                Bunker(
                    pixel_Size*8*2 + i * ((win.width - pixel_Size*16 )/ 5),
                    30 + tank.height + pixel_Size*6,
                    batch,
                    pixel_Size=pixel_Size,
                )
            )
        return bunkers

    def spawn_tank(batch, pixel_Size, level) -> Tank:
        return Tank(10, 30, batch, pixel_Size, SHIPTYPES[-1], level)
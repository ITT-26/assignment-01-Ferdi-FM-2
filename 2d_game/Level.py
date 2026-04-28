from Elements import Invader, Tank, Projectile, Bunker
from Difficulty import LEVEL, DifficultySetting, SHIPTYPES
from Spawner import Spawner
import os
import random
import pyglet

DIRECTORY_PATH = os.path.realpath(__file__).replace(os.path.basename(__file__), "")

class Level:
    def __init__(self, win, batch, invader_Batch, bunker_Batch, columns, difficulty):
        self.win = win
        self.batch = batch
        self.pixel_Size: float = win.width/160 
        self.difficulty:DifficultySetting = difficulty

        #Game-State
        self.score: int = 0 
        self.pause: bool = False
        self.won: bool = False
        self.counter: int = 0
        self.ellapsed_Time: float = 0
        self.last_Shot: float = 0

        #Game-Elements
        self.direction: int = 1 #-1 = left , 1 = right
        self.tank: Tank = Spawner.spawn_tank(batch, self.pixel_Size, LEVEL[difficulty])
        self.invaders: list[Invader] = Spawner.spawn_invaders(columns, LEVEL[difficulty], invader_Batch, win, self.pixel_Size)
        self.bunkers: list[Bunker] = Spawner.spawn_bunkers(bunker_Batch, win, self.pixel_Size, self.tank)
        self.projectiles: list[Projectile] = []
        
        #Sound-Effects
        self.shoot_Sound: pyglet.media.StreamingSource = pyglet.media.load(f"{DIRECTORY_PATH}/assets/shoot.wav", streaming=False)
        self.kill_Sound: pyglet.media.StreamingSource = pyglet.media.load(f"{DIRECTORY_PATH}/assets/invaderkilled.wav", streaming=False)
        self.death_Sound: pyglet.media.StreamingSource = pyglet.media.load(f"{DIRECTORY_PATH}/assets/explosion.wav", streaming=False)
        self.move_Sound: pyglet.media.StreamingSource = pyglet.media.load(f"{DIRECTORY_PATH}/assets/fastinvader2.wav", streaming=False)

    def update(self, dt):
        if self.pause:
            return

        self.update_invaders(dt)
        self.update_projectiles() #if one wants to speed up projectiles the update interval must be increased and projectile speed decreased, otherwise projectiles can skip over pixels and not register hits

        if len(self.invaders) == 0:
            self.won = True
            self.pause = True

    #handles invader movement, shooting and win
    def update_invaders(self,dt):
        move_down = 0 
        self.ellapsed_Time += dt
        self.counter += 1 #practically counts frames

        if(self.counter <= len(self.invaders)+1): return #    move only every len(invaders)+1 frames => invaders move faster when less are left 

        self.counter = 0
        current_Direction = self.direction
        enemy_Speed = self.win.width * LEVEL[self.difficulty].enemy_speed

        for invader in self.invaders: 
            if invader.x - enemy_Speed <= 0:
                self.direction = 1
            if invader.x + invader.width + enemy_Speed >= self.win.width:
                self.direction = -1
        
        if current_Direction != self.direction: 
            move_down = -self.win.height * 0.025 #on direction Change move down 0.25% of display so it works the same regardless of windowheight
            enemy_Speed = 0 #and dont move left/right

        for invader in self.invaders:
            invader.move(enemy_Speed*self.direction, move_down) 
            if invader.y <= 0:
                self.won = False
                self.pause = True

            shoot_Chance = random.random()
            if(shoot_Chance < invader.shoot_Chance):
                self.enemy_Shoot(invader=invader)        

    #moves the projectiles and checks for Hits
    def update_projectiles(self):
        for projectile in self.projectiles[:]: 
            projectile.move()

            #check for y edge of screen before hits to elements to reduce iterations
            if projectile.y >= self.win.height or projectile.y <= 0:
                self.projectiles.remove(projectile)
                continue

            #enemys can't shoot each other
            if not projectile.isEnemy:   
                for invader in self.invaders:
                    #since invaders are sorted by row and start with the lowest i can check if the projectile is still under the lowest row and stop checking for others if true
                    if invader.y > projectile.y:
                        break
                    if invader.hit_test(projectile):
                        self.kill_Sound.play()
                        if projectile in self.projectiles: self.projectiles.remove(projectile)
                        if invader.hit_Points == 0:
                            if invader in self.invaders: self.invaders.remove(invader)
                            self.score += 100 if invader.ship_Type == SHIPTYPES[0] else 300
                        break
            else:
                if self.tank.hit_test(projectile):
                    if projectile in self.projectiles: self.projectiles.remove(projectile)
                    if self.tank.hit_Points <= 0:
                        self.death_Sound.play()
                        self.won = False
                        self.pause = True
                    continue
            
            for bunker in self.bunkers:
                #checking if first bunker is already out of y-Range of the projectile and skip if true
                if not projectile.isEnemy and bunker.y + bunker.height < projectile.y: 
                    break
                if bunker.hit_test(projectile):
                    self.projectiles.remove(projectile)
                    continue

    #tank-shots
    def shoot(self):
        if self.last_Shot != 0 and self.ellapsed_Time - self.last_Shot < LEVEL[self.difficulty].fire_rate: #self.last_Shot != 0 so first shot isn't time dependend
            return

        self.shoot_Sound.play()
        self.projectiles.append(
            Projectile(
                self.tank.x + len(self.tank.tankPattern)*self.pixel_Size/2 - self.pixel_Size, 
                self.tank.y + len(self.tank.tankPattern[0])*self.pixel_Size, 
                self.batch, 
                self.pixel_Size,
                (255,255,255),
                False
            )
        )
        self.last_Shot = self.ellapsed_Time

    #invader shot
    def enemy_Shoot(self, invader):
        self.shoot_Sound.play()
        self.projectiles.append(
            Projectile(
                invader.x + invader.width/2 + self.pixel_Size, 
                invader.y, 
                self.batch, 
                self.pixel_Size,
                (176, 62, 149),
                True
            )
        )
    
    def clear(self):
        self.invaders.clear()
        self.bunkers.clear()
        self.projectiles.clear()
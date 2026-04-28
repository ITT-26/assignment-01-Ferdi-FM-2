from pyglet import shapes
from Difficulty import ShipType, Difficulty

class Projectile():
    def __init__(self,x: int, y:int, batch, pixel_Size, color:tuple, isEnemy:bool):
        self.x = x
        self.y = y
        self.width = pixel_Size
        self.height = pixel_Size*3
        self.pixel_Size = pixel_Size
        self.shape = shapes.Rectangle(x, y, self.width, self.height, color=color, batch=batch)
        self.isEnemy = isEnemy

    def move(self):
        speed = self.pixel_Size #speed is dependend on the interval of updates and pixelsize for hittest to work properly, otherwise projectiles can skip over pixels and not register hits
        if self.isEnemy: 
            speed = -speed
        
        self.y += speed
        self.shape.position = (self.x, self.y) #pyglet documentation recommends position, instead of changing x/y
    
    #Checks a Target agains itself for collision
    def hit_test(self, target) -> bool:
        proj_Right = self.x + self.width
        proj_Left = self.x
        proj_Top = self.y + self.height
        proj_Bottom = self.y

        hitWidth = target.x <= proj_Right <= target.x + target.width or target.x <= proj_Left <= target.x + target.width
        hitHeight = target.y <= proj_Top <= target.y + target.height or target.y <= proj_Bottom <= target.y + target.height
       
        if hitWidth and hitHeight: return True
        return False

class Invader():
    def __init__(self, x, y, batch, pixel_Size, ship_Type:ShipType):
        self.x = x
        self.y = y
        self.batch = batch
        self.width = pixel_Size*len(ship_Type.pattern[0]) #pixel_Size*nmbr of Pixels, would need to be variable dependend on max in pattern of ship_type if larger ships become an option
        self.height = pixel_Size*len(ship_Type.pattern)
        self.pixel_size = pixel_Size

        self.ship_Type = ship_Type
        self.hit_Points = ship_Type.hit_Points
        self.invader_pattern = ship_Type.pattern
        self.shoot_Chance = ship_Type.shoot_Chance

        self.pixels = []
        self.build()

    #idea with matrix/loop from ChatGPT (see Game.py -> Citations #1)
    def build(self):
        invader_height = len(self.invader_pattern)
        for rowNr, row in enumerate(self.invader_pattern):
            for cellNr, cell in enumerate(row):
                if cell == "1":
                    rect = shapes.Rectangle(
                        self.x + cellNr * self.pixel_size,
                        self.y + (invader_height - rowNr) * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size,
                        color=(255, 255, 255),
                        batch=self.batch
                    )
                    self.pixels.append(rect)

    #Checks self against a Projectile for collision
    def hit_test(self, projectile:Projectile) -> bool:
        if projectile.isEnemy:
            return False
        if (projectile.hit_test(self)):
            self.hit_Points -= 1
            self.pixels = self.pixels[0::2]   #remove every second pixel to simulate damage
            return True
        return False

    def move(self, x, y=0):
        self.x += x
        self.y += y
        for p in self.pixels:
            pos = p.position
            p.position = (pos[0] + x, pos[1] + y) 

class Tank():
    def __init__(self, x:int, y:int, batch, pixel_Size, ship_type:ShipType, difficulty:Difficulty):
        self.x = x
        self.y = y
        self.batch = batch
        self.width = pixel_Size*len(ship_type.pattern[0]) #pixel_Size*nmbr of Pixels
        self.height = pixel_Size*len(ship_type.pattern)
        self.pixel_size = pixel_Size

        self.tankPattern: list[str] = ship_type.pattern
        self.hit_Points:int = ship_type.hit_Points + difficulty.tank_hitPoints_addition

        self.tankPixels = []
        self.build()

    def build(self):
        tank_height = len(self.tankPattern)
        for rowNr, row in enumerate(self.tankPattern):
            for colNr, pixel in enumerate(row):
                if pixel == "1":
                    rect = shapes.Rectangle(
                        self.x + colNr * self.pixel_size,
                        self.y + (tank_height - rowNr) * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size,
                        color=(0, 255, 0),
                        batch=self.batch
                    )
                    self.tankPixels.append(rect)

    def move(self, move_Speed, winWidth): 
        if self.x + move_Speed < 0 or self.x + self.width + move_Speed > winWidth: return
        self.x += move_Speed
        for p in self.tankPixels:
            pos = p.position
            p.position = (pos[0] + move_Speed, pos[1])

    #Checks self against a Projectile for collision
    def hit_test(self, projectile:Projectile) -> bool:
        for pixel in self.tankPixels:
            if projectile.hit_test(pixel):
                self.hit_Points -= 1
                self.tankPixels.remove(pixel)
                return True      
        return False


class Bunker():
    def __init__(self, x:int, y:int, batch, pixel_Size):
        self.x = x
        self.y = y
        self.batch = batch
        self.width = pixel_Size*8 #pixel_Size*nmbr of Pixels
        self.height = pixel_Size*8

        self.pixel_size = pixel_Size
        self.bunker_pattern = [
                "0011111100",
                "0111111110",
                "1111111111",
                "1111111111",
                "1111111111",
                "1111111111",
                "1110000111",
                "1100000011"
            ]
        self.pixels = []
        self.build()

    def build(self):
        bunker_height = len(self.bunker_pattern)
        for rowNr, row in enumerate(self.bunker_pattern):
            for colNr, cell in enumerate(row):
                if cell == "1":
                    rect = shapes.Rectangle(
                        self.x + colNr * self.pixel_size,
                        self.y + (bunker_height - rowNr) * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size,
                        color=(0, 255, 0),
                        batch=self.batch
                    )
                    self.pixels.append(rect)

    #Checks self against a Projectile for collision
    def hit_test(self, projectile:Projectile) -> bool:
        for i, pixel in enumerate(self.pixels):
                if (projectile.hit_test(pixel)):
                    self.pixels.remove(pixel)
                    return True        
        return False
    


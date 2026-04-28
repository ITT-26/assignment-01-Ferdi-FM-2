import pyglet
import os
from pyglet import window
from pyglet.window import key
from DIPPID import SensorUDP
from Level import Level
from Difficulty import DifficultySetting, LEVEL

# Citations:
# 1: Asked ChatGPT how a space-invader sprite can be generated in pyglet. Prompt: "pyglet can you create a spaceinvader ship?"
# 2: Asked for documentation in general (e.g. how to create dataclass/Enum(wasn't useful since ended up looking in documentation anyway), if python has an equivalent to some c# syntax like varX = bool ? var1 : var 2 or $"score: {score}")
# used/looked up code from the examples in the presence-lesson (e.g. demo_device) and documentation https://pyglet.readthedocs.io/en/latest (e.g. batch, keyStateHandler)
# SoundEffects from https://classicgaming.cc/classics/space-invaders/sounds

#Notes:
# Using "real" sprites would propably be more performant, but with own pixel array i could simulate damage
PORT = 5700
sensor = SensorUDP(PORT)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = int(WINDOW_WIDTH/16*9) #WINDOW_HEIGHT #for quadratic window
DIFFICULTY = DifficultySetting.EASY #Starting difficulty, set to diffrent to see other level
win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

class Game:
    def __init__(self):
        self.win = win
        self.batch = pyglet.graphics.Batch() #batch for tank and projectiles
        self.invader_Batch = pyglet.graphics.Batch() #batch for invaders
        self.bunker_Batch = pyglet.graphics.Batch() #batch for bunkers

        self.keys = key.KeyStateHandler()
        self.win.push_handlers(self.keys)
        
        self.total_Score = 0       
        self.game_Startet:bool = False
        self.level:Level = Level(self.win, self.batch, self.invader_Batch, self.bunker_Batch, 8, DifficultySetting.EASY) #to display gameElements before start
        self.difficulty:DifficultySetting = DIFFICULTY #the Start difficulty

        #label for Level, Score, Hitpoints
        self.scor_label = pyglet.text.Label(
            "Score: 0",
            x=10,
            y=10,
            color=(255, 255, 255, 255),
            font_size=WINDOW_HEIGHT/30
        )

        #Middle Label for GameStart/GameEnd
        self.end_Label = pyglet.text.Label(
            "Press\n\"S\" or \"Button_2\"\nto start", #\n\nYou can control the tank with the arrow keys or\nby tilting the phone left/right and shoot with \"Button_1\"
            x=self.win.width // 2,
            y=self.win.height // 2,
            anchor_x="center",
            anchor_y="center",
            font_size=30,
            multiline=True,
            width= win.width,
            align="center"
        )
        
        self.win.push_handlers(self.on_draw)
        pyglet.clock.schedule_interval(self.update, 1/60)
        #pyglet.clock.schedule_interval(self.update_Projectile, 1/120) #If one wants to increase projectile speed updates must be faster and pixelmovementSpeed slower to not jump over pixels for hittest of bunkers

    #Starts (or resets) the Game
    def startGame(self, columns, difficulty):
        self.level.clear()     
        self.level = Level(self.win, self.batch, self.invader_Batch, self.bunker_Batch, columns, difficulty)
        self.game_Startet = True

    #drawing
    def on_draw(self):
        self.win.clear()
        self.batch.draw()
        self.invader_Batch.draw()
        self.bunker_Batch.draw()
        self.scor_label.draw()
        self.end_Label.draw()

    #whole update-Logic running at "60Fps"/ every 1/60 seconds
    def update(self, dt):
        if not self.game_Startet or self.level.pause and self.end_Label.text != "":  #self.endlabel.text is needed so the endGame-Message gets displayed properly
            return
        self.end_Label.text = "" 
        
        #Active Game
        self.level.update(dt)
        self.update_input(dt)
        self.scor_label.text = f"Level: {self.difficulty + 1} | Score: { self.total_Score + self.level.score} | HitPoints: {self.level.tank.hit_Points}"

        #End Game
        if self.level.pause:
            if self.level.won:
                self.end_Label.text = "You Won!\npress \"S\" or \"Button_2\"\n to start a more difficult level" if self.difficulty < (len(DifficultySetting)-1) else "Congratiulations, You Won!\nPress \"S\" to restart from the first level"
                self.difficulty = (self.difficulty+1) % len(DifficultySetting) #stay in range of the DifficultySettings IntEnum 
                self.total_Score = self.level.score
            else:
                self.end_Label.text = "You Lost!\npress \"S\" or \"Button_2\"\nto restart"
            self.game_Startet = False

    #keyboard input
    def update_input(self, dt):
        if self.level.pause or not self.game_Startet:
            return
        if self.keys[key.LEFT]:
            self.level.tank.move(-self.win.width/150, win.width)
        if self.keys[key.RIGHT]:
            self.level.tank.move(self.win.width/150, win.width)
        if self.keys[key.UP]:
            self.level.shoot()
        if sensor.get_value("button_1") == 1: #allows for holding down button_1 in DIPPID to shoot
            self.level.shoot()
    
    #DIPPID input (when holding smartphone upright, tilting left and right moves the tank, button 1 shoots, button 2 starts the game)
    #Movement is constant, so more tilt doesnt translate to faster movement
    def movement_dippid(self,data):
        if self.level.pause or not self.game_Startet:
            return
        moveX = data["x"]
        if(abs(moveX) < 0.14): return #DIPPID always shows x between -0.1 to 0.1 when smartphone is laying still
        self.level.tank.move((self.win.width/200) * (moveX*-1.4), win.width) #acceleration multiplied by -1.4 for less needed tilt and reverse direction
        #alternative constant Movement
        #if moveX > 0:
        #    #left
        #    self.level.tank.move(-self.win.width/200, win.width) #better to control with slower movement_speed (compared to keyboard)
        #else:
        #    #right
        #    self.level.tank.move(self.win.width/200, win.width)


game = Game()

@win.event
def on_key_press(symbol, modifiers):
        if symbol == key.Q:
            os._exit(0)
        if symbol == key.S:
            if not game.game_Startet:
                game.startGame(10, game.difficulty)

##def button_1_dippid(data):
##    if game.level.pause or not game.game_Startet:
##        return
##    if(data == 1): game.level.shoot()

def button_2_dippid(data):
    if not game.game_Startet and data == 1:
        game.startGame(8, game.difficulty) #less targets since controls with DIPPID are alot harder      

sensor.register_callback('accelerometer', game.movement_dippid) #could also be put in the update function to use polling
sensor.register_callback('button_2', button_2_dippid)
#sensor.register_callback('button_1', button_1_dippid) #if shoot shouldn't allow for holding down button_1


pyglet.app.run()


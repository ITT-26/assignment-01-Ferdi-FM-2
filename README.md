[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Etw90P0Z)
# DIPPID and Pyglet

# Dippid Sender
Simulates the acceleration and the button_1 push/press of a smartPhone using DIPPID
It randomly switches between:
    - "idle"    : Simulates Smartphone laying around, practically just noise
    - "looking" : Holding the Smartphone in hand and looking at it
    - "shake"   : Shaking the phone with light to medium intensity in random directions
    - "movement": Moving the smartphone or e.g. having it in the pocket
At random intervals "button_1" gets pressed

# 2d Game

## Space Invaders

A simple Version of Space Invaders

- You can start the Game by pressing "S" on the keyboard or with DIPPID "button_2"
- The Tank can be moved with the arrow-keys or with DIPPID by tilting the phone left/right when holding it
- You can shoot with the arrow_up key or with DIPPID "button_1"

Features:
- The Invaders get faster the more you destroy (like the original game, but of cause not for the same reason)
- The Invaders shoot back
- There are 3 "Levels" increasing in difficulty
    - First Level is 3 rows of Basic Invaders with 1 HitPoints and Tank has 4 HitPoints
    - Second Level is 3 rows of Basic Invaders and 1 rows of advanced invaders with 3 HitPoints and increased fire-Rate, 
      also Tank only has 3 HitPoints
    - Third Level is 2 rows of Basic Invaders and 2 rows of advanced invaders with 3 HitPoints and increased fire-Rate,
      fire-Rate is a little slower and enemys move faster
- Once Lost or Won the current Level can be restarted
- Original Shoot, Destroy and gameOver sounds were used from https://classicgaming.cc/classics/space-invaders/sounds 
- Small Details:
    - The Advanced Invaders take visible damage
    - The Tank takes visible damage
    - Should work with any window width/height (currently stays at 16:9 with width as Constant)

Extras:
- It's written so new Levels, Invaders or Tanks could be added with different attributes
- Code-Citation in 2d_game\Game.py

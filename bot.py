from World import World
from Monster import Monster
from Player import Player
from time import sleep

world = World()
player = Player()
while True:
    shot = False
    monsters = world.get_monsters()
    for monster in monsters:
       monster = Monster(monster)
       if monster.shootable():
           player.shoot(1)
           sleep(0.25)
           shot = True
           break

    if not shot:
        sleep(0.25)
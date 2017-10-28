from World import World
from Monster import Monster
from Player import Player

world = World()
player = Player()
while True:
    monsters = world.get_monsters()
    for monster in monsters:
        monster = Monster(monster)
        if monster.shootable():
            player.shoot()
            break
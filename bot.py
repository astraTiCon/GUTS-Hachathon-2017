from World import World
from Monster import Monster
from Player import Player
from time import sleep
from random import choice
from itertools import chain
import math

def self_remove(players):
    p_id = player.get_id()
    for p in players:
        if p['id'] != p_id:
            yield p


def try_dooring(player, world, door_timer):
    doors = world.get_doors()
    for door in doors:
        doorx = (door['line']['v1']['x'] + door['line']['v2']['x'])/2
        doory = (door['line']['v1']['y'] + door['line']['v2']['y'])/2
        if (door_timer == 0 and door['distance'] < 150 and
            player.looking_at({ 'x':doorx,'y':doory } ,0.3)):
            door_timer = door_open_threshold
            player.use()
            sleep(.2)
            player.forward(40)
    return door_timer


def shoot(player, monsters, door_timer):
    shot = False
    door_timer = max(0,door_timer - 1)
    for m in monsters:
        m = Monster(m)
        if player.looking_at(m.monster['position']):
            los = m.shootable(str(player.get_id()))
            if(los < 0):
                player = Player()
                continue
            if not los:
                continue
            player.shoot(1)
            choice([player.rstrafe, player.lstrafe])(38)
            sleep(.1)
            shot = True
            break
    return shot, door_timer


def get_all_monsters(world, dist=2000):
    monsters = chain(world.get_monsters(dist), self_remove(world.get_players()))
    return monsters


def get_targets(monsters):
    targets = []
    for m in monsters:
        m = Monster(m)
        if not m.shootable(str(player.get_id())):
            continue
        targets.append(m)
    return targets


def choose_target(player, targets):
    best_target = targets[0]
    danger_dist = targets[0].monster['distance']
    best_angle_change = player.get_angle_change(targets[0].monster['position'])

    for tar in targets:
        angle_change = player.get_angle_change(tar.monster['position'])
        if ((angle_change < best_angle_change and danger_dist > 200) or
            (tar.monster['distance'] < 200)):
            best_angle_change = angle_change
            danger_dist = tar.monster['distance']
            best_target = tar
    return best_target, danger_dist


def aim_n_shoot(player, target):
    angle = player.get_angle(target.monster['position'])
    player.right(math.degrees(angle))
    player.shoot(1)


world = World()
player = Player()
door_open_threshold = 10
door_timer = 0

while True:
    monsters = get_all_monsters(world)
    shooot, door_timer = shoot(player, monsters, door_timer)
    if shooot:
        continue

    targets = get_targets(monsters)
    if len(targets) > 0:
        best_target, danger_dist = choose_target(player, targets)
        aim_n_shoot(player, best_target)
    door_timer = try_dooring(player, world, door_timer)

#!/usr/bin/env python3
from World import World
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
        doorx = (door['line']['v1']['x'] + door['line']['v2']['x']) / 2
        doory = (door['line']['v1']['y'] + door['line']['v2']['y']) / 2
        if (door_timer == 0 and door['distance'] < 150 and
            player.looking_at({ 'x':doorx,'y':doory } ,0.3)):
            door_timer = door_open_threshold
            player.use()
            sleep(.2)
            player.forward(40)
    return door_timer


def shoot(player, monsters, door_timer, move_flag):
    shot = False
    door_timer = max(0,door_timer - 1)
    for m in monsters:
        if player.looking_at(m['position']):
            los = player.can_shoot(m['id'])
            if(los < 0):
                player = Player()
                continue
            if not los:
                continue
            player.shoot(1)
            sleep(0.05)
            player.shoot(1)
            if m['distance'] > 500:
                [player.rstrafe, player.lstrafe][move_flag](38)
                move_flag = not move_flag
            sleep(.1)
            shot = True
            break
    return shot, door_timer, move_flag


def get_all_monsters(world, dist=2000):
    monsters = chain(world.get_monsters(dist), self_remove(world.get_players()))
    return monsters


def choose_target(player, targets):
    best_target = targets[0]
    danger_dist = targets[0]['distance']
    best_angle_change = player.get_angle_change(targets[0]['position'])

    for tar in targets:
        angle_change = player.get_angle_change(tar['position'])
        if ((angle_change < best_angle_change and danger_dist > 200) or
            (tar['distance'] < 200)):
            best_angle_change = angle_change
            danger_dist = tar['distance']
            best_target = tar
    return best_target, danger_dist


def aim_n_shoot(player, target):
    angle = player.get_angle(target['position'])
    player.right(math.degrees(angle))
    sleep(0.1)
    player.shoot(1)


def distance(a, b):
    return math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2)


def random_movement(n=4):
    for _ in range(n):
        choice([player.forward, player.backward, player.lstrafe, player.rstrafe])(20)


def move_to(tar_type, dist=200):
    targets = list(world._get_pickups(tar_type, dist))
    if not targets:
        return

    prev_pos = player.get_position()
    target = min(targets, key=lambda x: x['distance'])
    angle = player.get_angle(target['position'])
    player.right(math.degrees(angle))
    player.forward(40)
    new_pos = player.get_position()
    sleep(.2)
    if distance(prev_pos, new_pos) < 50:
        random_movement()
        return False
    return True


world = World()
player = Player()
door_open_threshold = 10
door_timer = 0
move_flag = False


while True:
    monsters = list(filter(lambda x: player.can_shoot(x['id']),
                           get_all_monsters(world)))
    shooot, door_timer, move_flag = shoot(player, monsters, door_timer, move_flag)
    if shooot:
        continue

    if len(monsters) <= 0:
        while move_to('armor'):
            pass

        while move_to('weapon', 500):
            pass

        if player.get_health() < 38:
            while move_to('health'):
                pass

    player.switch_weapon()
    if len(monsters) > 0:
        best_target, danger_dist = choose_target(player, monsters)
        aim_n_shoot(player, best_target)
    door_timer = try_dooring(player, world, door_timer)

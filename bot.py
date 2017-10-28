from World import World
from Monster import Monster
from Player import Player
from time import sleep
import math

def self_remove(players):
    p_id = player.get_id()
    for p in players:
        print(p)
        if p['id'] != p_id:
            yield p

world = World()
player = Player()
door_open_threshold = 10
door_timer = 0

while True:
    shot = False
    door_timer = max(0,door_timer - 1)
    monsters = world.get_monsters()
    monsters += self_remove(world.get_players())
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
            sleep(0.25)
            shot = True
            break

    if shot:
        continue

    targets = []

    for m in monsters:
        m = Monster(m)
        if not m.shootable(str(player.get_id())):
            continue
        targets.append(m)

    if len(targets) > 0:
        best_target = targets[0]
        danger_dist = targets[0].monster['distance']
        best_angle_change = player.get_angle_change(targets[0].monster['position'])

        for tar in targets:
            angle_change = player.get_angle_change(tar.monster['position'])
            if (angle_change < best_angle_change and danger_dist > 200) or (tar.monster['distance'] < 200):
                best_angle_change = angle_change
                danger_dist = tar.monster['distance']
                best_target = tar

        target_id = best_target.monster['id']

        while tar.shootable(str(player.get_id())) and not player.looking_at(tar.monster['position']):
            monsters = world.get_monsters(danger_dist * 1.2 + 100)
            monsters += self_remove(world.get_players(danger_dist * 1.2 + 100))
            tar = None
            for m in monsters:
                if m['id'] == target_id:
                    tar = Monster(m)
                    break

            if tar is None:
                break

            angle = player.get_angle(tar.monster['position'])
            p_angle = math.radians(player.get_position()['angle'])
            player.right(math.degrees(angle))
            player.shoot(1)
            

    doors = world.get_doors()
    for door in doors:
        doorx = (door['line']['v1']['x'] + door['line']['v2']['x'])/2
        doory = (door['line']['v1']['y'] + door['line']['v2']['y'])/2
        if door_timer == 0 and door['distance'] < 150 and player.looking_at({ 'x':doorx,'y':doory } ,0.3):
            door_timer = door_open_threshold
            player.use()
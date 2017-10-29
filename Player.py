#!/usr/bin/env python3
import json
import requests
import math

class Player:
    def __init__(self, url='http://0.0.0.0:6001'):
        self.url = url

    def _turn(self, turn_type, angle):
        data = {
            'type': turn_type,
            'target_angle': angle
        }
        requests.post(self.url + '/api/player/turn', json=data)

    def _self_info(self, info_type):
        r = requests.get(self.url + '/api/player')
        return json.loads(r.text)[info_type]

    def _action(self, action_type, amount=1):
        data = {
            'type': action_type,
            'amount': amount
        }
        requests.post(self.url + '/api/player/actions', json=data)

    def left(self, angle):
        self._turn('left', angle)

    def right(self, angle):
        self._turn('right', angle)

    def turn_dir(self, direction, amount=10):
        self._action("turn-" + direction, amount)

    def forward(self, amount=20):
        self._action('forward', amount)

    def backward(self, amount=20):
        self._action('backward', amount)

    def lstrafe(self, amount=20):
        self._action('strafe-left', amount)

    def rstrafe(self, amount=20):
        self._action('strafe-right', amount)

    def shoot(self, amount):
        self._action('shoot', amount)

    def get_position(self):
        position = self._self_info('position')
        position['angle'] = self._self_info('angle')
        return position

    def get_health(self):
        return self._self_info('health')

    def get_keys(self):
        return self._self_info('keyCards')

    def get_id(self):
        return self._self_info('id')

    def use(self):
        self._action('use')

    def switch_weapon(self):
        self._action('switch-weapon')

    def get_angle_change(self,obj):
        angle = self.get_angle(obj)
        d_angle = angle - math.radians(self.get_position()['angle'])
        d_angle = abs(d_angle)
        d_angle = min(d_angle,2 * math.pi - d_angle)
        return d_angle

    def get_angle(self,obj):
        player_coord = self.get_position()
        dx = obj['x'] - player_coord['x']
        dy = obj['y'] - player_coord['y']
        dx = dx if dx != 0 else 0.0001
        angle = math.atan(dy / dx)

        if (not max(0, dy)) and (not max(0, dx)):
            angle += math.pi
        elif (not max(0, dx)) and max(0, dy):
            angle += math.pi

        if angle < 0:
            angle += 2 * math.pi
        return angle

    def looking_at(self, obj, error=0.05):
        dx = obj['x'] - self.get_position()['x']
        dy = obj['y'] - self.get_position()['y']
        d_angle = self.get_angle_change(obj)
        distance = math.sqrt(dx**2 + dy**2)
        return abs(d_angle) < error * (1 + 50 / distance ** 0.65)
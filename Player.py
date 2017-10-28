#!/usr/bin/env python3
import json
import requests


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

    def forward(self, amount=20):
        self._action('forward', amount)

    def backward(self, amount=20):
        self._action('backward', amount)

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

    def use(self):
        self._action('use')

    def switch_weapon(self):
        self._action('switch-weapon')

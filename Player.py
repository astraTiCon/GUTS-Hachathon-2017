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

    def _self_info(type):
        r = requests.get(self.url + '/api/player')
        return json.loads(r.text)[type]

    def _action(self, action_type, amount):
        data = {
            'type': action_type,
            'amount': amount
        }
        requests.post(self.url + '/api/player/actions', json=data)


    def left(self, angle):
        self._turn('left', angle)


    def right(self, angle):
        self._turn('right', angle)


    def forward(self, amount=100):
        self._action('forward', amount)


    def shoot(self, amount=1):
        self._action('shoot', amount)


    def get_position(self):
        position = self._self_info('position')
        position[angle] = self._self_info('angle')
        return position


    def get_health(self):
        return self._self_info('health')


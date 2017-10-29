import json
import requests


class World:
	def __init__(self, url='http://0.0.0.0:6001'):
		self.url = url

	def get_monsters(self, distance=2000):
		for obj in self._get_pickups('', 2000):
			name = obj['type']
			if name.isupper() and obj['health'] > 0:
				yield obj

	def _get_pickups(self, obj_type, distance=2000):
		data = {'distance': distance}
		r = requests.get(self.url + "/api/world/objects", params=data)
		if r.status_code != 200:
			print("world/objects request error: " + r.text)
			return {}

		for obj in json.loads(r.text):
			if obj_type in obj['type']:
				yield obj

	def get_doors(self):
		r = requests.get(self.url + "/api/world/doors")
		if r.status_code != 200:
			print("world/doors request error: " + r.text)
			return {}
		return json.loads(r.text)

	def get_health(self, distance=2000):
		return self._get_pickups('health', 2000)

	def get_armor(self, distance=2000):
		return self._get_pickups('armor', 2000)

	def get_ammo(self, distance=2000):
		return self._get_pickups('ammo', 2000)

	def get_players(self):
		r = requests.get(self.url + '/api/players')
		return json.loads(r.text)
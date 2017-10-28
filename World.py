import json
import requests

class World:
	def __init__(self,url="http://0.0.0.0:6001"):
		self.url = url

	def get_world(self,distance = 2000):

		r = requests.get(self.url + "/api/world/objects", params = {'distance': distance})
		if r.status_code != 200:
			print("world/objects request error: " + r.text)
			return {}

		world_objects = json.loads(r.text)

		return world_objects

	def get_monsters(self,distance = 2000):

		world_objects = self.get_world(distance)
		monsters = []
		for obj in world_objects:
			name = obj['type']
			if name.isupper():
				monsters.append(obj)

		return monsters

	def get_doors(self):
		r = requests.get(self.url + "/api/world/doors")

		if r.status_code != 200:
			print("world/doors request error: " + r.text)
			return {}

		doors = json.loads(r.text)
		return doors

	def get_pickups(self,distance=2000):
		world_objects = get_world(distance)
		pickups = []

		for obj in world_objects:
			name = obj['type']
			if 'armor' in name or 'health' in name:
				pickups.append(obj)

		return pickups

	def get_players(self):
		r = requests.get(self.url + '/api/players')
		return json.loads(r.text)
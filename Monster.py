import json
import requests

class Monster:
    def __init__(self,monster,url="http://0.0.0.0:6001"):
        self.url = url
        self.monster = monster

    def is_alive(self):
        return self.monster['health'] > 0

    def in_los(self):
        r = requests.get(self.url + "/api/world/los/0/" + str(self.monster['id']))
        r = json.loads(r.text)
        return r['los']

    def shootable(self):
        return self.is_alive() and self.in_los()


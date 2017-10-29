import json
import requests

class Monster:
    def __init__(self, monster, url="http://0.0.0.0:6001"):
        self.url = url
        self.monster = monster

    def shootable(self,id1):
        r = requests.get(self.url + "/api/world/los/"+ id1  +"/" + str(self.monster['id']))
        r = json.loads(r.text)
        try:
            return r['los']
        except KeyError:
            print("bad id")
            return -1
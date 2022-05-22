import requests


class SuperHero():

    def _get_powerstats(self, name):
        url = f'https://superheroapi.com/api/2619421814940190/search/{name}'
        resp = requests.get(url)
        return resp.json()

    def __init__(self, name):
        self.name = name
        self.powerstats = {}
        response = self._get_powerstats(name)
        if response["response"] == 'success':
            self.powerstats = response["results"][0]["powerstats"]
        else:
            print(response["error"])


def main():
    dict_intelligence = {}
    hulk = SuperHero('Hulk')
    print('Hulk', hulk.powerstats)
    dict_intelligence['hulk'] = int(hulk.powerstats['intelligence'])

    captain_america = SuperHero('Captain America')
    print('Captain America', captain_america.powerstats)
    dict_intelligence['captain_america'] = int(captain_america.powerstats['intelligence'])

    thanos = SuperHero('Thanos')
    print('Thanos', thanos.powerstats)
    dict_intelligence['thanos'] = int(thanos.powerstats['intelligence'])

    print(dict_intelligence)
    sorted_keys = sorted(dict_intelligence, key=dict_intelligence.get)
    print(f'Самый умный супергерой: {sorted_keys[-1]} - {dict_intelligence[sorted_keys[-1]]}')


main()

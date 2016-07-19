def intersect(a, b):
    return list(set(a) & set(b))


def list_in(a, b):
    return len(intersect(a, b)) == len(a)


class Player():
    def __init__(self, json_d):
        self.name = json_d['fightersid']
        self.cfn_id = int(json_d['publicid'])
        self.region = json_d['region']
        self.platform = json_d['accountsource']

    @classmethod
    def create(cls, json_d):
        if json_d and list_in(['fightersid', 'publicid', 'region', 'accountsource'], json_d):
            return Player(json_d)
        else:
            return None


class PlayerSearch():
    def __init__(self, json_d):
        self.found_players = []
        for result in json_d:
            new_player = Player.create(result)
            if new_player:
                self.found_players.append(new_player)

    @classmethod
    def create(cls, json_d):
        if json_d and 'response' in json_d and 'searchresult' in json_d['response'][0]:
            return PlayerSearch(json_d['response'][0]['searchresult'])
        else:
            return None

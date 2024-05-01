import json
DB_FILE_NAME = "database.json"
PLAYERS = "players"


class Player:
    """A chess player"""
    def __init__(self, first_name, last_name, birth_date, national_chess_id):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id

    @staticmethod
    def load_all():
        """Return a list of players stored in DB"""
        with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            players = data[PLAYERS]
            list_players = []
            for p in players:
                player = Player(p["first_name"], p["last_name"], p["birth_date"], p["national_chess_id"])
                player.id = p["id"]
                list_players.append(player)
            return list_players

    @staticmethod
    def save(player):
        """Save an object in a Json database with a unique ID"""
        with open(DB_FILE_NAME, 'r+') as file:
            data = json.load(file)
            # We take the last gived ID and add 1 to it to make sure no object
            # from the same class are equal by id
            if len(data[PLAYERS]) == 0:
                player.id = 0
            else:
                player.id = data[PLAYERS][-1]["id"] + 1
            data[PLAYERS].append(player.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)
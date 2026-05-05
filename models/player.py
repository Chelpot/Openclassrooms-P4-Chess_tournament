import datetime as dt
import json
from operator import attrgetter
DB_FILE_NAME = "database.json"
PLAYERS = "players"


class Player:
    """A chess player"""
    def __init__(self, first_name, last_name, birth_date, national_chess_id):
        self._first_name = first_name
        self._last_name = last_name
        self._birth_date = birth_date
        self._national_chess_id = national_chess_id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, name):
        if len(name) < 2:
            raise Exception("Le prénom doit contenir au minimum 2 lettres.")
        self._first_name = name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, name):
        if len(name) < 2:
            raise Exception("Le nom doit contenir au minimum 2 lettres.")
        self._last_name = name

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, date):
        if not self.is_date_correct(date):
            raise Exception("Le date de naissance n'est pas correcte.")
        self._birth_date = date

    @property
    def national_chess_id(self):
        return self._national_chess_id

    @national_chess_id.setter
    def national_chess_id(self, id):
        if self.is_already_registered(id):
            raise Exception("Un utilisateur inscrit dans la base de donnée détient déja cet identifiant.")
        if not self.is_national_chess_id_correct(id):
            raise Exception("Le numéro national d'échecs est incorrect.")
        self._national_chess_id = id

    @staticmethod
    def load_all():
        """Return a list of players stored in DB"""
        with open(DB_FILE_NAME, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            players = data[PLAYERS]
            list_players = []
            for p in players:
                player = Player(p["first_name"], p["last_name"], p["birth_date"], p["national_chess_id"])
                player.id = p["id"]
                list_players.append(player)
            list_players = sorted(list_players, key=attrgetter("last_name", "first_name"))
            return list_players

    @staticmethod
    def load_with_id(id):
        """Return a tournament with corresponding id"""
        player = Player.load_all()
        for p in player:
            if p.id == id:
                return p
        print("Aucun joueur avec cet identifiant n'existe.")
        return None

    @staticmethod
    def is_player_existing(id):
        players = Player.load_all()
        return any(p.id == id for p in players)

    @staticmethod
    def save_new(player):
        """Save an player in the Json database with an unique ID"""
        with open(DB_FILE_NAME, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            # We take the last gived ID and add 1 to it
            if len(data[PLAYERS]) == 0:
                player.id = 0
            else:
                player.id = data[PLAYERS][-1]["id"] + 1

            # dict_player_protected = player.__dict__
            # dict_player = {}
            # for key in dict_player_protected:
            #     if key == "id":
            #         dict_player[key] = dict_player_protected[key]
            #     else:
            #         dict_player[key[1:]] = dict_player_protected[key]
            data[PLAYERS].append(player.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)

    def is_date_correct(self, date: str):
        """Check if date follow the layout DD/MM/YYYY and is a valid date. Return True if correct"""
        is_correct = True
        if len(date) == 10 and date.count("/") == 2:
            splited_date = date.split("/")
            day_date = int(splited_date[0])
            month_date = int(splited_date[1])
            year_date = int(splited_date[2])
            # Check if the date is a correct one
            try:
                dt.datetime(year_date, month_date, day_date)
            except ValueError:
                is_correct = False
        else:
            is_correct = False
        return is_correct

    def is_national_chess_id_correct(self, id: str):
        """Check if id follow the layout AB12345"""
        return id[:2].isalpha() and id[5:].isnumeric() and len(id) == 7

    def is_already_registered(self, chess_id):
        """Check if chess id is already registered"""
        for p in self.load_all():
            if p["national_chess_id"] == chess_id:
                return True
        return False

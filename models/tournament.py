import json
from operator import attrgetter

from models.player import Player
from models.round import Round
DB_FILE_NAME = "database.json"
TOURNAMENTS = "tournaments"


class Tournament:
    def __init__(self, name, place, starting_date, ending_date, number_of_rounds=4, description=""):
        self.name = name
        self.place = place
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round = 0
        self.list_rounds = []
        self.list_registered_players = []

    @staticmethod
    def load_all():
        """Return a list of tournaments stored in DB"""
        with open(DB_FILE_NAME, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            tournaments = data[TOURNAMENTS]
            list_tournaments = []
            for t in tournaments:
                tournament = Tournament(
                                    t['name'],
                                    t['place'],
                                    t['starting_date'],
                                    t['ending_date'],
                                    t['number_of_rounds'],
                                    t['description']
                                    )
                tournament.current_round = t['current_round']
                tournament.list_rounds = [Round.from_dict(r) for r in t["list_rounds"]
]
                tournament.list_registered_players = t['list_registered_players']
                tournament.id = t["id"]
                list_tournaments.append(tournament)
            list_tournaments = sorted(list_tournaments, key=attrgetter("id", "name"), reverse=True)
            return list_tournaments

    @staticmethod
    def load_with_id(id):
        """Return a tournament with corresponding id"""
        tournaments = Tournament.load_all()
        for t in tournaments:
            if t.id == id:
                return t
        print("Aucun tournois avec cet identifiant n'existe.")
        return None

    @staticmethod
    def is_tournament_existing(id):
        tournaments = Tournament.load_all()
        return any(t.id == id for t in tournaments)

    @staticmethod
    def save_new(tournament):
        """Save an player in the Json database with an unique ID"""
        with open(DB_FILE_NAME, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            # We take the last gived ID and add 1 to it
            if len(data[TOURNAMENTS]) == 0:
                tournament.id = 0
            else:
                tournament.id = data[TOURNAMENTS][-1]["id"] + 1
            data[TOURNAMENTS].append(tournament.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)
        return tournament.id

    def register_player(self, player_id):
        if self.is_player_valid_for_registration(player_id):
            self.list_registered_players.append(player_id)

    def is_player_valid_for_registration(self, player_id):
        """Check if the player id is existing and if it's not already registered"""
        if Player.is_player_existing(player_id):
            if player_id in self.list_registered_players:
                print(f"Le joueur avec l'id \"{player_id}\" est déja inscrit.")
            else:
                print(f"Le joueur avec l'id \"{player_id}\" est maintenant inscrit.")
                return True
        else:
            print(f"Le joueur avec l'id \"{player_id}\" n'existe pas.")
        return False

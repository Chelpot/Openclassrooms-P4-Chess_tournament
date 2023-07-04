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

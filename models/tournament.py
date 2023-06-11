class Tournament:
 
    def __init__(self, name, place, starting_date, ending_date, description=""):
        self.name = name
        self.place = place
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.description = description

        self.current_round = 1
        self.number_of_rounds = 4
        self.list_rounds = []
        self.list_registered_players = []
        
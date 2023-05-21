class Tournament:
 
    def __init__(self, name, place):
        self.name = name,
        self.place = place,

        self.starting_date = None
        self.ending_date = None
        self.current_turn = 1
        self.number_of_turns = 4
        self.list_turns = []
        self.list_registered_players = []
        self.description = ""
        
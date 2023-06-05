class Turn:

    def __init__(self, name, starting_date_hour, ending_date_hour, matches=[]) :
        self.name = name
        self.starting_date_hour = starting_date_hour
        self.ending_date_hour = ending_date_hour
        self.matches = matches
        

    def add_match(self, first_player, second_player, first_player_score, second_player_score):
        """"Add a match to the list of matches for this turn with players and scores"""
        self.matches.append(((first_player, first_player_score), (second_player, second_player_score)))

    def validate_match(self):
        self.ending_date_hour = None #TODO: affecter time.now() à la validation du match.
        
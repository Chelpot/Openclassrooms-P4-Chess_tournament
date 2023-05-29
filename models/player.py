class Player:
    """A chess player"""
    def __init__(self, first_name, last_name, birth_date, national_chess_id):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id

    def __str__(self) -> str:
        return f"First name : {self.first_name}, Last name : {self.last_name}, Birthdate : {self.birth_date}, National chess id : {self.national_chess_id}"
        
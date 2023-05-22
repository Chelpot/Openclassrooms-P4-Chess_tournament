from view import global_view as v
from models import tournament, turn, player

def launch():
    running = True
    v.display_welcoming_message()
    while running:
        v.display_action_pannel()
        choice = input()
        call_function(choice)


def call_function(choice):
    if choice == "1":
        create_player()


def create_player():
    """create a player"""
    is_valid = False
    step = 0
    data = []
    while not is_valid:
        v.display_create_player(step)
        if step < 4:
            answer = input()
            step += 1
        else:
            is_valid = True
    
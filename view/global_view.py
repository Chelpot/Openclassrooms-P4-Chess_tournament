def display_welcoming_message():
    print("*************************************************")
    print("*   Bienvenue, vous utilisez actuellement un    *")
    print("*  logiciel permettant de gérer les tournois du *")
    print("*                 club d'échec.                 *")
    print("*************************************************")

def display_action_pannel():
    print("*************************************************")
    print("Entrez le numéro de l'action que vous souhaitez entreprendre :")
    print("1. Créer un joueur")


def display_create_player(step=0):
    if step == 0:
        print("Prénom : ")
    if step == 1:    
        print("Nom : ")
    if step == 2:
        print("Date de naissance (JJ/MM/AAAA) : ")
    if step == 3:
        print("Identifiant national d'échecs : ")
    if step == 4:
        print("Toutes les informations ont été saisies")

def display_players():
    """Display a list of all players in DB sorted by alphabetical order."""
    pass

def display_tournaments():
    """Display a list of all tournaments."""
    pass

def display_infos_for_tournament(tournament):
    """display the name and dates for a given tournament."""
    pass

def display_players_for_tournament():
    """display a list of all the players for a given tournament, the players will be sorted by alphabetical order."""
    pass

def display_matches_for_turns_of_tournament():
    """display all turns for a tournament, and all matches for each turns"""
    pass
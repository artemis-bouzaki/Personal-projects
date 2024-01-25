"""
This project is a top trumps game. The player get allocated a pokemon randomly,
and its features are compared to the computers randomly allocated pokemon. The user gets to choose the number of rounds and the stat to compare for each
round. The winner is determined by who has the highest stat value.

EXTENSIONS:      1) ADD CHARACTERISTICS FROM API OTHER THAN HEIGHT ETC
                 2) ALLOW MULTIPLE ROUNDS
                 3) NICE PRESENTATION OF ALL ROUND RESULTS AT THE END IN TABLE FORMAT
                 4) INPUT VALIDATION

Authors: Artemis Bouzaki
Date created: 11/01/2023
"""

# import necessary packages
import random
import requests
from prettytable import PrettyTable

def get_random_pokemon():
    """
    This function gets a random Pokemon using ID number from Pokemon API.

    Returns:
        pokemon_characteristics(dict): Dictionary of Pokemon features and their values.
    """
    # Generate random number
    pokemon_number = random.randint(1, 151)
    # Get Pokemon based on ID number from Pokemon API
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}/'
    response = requests.get(url)
    pokemon = response.json()

    # Record features in dictionary (can add more features easily here)
    pokemon_characteristics = {
        'name': pokemon['name'],
        'id': pokemon['id'],
        'height': pokemon['height'],
        'weight': pokemon['weight'],
        'base experience': pokemon['base_experience'] # this is an extra feature
    }
    return pokemon_characteristics

def choose_number_of_rounds():
    """
    This function is used to determine the number of rounds at the start of the game. The input is validated to meet the criteria.
    The player can choose to play up to 10 rounds.
    :return: number_of_rounds(int)
    """
    number_of_rounds = input("Please choose the number of rounds you want to play (up to 10 rounds): ")
    # Validate input
    while not number_of_rounds.isdigit() or int(number_of_rounds) < 1 or int(number_of_rounds) > 10:
        number_of_rounds = input("Please choose a number between 1 and 10 inclusive: ")

    return int(number_of_rounds)

def choose_stat():
    """
    This function takes input for stat choice checks if the parameter takes one of the acceptable values (id, height, weight)
    :param stat: str
    :return: bool
    """
    stat_choice = input("Which stat do you want to use for this round? (id, height, weight, base experience) ")
    # Check user input meets criteria CODE HERE (should be calling function check_stat_value)
    while stat_choice != "id" and stat_choice != "weight" and stat_choice != "height" and stat_choice != "base experience":
        stat_choice = input(
            "Please make sure you type the stat correctly. Choose one of the following: id, height, weight, base experience. ")
    return stat_choice

def choose_winner(player_score, opponent_score, player_win_count, opponent_win_count):
    """
    This function compares the players score to the opponents score and prints the winner.
    :param player_score: int
    :param opponent_score:  int
    :return: void
    """
    if player_score > opponent_score:
        print("Congratulations, you win! You get a point for winning this round.")
        player_win_count += 1
        round_winner = "Player"
    elif player_score < opponent_score:
        print("You lost this time. Your opponent gets a point.")
        opponent_win_count += 1
        round_winner = "Opponent"
    else:
        print(" It's a draw. No one gets a point.")
        round_winner = "Draw"
    return round_winner, player_win_count, opponent_win_count

def display_outcomes(round_results):
    """
    This function takes the array round_results containing all the important information about the round and converts it to a table.
    :param round_results: array
    :return: table of statistics and winners
    """
    table = PrettyTable()
    table.field_names = ["Round", "Player's Pokemon", "Opponent's Pokemon", "Stat Chosen", "Winner"]

    for round_number, result in enumerate(round_results, start=1):
        table.add_row([round_number, result["player_pokemon_name"], result["opponent_pokemon_name"],
                       result["stat_chosen"], result["winner"]])

    return table
def play_game():
    """
    This is the main function for the game. The player and opponent get allocated pokemons randomly. Player chooses a stat and the
    function determines a winner.
    :return: void
    """
    # Let player choose number of rounds and initialise to first round
    number_of_rounds = choose_number_of_rounds()
    current_round = 1
    #Initialise count for who wins each round and an array to hold stats of each round
    round_results = []
    player_win_count, opponent_win_count = 0, 0

    while current_round <= number_of_rounds:
        print(f"Round {current_round} started.")
        # Get a Pokemon for player and opponent randomly
        pokemon_player = get_random_pokemon()
        pokemon_opponent = get_random_pokemon()

        # Print the Pokemon allocated to the player
        print(f"You were given the following Pokemon: {pokemon_player['name']}")
        # Determine stat choice
        stat_choice = choose_stat()
        # Print details of opponents Pokemon name and stat
        print(f"Your opponent chose {pokemon_opponent['name']}")
        print(
            f"Your stat value is {pokemon_player[stat_choice]}. Your opponents stat value is {pokemon_opponent[stat_choice]}")

        # Display final outcome
        round_winner, player_win_count, opponent_win_count = choose_winner(pokemon_player[stat_choice], pokemon_opponent[stat_choice], player_win_count, opponent_win_count)
        # Save stats to array round_results
        round_results.append({
            "round_number": current_round,
            "player_pokemon_name": pokemon_player["name"],
            "opponent_pokemon_name": pokemon_opponent["name"],
            "stat_chosen": stat_choice,
            "winner": round_winner
        })
        # Increment to the next round
        current_round += 1

    # Display final results in a table format
    print("It's time for the final results...")
    print(display_outcomes(round_results))
    print(f"The final score is Player: {player_win_count} Opponent: {opponent_win_count}")
    if player_win_count > opponent_win_count:
        print("Congratulations! You had the majority of wins in this game.")
    elif opponent_win_count > player_win_count:
        print("Unfortunately, you lost. Good luck next time!")
    else:
        print("Overall, it's a draw!")

# Function calling
play_game()
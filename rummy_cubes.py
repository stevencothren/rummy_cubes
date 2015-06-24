from rummy_cubes_game import RummyCubesGame


def main(num_players, num_games):
    while num_games > 0:
        num_games -= 1
        game = RummyCubesGame(num_players)
        game.run()

if __name__ == "__main__":
    number_of_players = 2
    number_of_games = 1
    main(number_of_players, number_of_games)

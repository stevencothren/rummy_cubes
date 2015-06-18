from copy import deepcopy
from importlib import import_module
from random import shuffle


class RummyCubesGame:
    def __init__(self, num_players):
        self.players = []
        self.board = []
        self.bag = []
        self.game_over = False
        self.winner = -1
        self.initialize_game(num_players)

    def run(self):
        while not self.game_over:
            for player in self.players:
                if self.game_over:
                    break

                player_actions = player.move(deepcopy(self.board))

                # Player gave no actions, so is drawing a tile
                if not player_actions:
                    player.add_tile(self.draw_tile())
                    print("Draw Tile")
                else:
                    if self.process_move(player, player_actions):
                        print("Process Move")
                    else:
                        player.add_tile(self.draw_tile())
                        print("Invalid Player Actions - Draw Tile")

            self.game_over = True
            self.winner = 1

        print("Winner is player " + str(self.winner))

    def initialize_game(self, num_players):
        self.generate_tile_bag()

        for player_num in range(num_players):
            player_hand = self.draw_initial_hand()
            player_module = import_module("player_" + str(player_num + 1))
            ai = getattr(player_module, "player_ai")
            self.players.append(RummyCubesPlayer(player_hand, ai))

    def generate_tile_bag(self):
        # 106 tiles with 2 Jokers
        tile_ids = list(range(1, 107))
        shuffle(tile_ids)

        for value in range(1, 14):
            for suit in ["Black", "Blue", "Red", "Yellow"]:
                self.bag.append({'id': tile_ids.pop(),
                                 'suit': suit,
                                 'value': value})
                self.bag.append({'id': tile_ids.pop(),
                                 'suit': suit,
                                 'value': value})

        # Two Jokers
        self.bag.append({'id': tile_ids.pop(),
                         'suit': "Joker",
                         'value': -1})
        self.bag.append({'id': tile_ids.pop(),
                         'suit': "Joker",
                         'value': -1})

        shuffle(self.bag)
        return

    def draw_initial_hand(self):
        hand = {}
        for _ in range(14):
            tile = self.draw_tile()
            hand[tile['id']] = tile
        return hand

    def draw_tile(self):
        return self.bag.pop()

    def process_move(self, player, player_actions):
        # Validate player actions

        # If legal
        # Update player hand based on actions
        # Update player first_move
        # Update board based on actions
        # Check for game won
        return True


class RummyCubesPlayer:
    def __init__(self, player_hand, player_ai):
        self.hand = player_hand
        self.ai = player_ai
        self.first_move = True

    def move(self, board):
        return self.ai(board, deepcopy(self.hand), self.first_move)

    def get_player_hand(self):
        return deepcopy(self.hand)

    def remove_tile(self, tile_id):
        del self.hand[tile_id]

    def add_tile(self, tile):
        self.hand[tile['id']] = tile


def main(num_players, num_games):
    while num_games > 0:
        num_games -= 1
        game = RummyCubesGame(num_players)
        game.run()

if __name__ == "__main__":
    number_of_players = 2
    number_of_games = 1
    main(number_of_players, number_of_games)

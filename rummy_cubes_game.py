from copy import deepcopy
from importlib import import_module
from random import shuffle

from rummy_cubes_player import RummyCubesPlayer


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
            for player_idx, player in enumerate(self.players):
                if self.game_over:
                    break

                player_name = "Player " + str(player_idx + 1)

                print(player_name + "'s turn")
                player.print_hand()
                player_moves = player.move(deepcopy(self.board))

                # Player gave no actions, so is drawing a tile
                if not player_moves:
                    player.add_tile(self.draw_tile())
                    print("\tDrew a Tile")
                    player.print_hand()
                else:
                    print("Processing Player " + player_name + " Moves")
                    if self.process_move(player_idx, player_moves):
                        # TODO: Fix this nastiness!
                        player = self.players[player_idx]
                        print("\tMoves Successful")
                    else:
                        player.add_tile(self.draw_tile())
                        print("\tInvalid Player Actions - Draw Tile")

                    player.print_hand()

                if len(player.get_player_hand()) == 0:
                    self.winner = player_idx + 1
                    self.game_over = True

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

    def process_move(self, player_idx, player_moves):
        new_player = deepcopy(self.players[player_idx])
        new_board = deepcopy(self.board)
        new_player_hand = new_player.get_player_hand()
        valid_move = True

        print("Player moves : ")
        for move in player_moves:
            if not valid_move:
                break

            new_tile_set = []
            for tile_id in move:
                if not valid_move:
                    break

                print("\t" + str(tile_id))
                tile_in_hand = False
                tile_on_board = False

                # Check if the tile is in the player's hand
                if new_player.has_tile(tile_id):
                    new_tile_set.append(new_player.get_tile(tile_id))
                    new_player.remove_tile(tile_id)
                    tile_in_hand = True
                # Check if the tile is on the board
                else:
                    for i, tile_set in enumerate(new_board):
                        for j, tile in enumerate(tile_set):
                            if tile['id'] == tile_id:
                                tile_on_board = True
                                new_tile_set.append(tile)
                                del new_board[i][j]
                                break
                        if tile_on_board:
                            break

                if not tile_in_hand and not tile_on_board:
                    valid_move = False

            if valid_move:
                new_board.append(new_tile_set)

        for i, tile_set in enumerate(new_board):
            if not valid_move:
                break

            if len(tile_set) == 0:
                del new_board[i]
            elif len(tile_set) < 3:
                valid_move = False
            else:
                valid_set = True
                valid_run = True

                set_value = -1
                run_values = []
                tile_suits = {}

                for tile in tile_set:
                    if set_value == -1:
                        set_value = tile['value']
                    elif tile['value'] != set_value:
                        valid_set = False

                    if tile['suit'] in tile_suits:
                        valid_set = False
                    else:
                        tile_suits[tile['suit']] = 1

                    run_values.append(tile['value'])

                if not valid_set:
                    if len(tile_suits) > 1:
                        valid_run = False
                    else:
                        sorted_values = sorted(run_values)
                        cur_val = -1
                        for value in sorted_values:
                            if cur_val == -1:
                                cur_val = value
                            elif value == cur_val + 1:
                                cur_val = value
                            else:
                                valid_run = False
                                break

                if not valid_set and not valid_run:
                    valid_move = False

        print("Valid: " + str(valid_move))

        if valid_move:
            self.players[player_idx] = new_player
            self.board = new_board

        return valid_move

from copy import deepcopy
from importlib import import_module
from random import shuffle

from rummy_cubes_player import RummyCubesPlayer
from rummy_cubes_board import RummyCubesBoard


class RummyCubesGame:
    def __init__(self, num_players):
        self.players = []
        self.board = RummyCubesBoard()
        self.bag = []
        self.game_over = False
        self.winner = -1
        self.initialize_game(num_players)

        self.minimum_first_move_points = 30
        self.initial_hand_size = 14

    def initialize_game(self, num_players):
        self.generate_tile_bag()

        for player_num in range(num_players):
            player_hand = self.draw_initial_hand()
            player_module = import_module("player_" + str(player_num + 1))
            ai = getattr(player_module, "player_ai")
            self.players.append(RummyCubesPlayer(player_hand, ai))

    def generate_tile_bag(self):
        # 106 tiles with 2 Jokers
        # tile_ids = list(range(1, 107))
        # 106 tiles, no jokers
        tile_ids = list(range(1, 105))
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
        # TODO: Jokers are disabled for now
        # Need to add logic into the rummy_cubes_board to deal with them
        # self.bag.append({'id': tile_ids.pop(),
        #                 'suit': "Joker",
        #                 'value': -1})
        # self.bag.append({'id': tile_ids.pop(),
        #                 'suit': "Joker",
        #                 'value': -1})

        shuffle(self.bag)
        return

    def draw_initial_hand(self):
        hand = {}
        for _ in range(self.initial_hand_size):
            tile = self.draw_tile()
            hand[tile['id']] = tile
        return hand

    def draw_tile(self):
        return self.bag.pop()

    def run(self):
        while not self.game_over:
            player_action_count = 0
            for player_idx, player in enumerate(self.players):
                if self.game_over:
                    break

                player_name = "Player " + str(player_idx + 1)

                print(player_name + "'s turn")
                self.board.print_board()
                player.print_hand()
                player_moves = player.move(self.board.get_board())

                # Player gave no actions, so is drawing a tile
                if not player_moves:
                    player.add_tile(self.draw_tile())
                    player_action_count += 1
                    print("\tDrew a Tile")
                    player.print_hand()
                else:
                    print("Processing Player " + player_name + " Moves")
                    if self.process_move(player_idx, player_moves):
                        # TODO: Fix this nastiness!
                        player = self.players[player_idx]
                        player_action_count += 1
                        print("\tMoves Successful")
                    else:
                        player.add_tile(self.draw_tile())
                        print("\tInvalid Player Actions - Draw Tile")

                    player.print_hand()

                if len(player.get_player_hand()) == 0:
                    self.winner = player_idx + 1
                    self.game_over = True

            # No more tiles and no moves or draws during the last round
            if len(self.bag) == 0 and player_action_count == 0:
                self.game_over = True
                winner_tile_count = 0
                for player_idx, player in enumerate(self.players):
                    if winner_tile_count == -1:
                        winner_tile_count = len(player.get_player_hand)
                        self.winner = player_idx + 1
                    elif len(player.get_player_hand) < winner_tile_count:
                        winner_tile_count = len(player.get_player_hand)
                        self.winner = player_idx + 1

        print("Winner is player " + str(self.winner))

    def process_move(self, player_idx, player_moves):
        new_player = deepcopy(self.players[player_idx])
        new_board = deepcopy(self.board)
        move_point_total = 0
        valid_move = True

        print("Player moves : ")
        for move in player_moves:
            new_tile_set = []
            for tile_id in move:
                print("\t" + str(tile_id))
                # Check if the tile is in the player's hand
                if new_player.has_tile(tile_id):
                    move_point_total += new_player.get_tile_value(tile_id)
                    new_tile_set.append(new_player.pop_tile(tile_id))
                # Check if the tile is on the board
                elif new_board.has_tile(tile_id):
                    new_tile_set.append((new_board.pop_tile(tile_id)))
                else:
                    valid_move = False
                    break
            if valid_move:
                new_board.add_tile_set(new_tile_set)
            else:
                break

        new_board.remove_empty_tile_sets()

        if valid_move:
            if not new_board.is_valid():
                valid_move = False
            elif new_player.is_first_move():
                if move_point_total >= self.minimum_first_move_points:
                    new_player.first_move_made()
                else:
                    valid_move = False

        if valid_move:
            print("Move is Valid")
            self.players[player_idx] = new_player
            self.board = new_board
        else:
            print("Move is NOT Valid")

        return valid_move

from copy import deepcopy

class RummyCubesPlayer:
    def __init__(self, player_hand, player_ai):
        self.hand = player_hand
        self.ai = player_ai
        self.first_move = True

    def move(self, board):
        # TODO: Can the player AI change first_move?
        return self.ai(deepcopy(board), deepcopy(self.hand), self.first_move)

    def get_player_hand(self):
        return deepcopy(self.hand)

    def remove_tile(self, tile_id):
        del self.hand[tile_id]

    def add_tile(self, tile):
        self.hand[tile['id']] = tile

    def has_tile(self, tile_id):
        if self.hand[tile_id]:
            return True
        else:
            return False

    def get_tile(self, tile_id):
        return self.hand[tile_id]

    def get_tile_value(self, tile_id):
        return self.hand[tile_id]['value']

    def pop_tile(self, tile_id):
        tile = self.hand[tile_id]
        del self.hand[tile_id]
        return tile

    def is_first_move(self):
        return self.first_move

    def first_move_made(self):
        self.first_move = False

    def print_hand(self):
        print("Player Hand: ")
        for tile_id in self.hand:
            print("\t" + str(self.hand[tile_id]['id']) + " : " +
                  self.hand[tile_id]['suit'] + " : " + str(self.hand[tile_id]['value']))

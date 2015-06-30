

class RummyCubesBoard:
    def __init__(self):
        self.board = []

    def get_board(self):
        return self.board

    def set_board(self, new_board):
        self.board = new_board

    def get_tile_location(self, tile_id):
        tile_location = [-1, -1]
        for i, tile_set in enumerate(self.board):
            for j, tile in enumerate(tile_set):
                if tile['id'] == tile_id:
                    tile_location[0] = i
                    tile_location[1] = j
                    break
            if tile_location[0] != -1:
                break

        return tile_location

    def has_tile(self, tile_id):
        tile_location = self.get_tile_location(tile_id)

        if tile_location[0] != -1 and tile_location[1] != -1:
            return True
        else:
            return False

    def pop_tile(self, tile_id):
        tile_location = self.get_tile_location(tile_id)

        if tile_location[0] != -1 and tile_location[1] != -1:
            tile = self.board[tile_location[0]][tile_location[1]]
            del self.board[tile_location[0]][tile_location[1]]
        else:
            tile = None

        return tile

    def add_tile_set(self, tile_set):
        self.board.append(tile_set)
        return

    def remove_empty_tile_sets(self):
        for i, tile_set in enumerate(self.board):
            if len(tile_set) == 0:
                del self.board[i]
        return

    def is_valid(self):
        valid_board = True

        for i, tile_set in enumerate(self.board):
            if len(tile_set) < 3:
                valid_board = False
                break
            elif not self.is_valid_set(tile_set) and not self.is_valid_run(tile_set):
                valid_board = False
                break

        return valid_board

    @staticmethod
    def is_valid_set(tile_set):
        valid_set = True
        set_value = -1
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

        return valid_set

    @staticmethod
    def is_valid_run(tile_set):
        valid_run = True
        run_values = []
        tile_suits = {}

        for tile in tile_set:
            run_values.append(tile['value'])
            tile_suits[tile['suit']] = 1

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

        return valid_run

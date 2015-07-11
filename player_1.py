

def player_ai(game_board, player_hand, first_move):
    print("Player 1 AI Called")

    moves = []
    move_point_total = 0

    # TODO: Fix offsets so we don't have tile value 1 in the position 0, etc

    # Create a 4 x 13 array with the values of the tiles in the player's hand
    # Ignores the possibility of duplicate tiles
    hand = [[None for _ in range(13)] for _ in range(4)]
    for tile_id in player_hand:
        tile = player_hand[tile_id]
        if tile['suit'] == "Black":
            hand[0][tile['value']-1] = tile
        elif tile['suit'] == "Blue":
            hand[1][tile['value']-1] = tile
        elif tile['suit'] == "Red":
            hand[2][tile['value']-1] = tile
        elif tile['suit'] == "Yellow":
            hand[3][tile['value']-1] = tile

    # Search for sets in the player's hand
    set_tile_values = []
    for tile_value in range(13):
        total = 0
        for tile_suit in range(4):
            if hand[tile_suit][tile_value]:
                total += 1
        if total >= 3:
            set_tile_values.append(tile_value)

    # Add any sets to the list of moves the player will make, add the tile value to the total
    # And remove the tile from the player's hand
    for tile_value in set_tile_values:
        set_move = []
        for tile_suit in range(4):
            if hand[tile_suit][tile_value]:
                set_move.append(hand[tile_suit][tile_value]['id'])
                move_point_total += hand[tile_suit][tile_value]['value']
                hand[tile_suit][tile_value] = None
        moves.append(set_move)

    # Search for runs in the player's hand
    run_tile_sets = []
    for tile_suit in range(4):
        tile_value = 0
        while tile_value < 13:
            run_tile_set = []

            while tile_value < 13 and hand[tile_suit][tile_value]:
                run_tile_set.append([tile_suit, tile_value])
                tile_value += 1

            if len(run_tile_set) >= 3:
                run_tile_sets.append(run_tile_set)

            tile_value += 1

    # Add any runs to the list of moves the player will make, add the tile value to the total
    # And remove the tile from the player's hand
    for run_tile_set in run_tile_sets:
        run_move = []
        for tile in run_tile_set:
            run_move.append(hand[tile[0]][tile[1]]['id'])
            move_point_total += hand[tile[0]][tile[1]]['value']
            hand[tile[0]][tile[1]] = None
        moves.append(run_move)

    # Look for tiles in the player's hand that can be played on an existing tile set
    for tile_set in game_board:
        if is_set(tile_set):
            set_suits = {}
            set_value = tile_set[0]['value']
            tile_set_ids = []

            for tile in tile_set:
                set_suits[tile['suit']] = 1
                tile_set_ids.append(tile['id'])

            tile_to_add = None

            if 'Black' not in set_suits and hand[0][set_value - 1]:
                tile_to_add = [0, set_value - 1]
            elif 'Blue' not in set_suits and hand[1][set_value - 1]:
                tile_to_add = [1, set_value - 1]
            elif 'Red' not in set_suits and hand[2][set_value - 1]:
                tile_to_add = [2, set_value - 1]
            elif 'Yellow' not in set_suits and hand[3][set_value - 1]:
                tile_to_add = [3, set_value - 1]

            if tile_to_add:
                tile_set_ids.append(hand[tile_to_add[0]][tile_to_add[1]]['id'])
                move_point_total += hand[tile_to_add[0]][tile_to_add[1]]['value']
                hand[tile_to_add[0]][tile_to_add[1]] = None
                moves.append(tile_set_ids)

        elif is_run(tile_set):
            run_suit = tile_set[0]['suit']
            run_lowest = tile_set[0]['value']
            run_highest = tile_set[-1]['value']
            tile_set_ids = []

            for tile in tile_set:
                tile_set_ids.append(tile['id'])

            suit_value = -1
            if run_suit == 'Black':
                suit_value = 0
            elif run_suit == 'Blue':
                suit_value = 1
            elif run_suit == 'Red':
                suit_value = 2
            elif run_suit == 'Yellow':
                suit_value = 3

            if run_lowest > 1 and hand[suit_value][run_lowest - 2]:
                tile_set_ids.insert(0, hand[suit_value][run_lowest - 2]['id'])
                move_point_total += hand[suit_value][run_lowest - 2]['value']
                hand[suit_value][run_lowest - 2] = None

            if run_highest < 13 and hand[suit_value][run_highest]:
                tile_set_ids.append(hand[suit_value][run_highest]['id'])
                move_point_total += hand[suit_value][run_highest]['value']
                hand[suit_value][run_highest] = None

            if len(tile_set_ids) > len(tile_set):
                moves.append(tile_set_ids)

    if first_move and move_point_total < 30:
        moves = []

    return moves


def is_set(tile_set):
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


def is_run(tile_set):
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

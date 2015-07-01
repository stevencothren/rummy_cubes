

def player_ai(game_board, player_hand, first_move):
    print("Player 1 AI Called")

    moves = []
    move_point_total = 0

    # TODO: Fix offsets so we don't have tile value 1 in the position 0, etc

    # Create a 4 x 13 array with the values of the tiles in the player's hand
    # Ignores the possibility of duplicate tiles
    hand = [[None for x in range(13)] for x in range(4)]
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

    if first_move and move_point_total < 30:
        moves = []

    return moves

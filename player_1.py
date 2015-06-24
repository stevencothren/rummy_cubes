

def player_ai(game_board, player_hand, first_move):
    print("Player 1 AI Called")

    moves = []

    if first_move:
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

        possible_groups = []
        for i in range(13):
            total = 0
            for j in range(4):
                if hand[j][i]:
                    total += 1
            possible_groups.append(total)

        for i, val in enumerate(possible_groups):
            if val >= 3:
                new_move = []
                for j in range(4):
                    if hand[j][i]:
                        new_move.append(hand[j][i]['id'])
                moves.append(new_move)

    return moves
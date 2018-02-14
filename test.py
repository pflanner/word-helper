from word_score import GameBoard, Tile


def make_game_board(config):
    game_board = GameBoard(config)

    game_board.add_old_tile(Tile(letter='t', location=(4, 4)))
    game_board.add_old_tile(Tile(letter='o', location=(4, 5)))
    game_board.add_old_tile(Tile(letter='u', location=(4, 6)))
    game_board.add_old_tile(Tile(letter='t', location=(4, 7)))

    game_board.add_old_tile(Tile(letter='l', location=(5, 1)))
    game_board.add_old_tile(Tile(letter='a', location=(5, 2)))
    game_board.add_old_tile(Tile(letter='v', location=(5, 3)))
    game_board.add_old_tile(Tile(letter='a', location=(5, 4)))

    game_board.add_old_tile(Tile(letter='s', location=(6, 4)))
    game_board.add_old_tile(Tile(letter='h', location=(6, 5)))
    game_board.add_old_tile(Tile(letter='r', location=(6, 6)))
    game_board.add_old_tile(Tile(letter='e', location=(6, 7)))
    game_board.add_old_tile(Tile(letter='d', location=(6, 8)))

    game_board.add_old_tile(Tile(letter='x', location=(7, 7)))
    game_board.add_old_tile(Tile(letter='i', location=(7, 8)))
    game_board.add_old_tile(Tile(letter='s', location=(7, 9)))

    game_board.add_old_tile(Tile(letter='e', location=(6, 1)))
    game_board.add_old_tile(Tile(letter='a', location=(7, 1)))
    game_board.add_old_tile(Tile(letter='s', location=(8, 1)))
    game_board.add_old_tile(Tile(letter='e', location=(9, 1)))

    game_board.add_old_tile(Tile(letter='t', location=(8, 9)))
    game_board.add_old_tile(Tile(letter='u', location=(9, 9)))
    game_board.add_old_tile(Tile(letter='d', location=(10, 9)))

    game_board.add_old_tile(Tile(letter='h', location=(9, 10)))
    game_board.add_old_tile(Tile(letter='i', location=(10, 10)))
    game_board.add_old_tile(Tile(letter='r', location=(11, 10)))
    game_board.add_old_tile(Tile(letter='e', location=(12, 10)))
    game_board.add_old_tile(Tile(letter='d', location=(13, 10)))

    game_board.add_old_tile(Tile(letter='l', location=(10, 7)))
    game_board.add_old_tile(Tile(letter='e', location=(11, 7)))
    game_board.add_old_tile(Tile(letter='m', location=(12, 7)))

    game_board.add_old_tile(Tile(letter='s', location=(13, 5)))
    game_board.add_old_tile(Tile(letter='h', location=(13, 6)))
    game_board.add_old_tile(Tile(letter='o', location=(13, 7)))
    game_board.add_old_tile(Tile(letter='r', location=(13, 8)))
    game_board.add_old_tile(Tile(letter='e', location=(13, 9)))

    game_board.add_old_tile(Tile(letter='n', location=(14, 2)))
    game_board.add_old_tile(Tile(letter='a', location=(14, 3)))
    game_board.add_old_tile(Tile(letter='t', location=(14, 4)))
    game_board.add_old_tile(Tile(letter='i', location=(14, 5)))
    game_board.add_old_tile(Tile(letter='o', location=(14, 6)))
    game_board.add_old_tile(Tile(letter='n', location=(14, 7)))

    game_board.add_new_tile(Tile(letter='w', location=(9, 0)))
    game_board.add_new_tile(Tile(letter='i', location=(10, 0)))
    game_board.add_new_tile(Tile(letter='c', location=(11, 0)))
    game_board.add_new_tile(Tile(letter='k', location=(12, 0)))

    return game_board


def make_game_board_ben(config):
    b = GameBoard(config)
    b.add_old_tile(Tile(letter='c', location=(3, 7)))
    b.add_old_tile(Tile(letter='o', location=(4, 7)))
    b.add_old_tile(Tile(letter='v', location=(5, 7)))
    b.add_old_tile(Tile(letter='e', location=(6, 7)))
    b.add_old_tile(Tile(letter='y', location=(7, 7)))

    return b


def make_rack(str_rack):
    rack = []
    for letter in str_rack:
        rack.append(Tile(letter=letter))
    return rack


def print_progress(count):
    p = count / 13692
    p = p * 100
    f = "{:<102}"
    progress = '|' + ''.join(['=' * int(p)])
    print(f.format(progress) + '|')

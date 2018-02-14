from enum import Enum
import itertools
import test

tile_points = {
    'a': 1,
    'b': 4,
    'c': 4,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 3,
    'h': 3,
    'i': 1,
    'j': 10,
    'k': 5,
    'l': 2,
    'm': 4,
    'n': 2,
    'o': 1,
    'p': 4,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 2,
    'v': 5,
    'w': 4,
    'x': 8,
    'y': 3,
    'z': 10,
    '?': 0
}


class BoardConfig:
    def __init__(self):
        self.dl = set()
        self.tl = set()
        self.dw = set()
        self.tw = set()
        self.size = 15


class StandardBoardConfig(BoardConfig):
    def __init__(self):
        super().__init__()
        self.add_dls()
        self.add_tls()
        self.add_dws()
        self.add_tws()

    def add_dls(self):
        self.dl = set()
        self.dl.add((1, 2))
        self.dl.add((1, 12))
        self.dl.add((2, 1))
        self.dl.add((2, 4))
        self.dl.add((2, 10))
        self.dl.add((2, 13))
        self.dl.add((4, 2))
        self.dl.add((4, 6))
        self.dl.add((4, 8))
        self.dl.add((4, 12))
        self.dl.add((6, 4))
        self.dl.add((6, 10))
        self.dl.add((8, 4))
        self.dl.add((8, 10))
        self.dl.add((10, 2))
        self.dl.add((10, 6))
        self.dl.add((10, 8))
        self.dl.add((10, 12))
        self.dl.add((12, 1))
        self.dl.add((12, 4))
        self.dl.add((12, 10))
        self.dl.add((12, 13))
        self.dl.add((13, 2))
        self.dl.add((13, 12))

    def add_tls(self):
        self.tl.add((0, 6))
        self.tl.add((0, 8))
        self.tl.add((3, 3))
        self.tl.add((3, 11))
        self.tl.add((5, 5))
        self.tl.add((5, 9))
        self.tl.add((6, 0))
        self.tl.add((6, 14))
        self.tl.add((8, 0))
        self.tl.add((8, 14))
        self.tl.add((9, 5))
        self.tl.add((9, 9))
        self.tl.add((11, 3))
        self.tl.add((11, 11))
        self.tl.add((14, 6))
        self.tl.add((14, 8))

    def add_dws(self):
        self.dw.add((1, 5))
        self.dw.add((1, 9))
        self.dw.add((3, 7))
        self.dw.add((5, 1))
        self.dw.add((5, 13))
        self.dw.add((7, 3))
        self.dw.add((7, 11))
        self.dw.add((9, 1))
        self.dw.add((9, 13))
        self.dw.add((11, 7))
        self.dw.add((13, 5))
        self.dw.add((13, 9))

    def add_tws(self):
        self.tw.add((0, 3))
        self.tw.add((0, 11))
        self.tw.add((3, 0))
        self.tw.add((3, 14))
        self.tw.add((11, 0))
        self.tw.add((11, 14))
        self.tw.add((14, 3))
        self.tw.add((14, 11))


def compute_highest_score(board, rack):
    max_score = 0
    max_tiles = None
    count = 0
    for i in range(1, len(rack) + 1):
        for word in itertools.permutations(rack, i):
            count += 1
            if count % 140 == 0:
                test.print_progress(count)
            h_max_score, h_max_tiles = try_horizontal_placements(board, word)
            v_max_score, v_max_tiles = try_vertical_placements(board, word)
            max_score = max(max_score, max(h_max_score, v_max_score))
            max_tiles = h_max_tiles if max_score == h_max_score else v_max_tiles

    return max_score, max_tiles


def try_horizontal_placements(board, word):
    max_score = 0
    max_score_tiles = None
    for r in range(board.config.size):
        for c in range(board.config.size - len(word)):
            board.clear_new_tiles()
            cur_location = (r, c)
            for tile in word:
                tile.location = cur_location
                while not board.add_new_tile(tile) and tile.location[1] < board.config.size:
                    tile.location = (tile.location[0], tile.location[1] + 1)
                if tile.location in board.new_tiles:
                    cur_location = (tile.location[0], tile.location[1] + 1)
                else:
                    break
            if len(board.new_tiles) == len(word):
                max_score = max(max_score, compute_score(board))
                max_score_tiles = board.new_tiles.values()

    return max_score, max_score_tiles


def try_vertical_placements(board, word):
    max_score = 0
    max_score_tiles = None
    for r in range(board.config.size):
        for c in range(board.config.size - len(word)):
            board.clear_new_tiles()
            cur_location = (r, c)
            for tile in word:
                tile.location = cur_location
                while not board.add_new_tile(tile) and tile.location[0] < board.config.size:
                    tile.location = (tile.location[0] + 1, tile.location[1])
                if tile.location in board.new_tiles:
                    cur_location = (tile.location[0] + 1, tile.location[1])
                else:
                    break
            if len(board.new_tiles) == len(word):
                max_score = max(max_score, compute_score(board))
                max_score_tiles = board.new_tiles.values()

    return max_score, max_score_tiles


def load_dictionary():
    with open('./resources/words.txt') as f:
        return set(f.read().split())


def compute_score(board):
    """ compute the score based on the old and new tiles on the board

    :param board - an object describing the game board
    """

    if not check_validity(board):
        return 0

    score = 0
    for word in find_new_words(board):
        word_score = 0
        word_multiplier = 1
        for tile in word:
            tile_score = 0
            if not tile.is_wildcard:
                tile_score = tile_points.get(tile.letter)
                if tile.location in board.new_tiles:
                    if tile.location in board.config.dl:
                        tile_score *= 2
                    elif tile.location in board.config.tl:
                        tile_score *= 3

            if tile.location in board.config.dw:
                word_multiplier *= 2
            elif tile.location in board.config.tw:
                word_multiplier *= 3

            word_score += tile_score

        score += word_score * word_multiplier

        if len(board.new_tiles) == 7:
            score += 35

    return score


def find_new_words(board):
    # find the new words on the board
    words = set()  # a set of tuples of tiles

    for tile in board.new_tiles.values():
        word = [tile]
        cur = tile
        while cur.upper:
            cur = cur.upper
            word.insert(0, cur)

        cur = tile
        while cur.lower:
            cur = cur.lower
            word.append(cur)

        str_word = ''.join([x.letter for x in word])

        if str_word in dictionary and ((len(board.old_tiles) == 0 and len(word) == 1) or len(word) > 1):
            words.add(tuple(word))

        word = [tile]
        cur = tile
        while cur.left:
            cur = cur.left
            word.insert(0, cur)

        cur = tile
        while cur.right:
            cur = cur.right
            word.append(cur)

        str_word = ''.join([x.letter for x in word])

        if str_word in dictionary and ((len(board.old_tiles) == 0 and len(word) == 1) or len(word) > 1):
            words.add(tuple(word))

    return words


def check_validity(board):
    # check validity
    # todo check to make sure all tiles are in a line, are contiguous, are on the board and don't overlap
    # should we do this check here or as we're generating words?

    if board is None or board.new_tiles is None or len(board.new_tiles) == 0:
        return False

    old_tiles = board.old_tiles
    new_tiles = board.new_tiles

    # no tiles overlap
    for key in old_tiles.keys():
        for new_key in new_tiles.keys():
            if key == new_key:
                return False

    # new tiles in a line
    row = 0
    col = 1
    row_or_col = None
    row_col_value = None

    if len(new_tiles) > 1:
        items = iter(new_tiles.values())
        first_tile = next(items)
        second_tile = next(items)

        if first_tile.location[row] == second_tile.location[row]:
            row_or_col = row
            row_col_value = first_tile.location[row]

        if row_or_col is None or row_col_value is None:
            if first_tile.location[col] == second_tile.location[col]:
                row_or_col = col
                row_col_value = first_tile.location[col]
            else:
                return False

        if row_or_col is not None and row_col_value is not None:
            for item in items:
                if item.location[row_or_col] != row_col_value:
                    return False
        else:
            return False

    # contiguous
    # find the extreme tiles (highest/lowest or leftmost/rightmost) and make sure there are no gaps between them
    if len(new_tiles) == 1:
        if not next(iter(new_tiles.values())).has_neighbor():
            return False
    elif len(new_tiles) > 1:
        sorted_new_tile_locations = sorted(new_tiles.keys(), key=lambda loc: loc[row_or_col])
        for i in range(sorted_new_tile_locations[0][row_or_col - 1], sorted_new_tile_locations[-1][row_or_col - 1] + 1):
            current_location_row = i if row_or_col == col else row_col_value
            current_location_col = i if row_or_col == row else row_col_value
            current_location = (current_location_row, current_location_col)
            if current_location not in new_tiles and current_location not in old_tiles:
                return False

    # all new tiles are on the board
    for tile in new_tiles.values():
        if not board.is_on_board(tile):
            return False

    return True


class Orientation(Enum):
    VERTICAL = 0,
    HORIZONTAL = 1,
    SINGLE = 2,
    NONE = 3


class GameBoard:
    def __init__(self, board_config, **kwargs):
        self.old_tiles = kwargs.get('old_tiles', {})
        self.new_tiles = kwargs.get('new_tiles', {})
        self.config = board_config
        self.orientation = Orientation.NONE

    def add_old_tile(self, tile):
        loc = tile.location
        if loc is not None and loc not in self.old_tiles and loc not in self.new_tiles:
            self.neighborify(tile)
            self.old_tiles[loc] = tile
            return True
        else:
            return False

    def add_new_tile(self, tile):
        loc = tile.location
        if loc is not None and loc not in self.old_tiles and loc not in self.new_tiles and self.is_on_board(tile):
            new_orientation = Orientation.NONE
            if self.orientation == Orientation.NONE:
                new_orientation = Orientation.SINGLE
            elif self.orientation == Orientation.SINGLE:
                first_new_tile = next(iter(self.new_tiles.values()))
                if first_new_tile.location[0] == tile.location[0]:
                    new_orientation = Orientation.HORIZONTAL
                elif first_new_tile.location[1] == tile.location[1]:
                    new_orientation = Orientation.VERTICAL

            self.neighborify(tile)
            self.new_tiles[loc] = tile
            self.orientation = new_orientation

            return True
        else:
            return False

    def clear_new_tiles(self):
        for loc, tile in self.new_tiles.items():
            if tile.upper:
                tile.upper.lower = None
            if tile.lower:
                tile.lower.upper = None
            if tile.left:
                tile.left.right = None
            if tile.right:
                tile.right.left = None
        self.new_tiles = {}
        self.orientation = Orientation.NONE

    def neighborify(self, tile):
        loc = tile.location

        old_upper = self.old_tiles.get((loc[0] - 1, loc[1]))
        old_lower = self.old_tiles.get((loc[0] + 1, loc[1]))
        old_left = self.old_tiles.get((loc[0], loc[1] - 1))
        old_right = self.old_tiles.get((loc[0], loc[1] + 1))

        new_upper = self.new_tiles.get((loc[0] - 1, loc[1]))
        new_lower = self.new_tiles.get((loc[0] + 1, loc[1]))
        new_left = self.new_tiles.get((loc[0], loc[1] - 1))
        new_right = self.new_tiles.get((loc[0], loc[1] + 1))

        tile.upper = old_upper if old_upper is not None else new_upper
        tile.lower = old_lower if old_lower is not None else new_lower
        tile.left = old_left if old_left is not None else new_left
        tile.right = old_right if old_right is not None else new_right

        if tile.upper:
            tile.upper.lower = tile
        if tile.lower:
            tile.lower.upper = tile
        if tile.left:
            tile.left.right = tile
        if tile.right:
            tile.right.left = tile

    def is_on_board(self, tile):
        return 0 <= tile.location[0] < self.config.size and 0 <= tile.location[1] < self.config.size

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        row_format = "{:^5}" * self.config.size
        rows = []
        for r in range(self.config.size):
            row = []
            for c in range(self.config.size):
                loc = (r, c)
                tile = self.new_tiles.get(loc)
                if tile:
                    row.append("*" + tile.letter + "*")
                else:
                    tile = self.old_tiles.get(loc)
                    if tile:
                        row.append(tile.letter)
                    else:
                        row.append("")
            rows.append(row)
        return '\n'.join([row_format.format(*r) for r in rows])


class Tile:
    def __init__(self, **kwargs):
        self.upper = kwargs.get('upper', None)
        self.lower = kwargs.get('lower', None)
        self.left = kwargs.get('left', None)
        self.right = kwargs.get('right', None)
        self.letter = kwargs.get('letter', None)
        self.is_wildcard = kwargs.get('is_wildcard', False)
        self.location = kwargs.get('location', None)

    def has_neighbor(self):
        return self.upper is not None or \
               self.lower is not None or \
               self.left is not None or \
               self.right is not None

    def __str__(self):
        return self.letter

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Tile) and \
               self.letter == other.letter and \
               self.is_wildcard == other.is_wildcard and \
               self.location == other.location

    def __hash__(self):
        return hash(self.letter + str(self.is_wildcard) + str(self.location))


if __name__ == '__main__':
    dictionary = load_dictionary()
    config = StandardBoardConfig()
    game_board = test.make_game_board_ben(config)
    rack = test.make_rack("deohkoi")

    max_score, max_tiles = compute_highest_score(game_board, rack)
    game_board.clear_new_tiles()
    if max_tiles:
        for tile in max_tiles:
            game_board.add_new_tile(tile)
    print(max_score)
    print(game_board)

# TODO figure out why it's placing tiles off the board

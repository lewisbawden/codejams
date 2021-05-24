from adventofcode.y2019 import aoc
import time
import numpy as np


def day_20_part_1(tiles):
    neighbours = get_neighbour_tiles(tiles)
    corners = [k for k, n in neighbours.items() if len(n) == 2]
    return int(corners[0]) * int(corners[1]) * int(corners[2]) * int(corners[3])


def get_neighbour_tiles(tiles):
    num_tiles = len(tiles)
    tile_keys = [k for k in tiles.keys()]
    neighbours = {k: [] for k in tile_keys}

    def is_neighbour(t, n_edges):
        t_edges = [t[0, :], t[-1, :], t[:, 0], t[:, -1]]
        flipped = t_edges + [np.flip(t_edge) for t_edge in t_edges]
        for n_edge in n_edges:
            if any(np.array_equal(n_edge, t_edge) for t_edge in flipped):
                return True

    for i in range(num_tiles - 1):
        nk, nn = tile_keys[i], neighbours[tile_keys[i]]
        n_edges = [tiles[nk][0, :], tiles[nk][-1, :], tiles[nk][:, 0], tiles[nk][:, -1]]
        for j in range(i + 1, num_tiles):
            tk, t = tile_keys[j], tiles[tile_keys[j]]
            if is_neighbour(t, n_edges):
                neighbours[nk].append(tk)
                neighbours[tk].append(nk)
    return neighbours


def day_20_part_2(tiles):
    neighbours = get_neighbour_tiles(tiles)
    image_map = create_image_map(neighbours)
    image = create_image_from_map(image_map, tiles)
    return find_sea_monsters(image, sea_monster())


def find_sea_monsters(image, sm):
    valid_sm = np.sum(sm)
    invert = np.vectorize(lambda x: 0**x)
    not_sea_monster = invert(sm)

    smi, smj = sm.shape[0], sm.shape[1]
    for n in range(2):
        for m in range(4):
            for i in range(image.shape[0] - smi):
                for j in range(image.shape[1] - smj):
                    test = image[i: i + smi, j: j + smj]
                    test_mul = np.multiply(sm, test)
                    if valid_sm == np.sum(test_mul):
                        image[i: i + smi, j: j + smj] = np.multiply(image[i: i + smi, j: j + smj], not_sea_monster)
            image = np.rot90(image, 1)
        image = np.fliplr(image)
    return np.sum(image)


def sea_monster():
    with open("sea_monster.txt", "r") as f:
        data = f.readlines()
    sm = []
    for line in data:
        sml = []
        for s in line.strip("\n"):
            if s == "#":
                sml.append(1)
            else:
                sml.append(0)
        sm.append(sml)
    return np.array(sm, dtype=int)


def create_image_from_map(image_map, tiles):
    tile_size = next(iter(tiles.values())).shape[0] - 2
    n_size = image_map.shape[0] * tile_size
    image = np.zeros((n_size, n_size))

    def align_right(p1_name, p2_name):
        p1, p2 = tiles[p1_name], tiles[p2_name]
        for q in range(4):
            for m in range(2):
                for n in range(4):
                    if np.array_equal(p1[:, -1], p2[:, 0]):
                        tiles[p1_name] = p1
                        tiles[p2_name] = p2
                        return True
                    p2 = np.rot90(p2, 1)
                p2 = np.flipud(p2)
            p1 = np.rot90(p1, 1)
        return False

    def align_bottom(p1_name, p2_name):
        p1, p2 = tiles[p1_name], tiles[p2_name]
        for m in range(2):
            for n in range(4):
                if np.array_equal(p1[-1, :], p2[0, :]):
                    tiles[p2_name] = p2
                    return True
                p2 = np.rot90(p2, 1)
            p2 = np.fliplr(p2)
        return False

    # fix top left corner by checking right and down, then fix each tile row by row, left to right
    pc_name, pr_name, pb_name = str(image_map[0, 0]), str(image_map[0, 1]), str(image_map[1, 0])
    align_right(pc_name, pr_name)
    if not align_bottom(pc_name, pb_name):  # can only return false if top and top right need flipping vertically
        tiles[pc_name] = np.flipud(tiles[pc_name])
        tiles[pr_name] = np.flipud(tiles[pr_name])
        align_bottom(pc_name, pb_name)

    # percolate knowing top corner is correct so all others will just need rotating or flipping in place with no backtracking
    for i in range(image_map.shape[0]):
        for j in range(image_map.shape[0]):
            if i == 0 and j == 0:
                continue
            # top row first - rot/flip right tile place, knowing one to left is correct
            if i == 0 and j != image_map.shape[0] - 1:
                align_right(str(image_map[i, j]), str(image_map[i, j + 1]))
            if i > 0:
                # remaining rows - rot/flip only bottom tile, knowing one above is correct
                align_bottom(str(image_map[i - 1, j]), str(image_map[i, j]))

    for i in range(image_map.shape[0]):
        for j in range(image_map.shape[0]):
            image[i * tile_size: (i + 1) * tile_size, j * tile_size: (j + 1) * tile_size] = tiles[str(image_map[i, j])][1:-1, 1:-1]
    return image


def create_image_map(neighbours):
    n_size = int(np.sqrt(len(neighbours)))
    image_map = np.zeros((n_size, n_size), dtype=int)
    pieces = get_corners_edges_middle(neighbours)
    piece_map = get_piece_map(n_size)
    used = {}

    def increment_ij(_i, _j):
        _j += 1
        if _j == n_size:
            _j = 0
            _i += 1
        return _i, _j

    def allowed_piece(_i, _j, piece):
        if _i == 0 and _j == 0:
            return True

        if _i == 0:  # place top row based on left neighbour
            return str(image_map[_i, _j - 1]) in neighbours[piece]

        return str(image_map[_i - 1, _j]) in neighbours[piece]  # place remaining rows based on top neighbour

    # backtracking algorithm for finding just location of pieces in image map - no rotation / flipping yet
    def place_piece(i, j):
        if image_map.min() != 0:
            return True

        for piece in pieces[piece_map[i, j]].keys():
            if piece not in used:
                if allowed_piece(i, j, piece):
                    used[piece] = piece
                    image_map[i, j] = piece
                    if place_piece(*increment_ij(i, j)):
                        return True
                    else:
                        used.pop(piece)
                image_map[i, j] = 0
        return False

    if place_piece(0, 0):
        return image_map


def get_corners_edges_middle(neighbours):
    return {
        2: {k: v for k, v in neighbours.items() if len(v) == 2},  # corners
        1: {k: v for k, v in neighbours.items() if len(v) == 3},  # edges
        0: {k: v for k, v in neighbours.items() if len(v) == 4}   # middle
    }


def get_piece_map(n_size):
    piece_map = np.zeros((n_size, n_size), dtype=int)
    piece_map[:, 0] += 1
    piece_map[:, -1] += 1
    piece_map[0, :] += 1
    piece_map[-1, :] += 1
    return piece_map  # 2 => corners, 1 => edges, 0 => middles


def parse_tiles(data):
    def convert_line(tile_line):
        return [1 if pixel == "#" else 0 for pixel in tile_line]

    parsed = [tile.split(":\n") for tile in "".join(data).split("\n\n")]
    return {tile[0].strip("Tile "): np.array([convert_line(line) for line in tile[1].split("\n")]) for tile in parsed}


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_20_data.txt")
    # print(day_20_part_1(parse_tiles(data)))
    print(day_20_part_2(parse_tiles(data)))

    print(time.time() - t0)
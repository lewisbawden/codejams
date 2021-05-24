from adventofcode.y2019 import aoc
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

compass = {"ne": (0, 1), "e": (1, 1), "se": (1, 0), "sw": (0, -1), "w": (-1, -1), "nw": (-1, 0)}
sqrt3over2 = 0.86602540378


def day_24_part_1(lines):
    return len(first_tiles(lines))


def first_tiles(lines):
    tiles = set()
    for line in lines:
        i, j = 0, 0
        for cmd in line:
            i += compass[cmd][0]
            j += compass[cmd][1]
        if (i, j) in tiles:
            tiles.remove((i, j))
        else:
            tiles.add((i, j))
    return tiles


def hex_to_xy(i, j):
    return 0.5 * i + 0.5 * j, (-sqrt3over2) * i + sqrt3over2 * j


def day_24_part_2(lines):
    tiles = first_tiles(lines)
    lv = LiveView(tiles, 100)
    return len(lv.tiles)


class LiveView:
    def __init__(self, tiles, count):
        pg.setConfigOption('background', 'w')
        self.tiles = tiles
        self.prev_tiles = tiles
        self.count = count
        self.day = 0
        self.tile_plot_data = []
        self.prev_tile_plot_data = []

        self.app = QtWidgets.QApplication([])
        self.win = QtWidgets.QMainWindow()
        self.gv = pg.GraphicsView(parent=self.win)
        self.win.setCentralWidget(self.gv)
        self.pli = pg.PlotItem()
        self.scatter_points = pg.ScatterPlotItem()
        self.prev_scatter_points = pg.ScatterPlotItem()
        self.pli.addItem(self.scatter_points)
        self.pli.addItem(self.prev_scatter_points)
        self.start_b = QtWidgets.QPushButton("Start", parent=self.gv)
        self.start_b.setMaximumSize(35, 35)
        self.day_b = QtWidgets.QGraphicsSimpleTextItem()
        self.day_b.setText("Day: 0")
        self.gv.addItem(self.day_b)
        self.day_b.setPos(900, 0)
        self.day_b.hide()
        self.gv.setCentralWidget(self.pli)
        self.start_b.clicked.connect(self.execute_flip_tiles)

        # self.pli.sigRangeChanged.connect(self.update_data)
        # self.scatter_points.sigPlotChanged.connect(self.update_data)

        self.flip_tiles_step_thread = Worker(None, None)
        self.flip_tiles_thread = Worker(None, None)

        self.win.resize(1000, 800)
        self.win.move(50, 40)
        self.win.show()
        self.app.exec()

    def execute_flip_tiles(self):
        def output_result():
            return self.tiles
        self.flip_tiles_thread = Worker(self.flip_tiles)
        self.flip_tiles_thread.start()
        self.flip_tiles_thread.finished.connect(output_result)
        self.start_b.hide()
        self.day_b.show()

    def update_data(self):
        self.tile_plot_data = [{
                'pos': hex_to_xy(*ij),
                'data': ij,
                'size': 10,
                'pen': (0, 0, 0),
                'brush': (0, 0, 0),
                'symbol': "h"
            } for ij in self.tiles]
        gs = 180
        self.prev_tile_plot_data = [{
            'pos': hex_to_xy(*ij),
            'data': ij,
            'size': 10,
            'pen': (gs, gs, gs),
            'brush': (gs, gs, gs),
            'symbol': "h"
        } for ij in self.prev_tiles]
        scatter_points = pg.ScatterPlotItem(self.tile_plot_data)
        prev_scatter_points = pg.ScatterPlotItem(self.prev_tile_plot_data)
        while len(self.pli.curves) > 0:
            self.pli.clear()
        self.pli.addItem(scatter_points)
        self.pli.addItem(prev_scatter_points)
        self.scatter_points = scatter_points
        self.prev_scatter_points = prev_scatter_points
        self.xlims = self.scatter_points.dataBounds(0)
        self.ylims = self.scatter_points.dataBounds(1)

    def resize(self):
        try:
            f = 1.1
            self.pli.setXRange(self.xlims[0] * f, self.xlims[1] * f)
            self.pli.setYRange(self.ylims[0] * f, self.ylims[1] * f)
        except TypeError:
            pass

    def flip_tiles(self):
        def flip_tiles_step():
            print("flip_tiles_step", self.day)
            self.day_b.setText(f"Day: {self.day}")
            self.day += 1
            self.prev_tiles = self.tiles
            self.tiles = flip_tiles(self.tiles)
            self.update_data()
            # self.resize()

        while self.day < self.count:
            flip_tiles_step()
            time.sleep(0.5)
        return self.tiles


class Worker(QtCore.QThread):
    def __init__(self, func, *args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        self.output = 0

    def run(self):
        self.output = self.func(*self.args)


def flip_tiles(tiles):
    black_to_flip = set()
    potential_white_to_flip = set()
    white_to_flip = set()

    def flip_tile(_black, _tile, _tiles):
        adjacent = {(_tile[0] + i, _tile[1] + j) for i, j in compass.values()}
        occupied = adjacent.intersection(_tiles)
        if not _black and len(occupied) == 2:  # white tiles must have two black neighbour tiles
            white_to_flip.add(_tile)
        if _black:
            potential_white_to_flip.update(adjacent.difference(occupied))  # add all white tiles around a black tile (to a set)
            if len(occupied) == 0 or len(occupied) > 2:  # black tile can be flipped
                black_to_flip.add(_tile)

    for tile in tiles:  # find all black tiles to flip, populate white tile checklist
        flip_tile(True, tile, tiles)
    for tile in potential_white_to_flip:  # remove potential white to flip that are disqualified
        flip_tile(False, tile, tiles)

    final_tiles = tiles.difference(black_to_flip)
    final_tiles.update(white_to_flip)
    return final_tiles


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_24_data.txt")
    print(day_24_part_2([line.replace("e", "e ").replace("w", "w ").split() for line in data]))

    print(time.time() - t0)

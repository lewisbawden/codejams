import aoc
import time
import sys
import aoc_opcode as opc
from pyqtgraph.Qt import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np


def day_13_part_1(data):
    return BlockGame(data).num_blocks


def day_13_part_2(data):
    subs = {0: 2}

    app = QtWidgets.QApplication([])
    gui = BlockGameGui(data, subs)
    gui.show()
    app.exec()

    return None


class BlockGameGui(QtWidgets.QMainWindow):
    keyPressedSignal = QtCore.pyqtSignal(object)

    def __init__(self, data, subs=None):
        super(BlockGameGui, self).__init__()
        self.game = BlockGame(data, subs)
        self.game.initialise()
        self.keyPressedSignal.connect(self.update_game)
        self.game.signal_state_updated.connect(self.update_game)

        self.resize(800, 600)
        self.image = pg.ImageItem()
        self.image.setImage(self.game.screen)
        self.view = pg.PlotWidget()
        self.view.addItem(self.image)

        self.play_button = QtWidgets.QPushButton("Play")
        self.play_button.clicked.connect(self.start_game_pushed)
        self.cheat_button = QtWidgets.QPushButton("Cheat")
        self.cheat_button.setCheckable(True)
        self.cheat_button.clicked.connect(self.cheat_pushed)

        self.pause_button = QtWidgets.QPushButton("Pause")
        font = self.font()
        font.setPointSize(16)
        self.pause_button.setFont(font)
        self.pause_button.setCheckable(True)
        self.pause_button.clicked.connect(self.pause_pushed)
        self.pause_button.setFixedHeight(200)

        self.score_view = QtWidgets.QLCDNumber()
        self.score_view.setDigitCount(8)
        self.score_view.display(self.game.score)

        palette = self.score_view.palette()
        palette.setColor(palette.WindowText, QtGui.QColor(85, 85, 255))
        palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        self.score_view.setPalette(palette)

        game_speed_label = QtWidgets.QLabel("Game Speed")
        self.game_speed_button = QtWidgets.QDoubleSpinBox()
        self.game_speed_button.setValue(self.game.game_speed)
        self.game_speed_button.setSingleStep(0.1)
        self.game_speed_button.setMinimum(0.00001)
        self.game_speed_button.valueChanged.connect(lambda v: self.game.update_speed(v))

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.play_button, 0, 0, 1, 2)
        self.layout.addWidget(self.cheat_button, 1, 0, 1, 2)
        self.layout.addWidget(game_speed_label, 2, 0, 1, 2)
        self.layout.addWidget(self.game_speed_button, 3, 0, 1, 2)
        self.layout.addWidget(self.score_view, 0, 2, 4, 4)
        self.layout.addWidget(self.pause_button, 0, 6, 4, 3)
        self.layout.addWidget(self.view, 5, 0, 8, 9)

        self.win = QtWidgets.QWidget()
        self.win.setLayout(self.layout)
        self.setCentralWidget(self.win)
        self.view.setAspectLocked(True)
        self.setFocus()

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key_A or a0.key() == QtCore.Qt.Key_Left:
            inp = -1
        elif a0.key() == QtCore.Qt.Key_D or a0.key() == QtCore.Qt.Key_Right:
            inp = 1
        elif a0.key() == QtCore.Qt.Key_S or a0.key() == QtCore.Qt.Key_Down:
            inp = 0
        else:
            QtWidgets.QMainWindow.keyPressEvent(self, a0)
            return
        self.keyPressedSignal.emit(inp)

    def pause_pushed(self):
        if not self.pause_button.isChecked():
            self.game.set_paused(False)
            print("Unpaused")
        else:
            self.game.set_paused(True)
            print("Paused")

    def cheat_pushed(self):
        if not self.cheat_button.isChecked():
            self.game.set_cheat(False)
            print("Cheat off")
        else:
            self.game.set_cheat(True)
            print("Cheat on")

    def start_game_pushed(self):
        self.game.start_game(self.game_speed_button.value())

    def update_game(self, k=0):
        self.game.update_input(k)
        self.image.setImage(self.game.screen)
        self.score_view.display(self.game.score)
        self.update()


class Worker(QtCore.QThread):
    def __init__(self, func, *args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


class BlockGame(QtCore.QObject):
    signal_state_updated = QtCore.pyqtSignal(int)

    def __init__(self, data, subs=None, debug=False):
        super(BlockGame, self).__init__()
        self.init_data = data, subs
        self.cheat = False
        self.debug = debug

    def initialise(self):
        self.comp = opc.IntCode(*self.init_data)
        self.game_speed = 0.5
        self.paused = False
        self.inp = 0
        self.ticks = 0
        self.setup_game()

    def setup_game(self):
        self.ec, self.out = self.comp.run_opcode()
        self.get_tiles()

        def tiles_gen(tiles, coord):
            for t in tiles:
                yield t[coord]

        minx, maxx = min(tiles_gen(self.tiles, 0)), max(tiles_gen(self.tiles, 0))
        miny, maxy = min(tiles_gen(self.tiles, 1)), max(tiles_gen(self.tiles, 1))
        self.screen = np.zeros(shape=(maxx-minx+1, maxy-miny+1))
        self.fill_blocks()

    def get_tiles(self):
        self.tiles = [[self.out[i], self.out[i + 1], self.out[i + 2]] for i in range(0, len(self.out), 3)]
        self.num_blocks = sum([1 if t[2] == 2 else 0 for t in self.tiles])
        try:
            self.paddle = [t for t in self.tiles if t[2] == 3][0]
            self.move = self.paddle[0]
        except IndexError:
            pass
        try:
            self.ball = [t for t in self.tiles if t[2] == 4][0]
        except IndexError:
            pass
        try:
            score_tile = [t for t in self.tiles if t[0] == -1 and t[1] == 0][0]
            self.tiles = [t for t in self.tiles if t[0] != -1 or t[1] != 0]
            if score_tile[2] != 0 or self.ticks == 0:
                self.score = score_tile[2]
        except IndexError:
            pass

    def fill_blocks(self):
        for x, y, b in self.tiles:
            self.screen[x, y] = b

    def start_game(self, speed=None):
        print("Starting game")
        self.initialise()
        if speed is not None:
            self.game_speed = speed
        self.game_loop = Worker(self.update_state)
        self.game_loop.start()

    def update_speed(self, v):
        self.game_speed = v

    def set_paused(self, paused):
        self.paused = paused

    def set_cheat(self, cheat):
        self.cheat = cheat

    def update_state(self):
        t0 = time.time()
        while not self.ec:
            if time.time() - t0 > self.game_speed and not self.paused:
                t0 = time.time()
                self.ticks += 1
                if self.debug: print(f"Round {self.ticks}: using {self.inp}")
                self.ec, self.out = self.comp.run_opcode(self.inp)
                self.get_tiles()
                self.fill_blocks()
                self.signal_state_updated.emit(0)
                if self.debug: print(self.tiles, file=sys.stderr)
            if self.cheat: self.update_input()
            time.sleep(0.001)

    @QtCore.pyqtSlot(int)
    def update_input(self, inp=0):
        if self.cheat:
            self.inp = self.ball[0] - self.paddle[0]
        else:
            if inp == -1 and self.inp != -1:
                self.move -= 1
                self.inp -= 1
            elif inp == 1 and self.inp != 1:
                self.move += 1
                self.inp += 1
            elif inp == 0:
                self.inp = 0

        if 0 < self.move < self.screen.shape[0] - 2:
            self.screen[1:-1, self.paddle[1]] = 0
            self.screen[self.move, self.paddle[1]] = 3


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_13_data.txt")
    print(day_13_part_2(data))

    print(time.time() - t0)

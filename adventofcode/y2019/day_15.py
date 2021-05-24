import aoc
import time
import operator as op
import aoc_opcode as opc
from pyqtgraph.Qt import QtWidgets, QtGui, QtCore
import pyqtgraph as pg


class RepairDroidGui(QtWidgets.QMainWindow):
    keyPressedSignal = QtCore.pyqtSignal(object)

    def __init__(self, data, subs=None, auto_pilot=False):
        super(RepairDroidGui, self).__init__()
        self.droid = RepairDroid(data, subs, auto_pilot=auto_pilot)
        self.keyPressedSignal.connect(self.update_droid_state)
        self.droid.signal_state_updated.connect(self.update_droid_state)
        self.droid.signal_oxygen_updated.connect(self.update_oxygen_state)

        self.colours = [(255, 220, 150), (255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 0, 0), (75, 75, 255)]
        self.scp_data = {(0, 0): self.get_sp_entry((0, 0), Blocks.origin)}

        self.resize(1600, 900)
        self.maze_view = pg.ScatterPlotItem()
        self.view = pg.PlotWidget()
        self.view.addItem(self.maze_view)
        self.view.setXRange(min=-22, max=22)
        self.view.setYRange(min=-22, max=22)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.view, 0, 0)

        self.win = QtWidgets.QWidget()
        self.win.setLayout(self.layout)
        self.setCentralWidget(self.win)
        self.view.setAspectLocked(True)
        self.setFocus()

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key_A or a0.key() == QtCore.Qt.Key_Left:
            inp = Coords.W
        elif a0.key() == QtCore.Qt.Key_D or a0.key() == QtCore.Qt.Key_Right:
            inp = Coords.E
        elif a0.key() == QtCore.Qt.Key_S or a0.key() == QtCore.Qt.Key_Down:
            inp = Coords.S
        elif a0.key() == QtCore.Qt.Key_W or a0.key() == QtCore.Qt.Key_Up:
            inp = Coords.N
        else:
            QtWidgets.QMainWindow.keyPressEvent(self, a0)
            return
        self.keyPressedSignal.emit(inp)

    def update_state(self, new_points):
        scp_entries = {k: self.get_sp_entry(k, v) for k, v in new_points.items()}
        self.maze_view.addPoints([i for i in scp_entries.values()])
        self.update()

    def update_oxygen_state(self, oxygen_list):
        scp_entries = {k: self.get_sp_entry(k, Blocks.oxygen_gas) for k in oxygen_list}
        self.maze_view.addPoints([i for i in scp_entries.values()])
        self.update()
        self.droid.oxygen_updated = True

    def update_droid_state(self, k=0):
        new_points = self.droid.update_input(k)
        self.update_state(new_points)

    def get_sp_entry(self, k, v):
        if k == (0, 0) and not self.droid.oxygen_found:
            v = Blocks.origin
        if k == self.droid.oxygen_unit_xy and not self.droid.maze_complete:
            v = Blocks.oxygen_unit
        return {'pos': k, 'data': v, 'size': 15, 'pen': self.colours[v], 'brush': self.colours[v], 'symbol': "s"}


class Worker(QtCore.QThread):
    def __init__(self, func, *args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


class Coords:
    N = 1
    S = 2
    W = 3
    E = 4


class Blocks:
    wall = 0
    empty = 1
    oxygen_unit = 2
    droid = 3
    origin = 4
    oxygen_gas = 5


class Block:
    mapper = {1: [0, 1], 2: [0, -1], 3: [-1, 0], 4: [1, 0]}
    mapper_rev = {(0, 1): 1, (0, -1): 2, (-1, 0): 3, (1, 0): 4}

    def __init__(self, k, v, parent, distance):
        self.xy = k
        self.type = v
        self.parent = parent
        self.distance = distance
        self.dead_end = False

        self.children = self.init_children()
        self.inp_back = self.get_inp_back()
        self.remove_child(self.inp_back)

    def init_children(self):
        x, y = self.xy
        cond = op.gt
        east_west = [Coords.E, Coords.W] if cond(x, 0) else [Coords.W, Coords.E]
        north_south = [Coords.N, Coords.S] if cond(y, 0) else [Coords.S, Coords.N]
        if cond(abs(x), abs(y)):
            children = [east_west[0]] + north_south + [east_west[1]]
        else:
            children = [north_south[0]] + east_west + [north_south[1]]
        return {c: None for c in children}

    def get_inp_back(self):
        if self.parent is None:
            return None
        x = self.parent[0] - self.xy[0]
        y = self.parent[1] - self.xy[1]
        return self.mapper_rev[(x, y)]

    def get_child(self, inp):
        return self.xy[0] + self.mapper[inp][0], self.xy[1] + self.mapper[inp][1]

    def remove_child(self, inp):
        if inp in self.children.keys():
            self.children.pop(inp)
            if len(self.children) == 0:
                self.dead_end = True


class RepairDroid(QtCore.QObject):
    signal_state_updated = QtCore.pyqtSignal(int)
    signal_oxygen_updated = QtCore.pyqtSignal(list)

    def __init__(self, data, subs=None, auto_pilot=True):
        super(RepairDroid, self).__init__()
        self.init_data = data, subs
        self.comp = opc.IntCode(*self.init_data)
        self.x = 0
        self.y = 0
        self.out = 0
        self.update_complete = False
        self.maze = {(self.x, self.y): Blocks.droid}
        Block.mapper = {1: [0, 1], 2: [0, -1], 3: [-1, 0], 4: [1, 0]}
        self.paths = {(0, 0): Block((0, 0), Blocks.origin, None, 0)}

        self.maze_complete = False
        self.oxygen_found = False
        self.oxygen_complete = False
        self.oxygen_updated = False
        self.oxygen_unit_xy = None
        self.oxygen_paths = {"unfilled": [], "filled": []}
        self.oxygen_minutes = -1

        if auto_pilot:
            self.worker = Worker(self.find_oxygen_system)
            self.worker.start()

    @QtCore.pyqtSlot(int)
    def update_input(self, inp=None):
        self.inp = inp
        self.ec, out = self.comp.run_opcode(self.inp)
        if len(out) > 0:
            self.out = out[0]
            return self.update_maze()
        else:
            self.update_complete = True
            self.maze_complete = True
            return {}

    def update_maze(self):
        new_points = {}
        if self.out > 0:
            new_points[(self.x, self.y)] = Blocks.empty
            self.x += Block.mapper[self.inp][0]
            self.y += Block.mapper[self.inp][1]
            new_points[(self.x, self.y)] = Blocks.droid
        if self.out == 2:
            print("Found O2 system")
            new_points[(self.x, self.y)] = Blocks.oxygen_unit
            self.oxygen_unit_xy = (self.x, self.y)
            self.oxygen_found = True
        elif self.out == 0:
            new_points[(self.x + Block.mapper[self.inp][0], self.y + Block.mapper[self.inp][1])] = Blocks.wall
        self.maze.update(new_points)
        self.update_paths(new_points)
        return new_points

    def update_paths(self, new_points):
        block_coords_dict = {v: k for k, v in new_points.items()}  # k: coords of position; v: type of block

        if Blocks.empty in block_coords_dict.keys():
            old_position = block_coords_dict[Blocks.empty]
            new_position = None
            if Blocks.droid in block_coords_dict.keys():
                new_position = block_coords_dict.get(Blocks.droid)
            elif Blocks.oxygen_unit in block_coords_dict.keys():
                new_position = block_coords_dict.get(Blocks.oxygen_unit)
                self.oxygen_paths["unfilled"] = [new_position]
                self.paths[new_position] = Block(new_position, new_points[new_position],
                                                 parent=block_coords_dict[Blocks.empty],
                                                 distance=self.paths[old_position].distance + 1)
                self.paths[old_position].children[self.inp] = new_position
                print("Oxygen found at distance:", self.paths[old_position].distance + 1)
            if new_position is not None and new_position not in self.paths.keys():
                self.paths[new_position] = Block(new_position, new_points[new_position],
                                                 parent=block_coords_dict[Blocks.empty],
                                                 distance=self.paths[old_position].distance + 1)
                self.paths[old_position].children[self.inp] = new_position

        if Blocks.wall in block_coords_dict.keys():
            block = (self.x, self.y)
            self.paths[block].remove_child(self.inp)
            if self.paths[block].dead_end:
                while True:
                    parent = self.paths[block].parent
                    if parent is None:
                        self.maze_complete = True
                        break
                    all_dead_ends = all(self.paths[self.paths[parent].get_child(c)].dead_end == False for c in self.paths[parent].children)
                    if not (len(self.paths[parent].children) < 2 or all_dead_ends):
                        break
                    self.paths[parent].dead_end = True
                    block = parent
        self.update_complete = True

    def send_update_signal(self, inp):
        self.update_complete = False
        self.signal_state_updated.emit(inp)
        while not self.update_complete:
            time.sleep(0.0000005)

    def send_oxygen_signal(self, oxygen_list):
        self.oxygen_updated = False
        self.signal_oxygen_updated.emit(oxygen_list)
        while not self.oxygen_updated:
            time.sleep(0.0000005)

    def propogate_oxygen(self):
        if len(self.oxygen_paths["unfilled"]) == 0:
            self.send_oxygen_signal([(0, 0)])
            self.oxygen_complete = True
            return self.oxygen_complete

        self.send_oxygen_signal(self.oxygen_paths["unfilled"])

        new_oxygens = []
        for i in range(len(self.oxygen_paths["unfilled"]) - 1, -1, -1):
            oxy = self.oxygen_paths["unfilled"].pop()
            self.oxygen_paths["filled"].append(oxy)

            parent = self.paths[oxy].parent
            children = [c for c in self.paths[oxy].children.values()]
            valid_new_oxygens = [o for o in [parent] + children
                                 if o not in self.oxygen_paths["filled"]
                                 and o is not None]
            new_oxygens.extend(valid_new_oxygens)

        self.oxygen_paths["unfilled"].extend(new_oxygens)
        self.oxygen_minutes += 1

    def propogate_droid(self):
        b = self.paths[(self.x, self.y)]
        while b.dead_end:
            self.send_update_signal(b.inp_back)
            b = self.paths[(self.x, self.y)]
            if b.inp_back is None and b.dead_end:
                self.maze_complete = True
                self.update_complete = True
                return

        inps = [k for k in b.children.keys()]
        for inp in inps:
            # explore all routes first
            if b.children[inp] is None:
                self.send_update_signal(inp)
                if self.out != Blocks.wall:
                    self.update_input(self.paths[b.children[inp]].inp_back)
            # then explore known available routes that aren't dead ends
            elif not self.paths[b.children[inp]].dead_end:
                self.send_update_signal(inp)
                break
            # remove if dead end
            else:
                b.dead_end = True

    def find_oxygen_system(self):
        while not self.maze_complete:
            self.propogate_droid()
        while not self.oxygen_complete:
            print("Minutes since oxygen started:", self.oxygen_minutes)
            self.propogate_oxygen()


def day_15_part_1(data):
    app = QtWidgets.QApplication([])
    gui = RepairDroidGui(data, auto_pilot=True)
    gui.show()
    app.exec()
    return None


def day_15_part_2(data):

    return None


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_15_data.txt")
    print(day_15_part_1(data))

    print(time.time() - t0)

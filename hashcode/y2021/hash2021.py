import os
import time
import math


class Street:
    def __init__(self, vals):
        self.interx_in = vals[0]
        self.interx_out = vals[1]
        self.name = vals[2]
        self.length = int(vals[3])
        self.total_cars = 0
        self.total_cars_time = 0


class Car:
    def __init__(self, car_line):
        vals = car_line.split()
        self.num_roads = int(vals[0])
        self.route = vals[1:]
        self.total_time = 0


class Intersection:
    def __init__(self, name):
        self.name = name
        self.outgoing = []
        self.incoming = []
        self.score = 0


class Simulation:
    def __init__(self, header):
        vals = [int(v) for v in header.split()]
        self.duration = vals[0]
        self.num_intersections = vals[1]
        self.num_streets = vals[2]
        self.num_cars = vals[3]
        self.score = vals[4]

        self.streets = {}
        self.cars = {}
        self.intersections = {}
        self.output = []

    def add_streets(self, data):
        for line in data:
            vals = line.split()
            start, end, name, length = vals
            self.streets[name] = Street(vals)

            if start in self.intersections.keys():
                self.intersections[start].outgoing.append(name)
            else:
                self.intersections[start] = Intersection(start)
                self.intersections[start].outgoing = [name]

            if end in self.intersections.keys():
                self.intersections[end].incoming.append(name)
            else:
                self.intersections[end] = Intersection(end)
                self.intersections[end].incoming = [name]

    def add_cars(self, data):
        if len(self.streets) == 0:
            print("Add streets first")
            exit(0)

        for idx, line in enumerate(data):
            self.cars[idx] = Car(line)
            self.cars[idx].total_time = sum(self.streets[s].length for s in self.cars[idx].route)

        for car in self.cars.values():
            for street in car.route:
                self.streets[street].total_cars += 1
                self.streets[street].total_cars_time += car.total_time

    def analyse_input(self, print_num=0):
        num_valid_cars = sum(1 for c in self.cars.values() if c.total_time < self.duration)
        if print_num > 0:
            print("Total cars: {}, total that can reach destination {}".format(self.num_cars, num_valid_cars))

        self.ordered_streets = sorted([s for s in self.streets.values()], key=lambda s: -s.total_cars)
        for p in range(min(print_num, len(self.ordered_streets))):
            print(self.ordered_streets[p].__dict__)

        self.ordered_intersections = sorted([i for i in self.intersections.values()], key=lambda i: len(i.incoming))
        for p in range(min(print_num, len(self.ordered_intersections))):
            print(self.ordered_intersections[p].__dict__)

    def calc_output(self):
        max_lights = 5e10
        factor = 0.01
        for itx_key in self.intersections.keys():
            inter = self.intersections[itx_key]
            inter.score = sum(self.streets[s].total_cars_time for s in inter.incoming)
            lights = int(min(max_lights, len(inter.incoming)))
            if lights > 0 and inter.score > 0:
                outstrs = []
                for light_idx in range(lights):
                    inc_street = self.streets[inter.incoming[light_idx]]
                    ltime = math.ceil((inc_street.total_cars_time / inter.score) * self.duration * factor)
                    ltime = max(1, ltime)
                    outstrs.append("{} {}\n".format(inc_street.name, ltime))

                out = "{}\n{}\n".format(inter.name, lights)
                out += "".join(outstrs)

                self.output.append(out)


def hash_main(infile):
    with open(infile, "r") as f:
        inp = f.readlines()

    out = [line.rstrip('\n') for line in inp]

    sim = Simulation(out[0])
    sim.add_streets(out[1: 1 + sim.num_streets])
    sim.add_cars(out[1 + sim.num_streets:])

    sim.analyse_input(10)

    sim.calc_output()

    generate_output(infile, sim)


def generate_output(infile, sim):
    par = os.path.dirname(os.path.dirname(infile))
    fname = os.path.basename(infile)
    outfile = os.path.join(par, "Python", "Output", fname)

    output = sim.output
    with open(outfile.replace(".txt", ".out"), "w") as w:
        w.write("{}\n".format(len(output)))
        [w.write(out) for out in output]


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(__file__))
    for ch in ['a', 'b', 'c', 'd', 'e', 'f']:
        _infile = os.path.join(base, rf"InputFiles\{ch}.txt")
        t0 = time.time()
        hash_main(_infile)
        print(_infile, "Duration: ", time.time() - t0)

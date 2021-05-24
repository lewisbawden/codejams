class IntCode:
    def __init__(self, program_string, subs=None):
        self.program = self.parse_program(program_string, subs)
        self.expected_params = {0: None, 1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1}
        self.exit_code = False
        self.inp = None
        self.outp = []
        self.pointer = 0
        self.relative_base = 0
        self.run_opcode_funcs = {1: self.opcode_1, 2: self.opcode_2, 3: self.opcode_3, 4: self.opcode_4,
                                 5: self.opcode_5, 6: self.opcode_6, 7: self.opcode_7, 8: self.opcode_8,
                                 9: self.opcode_9}

    def run_opcode(self, _inp=None):
        self.inp = _inp
        self.outp = []

        incode = self.program[self.pointer]

        while True:
            params = self.parse_opcode(incode)
            argv = [self.program[p] if p in self.program.keys() else 0
                    for p in range(self.pointer + 1, self.pointer + len(params[1]) + 1)]
            argsm = [args for args in zip(argv, params[1])]

            self.run_opcode_funcs[params[0]](argsm)
            incode = self.program[self.pointer]

            if incode == 99:
                self.exit_code = True
                return self.exit_code, self.outp
            elif self.inp is None and incode == 3:
                return self.exit_code, self.outp

    @staticmethod
    def parse_program(program_string, subs=None):
        parsed = dict()
        count = 0
        for p in program_string:
            for s in p.split(","):
                if s != "\n":
                    parsed[count] = int(s)
                    count += 1
        if subs is not None:
            for mem, sub in subs.items():
                parsed[mem] = sub
        return parsed

    def opcode_1(self, args):
        self.program[self.p2mem(args[2])] = self.p2v(args[0]) + self.p2v(args[1])
        self.pointer += len(args) + 1

    def opcode_2(self, args):
        self.program[self.p2mem(args[2])] = self.p2v(args[0]) * self.p2v(args[1])
        self.pointer += len(args) + 1

    def opcode_3(self, args):
        self.program[self.p2mem(args[0])] = self.inp
        self.pointer += len(args) + 1
        self.inp = None

    def opcode_4(self, args):
        self.outp.append(self.p2v(args[0]))
        self.pointer += len(args) + 1

    def opcode_5(self, args):
        if self.p2v(args[0]) != 0:
            self.pointer = self.p2v(args[1])
        else:
            self.pointer += len(args) + 1

    def opcode_6(self, args):
        if self.p2v(args[0]) == 0:
            self.pointer = self.p2v(args[1])
        else:
            self.pointer += len(args) + 1

    def opcode_7(self, args):
        self.program[self.p2mem(args[2])] = 1 if self.p2v(args[0]) < self.p2v(args[1]) else 0
        self.pointer += len(args) + 1

    def opcode_8(self, args):
        self.program[self.p2mem(args[2])] = 1 if self.p2v(args[0]) == self.p2v(args[1]) else 0
        self.pointer += len(args) + 1

    def opcode_9(self, args):
        self.relative_base += self.p2v(args[0])
        self.pointer += len(args) + 1

    def parse_opcode(self, n):
        if n > 99:
            opcode = int(str(n)[-2:])
            param_modes = [0] * self.expected_params[opcode]
            for i in range(-3, -(len(str(n)) + 1), -1):
                param_modes[abs(i) - 3] = int(str(n)[i])
            return opcode, param_modes
        else:
            return n, [0] * self.expected_params[n]

    def p2v(self, param):
        try:
            if param[1] == 0:
                return self.program[param[0]]
            elif param[1] == 1:
                return param[0]
            elif param[1] == 2:
                return self.program[self.relative_base + param[0]]
        except KeyError:
            return 0

    def p2mem(self, param):
        mem = param[0] + self.relative_base
        if param[1] == 2 and mem >= 0:
            return mem
        elif param[1] == 0 and param[0] >= 0:
            return param[0]
        else:
            raise AttributeError
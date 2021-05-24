import aoc
import aoc_opcode as opc
import itertools as it
import time


def day_7_part_1(data):
    max_output = 0
    for ph in it.permutations(range(0, 5)):
        output = get_amplified_output(data, ph)
        if max_output < output:
            max_output = output
            max_ph = ph
    return max_output, max_ph


def get_amplified_output(data, ph_in):
    amps = [opc.IntCode(data.copy()) for i in range(5)]
    for ph, amp in zip(ph_in, amps):
        amp.run_opcode(ph)

    amp_inputs = {0: 0}
    loop = -1
    while True:
        loop += 1
        amp = loop % 5
        amps[amp].run_opcode(amp_inputs[loop])
        amp_inputs[loop + 1] = amps[amp].outp
        final_out = amps[amp].outp if amps[amp].outp is not None else final_out
        if all(amp.exit_code for amp in amps):
            return final_out


def day_7_part_2(data):
    max_output = 0
    for ph in it.permutations(range(5, 10)):
        output = get_amplified_output(data, ph)
        if max_output < output:
            max_output = output
            max_ph = ph
    return max_output, max_ph


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_7_data.txt")
    # print(day_7_part_1(data))
    print(day_7_part_2(data))
    print(time.time() - t0)
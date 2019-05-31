import sys
import os


def all_instrumets(lines):
    instruments = []
    for each in lines:  # get every insruments
        if each[0] != "|":
            instruments.append(each.strip())
    return instruments


def times(lines, instruments_times):
    i = -1
    for each in lines:
        if each[0] != "|":
            i = i + 1
        else:
            instruments_times[i] += 1
    return instruments_times


def all_period(lines):
    period = []
    for each in lines:  # get every insruments
        if each[0] == "|":
            period.append(each.strip().replace("|", ""))
    return period


def printer(instrument_l, command, instrument):
    if command != "--total":
        print(instrument + ":")
    else:
        print("Total:")
    # ---------deal with the matrix printer---------
    # find the rows of printer
    max = 0
    min = 0
    for each in instrument_l[1:]:
        if int(each) > max:
            max = int(each)
        if int(each) < min:
            min = int(each)
    printer_lines = max - min + 1

    # create a matrix called printer
    printer = [[] for each in range(printer_lines)]
    symbol = " "
    row = max
    for i in range(printer_lines):
        printer[i].append(symbol + str(row))
        printer[i].append(":")
        if row == 0:
            symbol = ""
        row -= 1

    # find the correct form of printer
    for i in range(len(instrument_l)):
        if instrument_l[i] == "\t":
            for every in printer:
                every.append("\t")
        elif instrument_l[i - 1] != "\t" \
                and abs(int(instrument_l[i]) -
                        int(instrument_l[i - 1])
                        ) > 1:
            if int(instrument_l[i - 1]) >\
               int(instrument_l[i]):
                for every in printer:
                    if int(instrument_l[i]) <= int(every[0]) <\
                       int(instrument_l[i - 1]):
                        every.append("*")
                    else:
                        every.append(" ")
            elif int(instrument_l[i - 1]) < int(instrument_l[i]):
                for every in printer:
                    if int(instrument_l[i]) >= int(every[0]) >\
                       int(instrument_l[i - 1]):
                        every.append("*")
                    else:
                        every.append(" ")
        else:
            for every in printer:
                if int(every[0]) == int(instrument_l[i]):
                    every.append("*")
                else:
                    every.append(" ")
        i += 1
    # delete the space behind the last "*"
    for each in printer:
        print(("".join(each)).replace("*", character_flag))


def handle_wave(instruments, instruments_times, period, command):
    period_time = 0
    position = 0  # position is the instruments' position
    l = [[]for each in range(len(instruments))]
    for instrument in instruments:
        if os.path.isfile("./instruments/" + instrument):
            # find the length of instrument_l
            if command[3] == "--total":
                max_len = 0
                for each in period:
                    if len(each) + 1 > max_len:
                        max_len = len(each) + 1
            else:
                max_len = len(period[period_time]) + 1
            # transfer the wave to a list called instrument_l
            instrument_l = ["0"] * max_len
            instrument_l[0] = "\t"
            while instruments_times[position] > 0:
                # get the final instrument_l
                with open("./instruments/" + instrument, "r") as f:
                    wave = f.readlines()
                    for i in range(len(wave)):  # delete and transfer
                        if wave[i][0] == "-":
                            wave[i] = wave[i][1:]
                        wave[i] = wave[i].strip()
                        wave[i] = wave[i][0] + \
                            wave[i][1:].replace("-", "*")
                        wave[i] = wave[i].replace("/", "*")
                        wave[i] = wave[i].replace("\\", "*")
                        for every in wave:
                            if every[0] == "0":
                                max_wave = len(every) - 1
                    j = 2  # this is the pointer of the wave
                    p = 1  # this is the pointer of the instrument_l
                    # use the note in a period to scan the wave
                    for note in period[period_time]:
                        if note == "*":
                            symbol = " "
                            for i in range(len(wave)):
                                if len(wave[i]) > j and p < len(instrument_l):
                                    if wave[i][j] == "*":
                                        instrument_l[p] = str(
                                            int(instrument_l[p]) +
                                            int(symbol + wave[i][0])
                                            )
                                    if wave[i][0] == "0":
                                        symbol = "-"
                            j += 1
                            p += 1
                        else:
                            j = 2  # back to the start of the wave
                            p += 1
                        if j > max_wave:
                            j = j - max_wave + 1
                    l[position] = instrument_l
                instruments_times[position] -= 1
                period_time += 1
            if command[3] != "--total":
                printer(instrument_l, command[3], instrument)
            position += 1
        else:
            print("Unknown source.")
    if command[3] == "--total":
        new_len = 0
        for sub in l:
            if len(sub) >= new_len:
                new_len = len(sub)
        instrument_l_new = ["0"]*new_len
        instrument_l_new[0] = "\t"

        for sub in l:
            i = 1
            for every in sub[1:]:
                instrument_l_new[i] = str(int(instrument_l_new[i]) +
                                          int(every)
                                          )
                i = i + 1

        printer(instrument_l_new, command[3], instrument)


if len(sys.argv) > 1:
    command = [""]*4  # get the correct order of sys.argv
    for each in sys.argv:
        if ".py" in each:
            command[0] = each
        elif "--character" in each:
            command[2] = each
        elif "--total" in each:
            command[3] = each
        else:
            command[1] = each

    character_flag = "*"
    if command[2] != "":
        character_flag = command[2][12]

    if(os.path.isfile(command[1])):  # Invalid path to score file.
        with open(command[1], "r") as score:
            lines = score.readlines()
            instruments = all_instrumets(lines)
            instruments_times = [0] * len(instruments)
            instruments_times = times(lines, instruments_times)
            period = all_period(lines)
            handle_wave(instruments, instruments_times, period, command)
    elif command[1] == "":
        print("No score file specified.")
    else:
        print("Invalid path to score file.")
else:
    print("No score file specified.")


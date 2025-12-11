from functools import cache

with open("data","r") as file:
    data = file.read().split("\n")

devices = {}

for line in data:
    line = line.split(": ")
    devices[line[0]] = line[1].split(" ")


@cache
def p(start_key, end_key, seen_fft = False, seen_dac = False):
    found_n = 0
    if start_key == "fft":
        seen_fft = True
    if start_key == "dac":
        seen_dac = True
    if start_key != end_key:
        for i in devices.get(start_key,[]):
            found_n += p(i, end_key, seen_fft, seen_dac) or 0
        return found_n
    else:
        if seen_fft and seen_dac:
            return 1
        else:
            return 0

print(p("svr","out"))
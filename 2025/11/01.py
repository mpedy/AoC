with open("data","r") as file:
    data = file.read().split("\n")

devices = {}

for line in data:
    line = line.split(": ")
    devices[line[0]] = line[1].split(" ")

print(devices)
found_paths = []
def find_exit(visited = [], start_key = "svr", end_key = "fft"):
    if start_key != end_key:
        for i in devices[start_key]:
            if i != "out":
                find_exit([*visited, i], i)
    else:
        found_paths.append(visited)

find_exit()
print(found_paths,"\nLength: ", len(found_paths))
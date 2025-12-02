import re

try:
    with open("01/input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("input.txt", "r") as file:
        data = file.read()

data = data.split("\n")

result = 0
for i in data:
    numbers = re.sub("[^0-9]*","",i)
    numbers = int(numbers[0]+numbers[-1])
    result += numbers

print(result)
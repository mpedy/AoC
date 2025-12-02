import re

try:
    with open("2023/01/input.txt", "r") as file:
        data = file.read()
except Exception:
    with open("input.txt", "r") as file:
        data = file.read()

data = data.split("\n")

result = 0
result_list = []
for i in data:
    result_numbers = []
    numbers = i
    index=-1
    while index < len(numbers)-1:
        index += 1
        for j in [["one",1],["two",2],["three",3],["four",4],["five",5],["six",6],["seven",7],["eight",8],["nine",9]]:
            if numbers[index] in ["0","1","2","3","4","5","6","7","8","9"]:
                result_numbers.append(int(numbers[index]))
                break
            elif numbers[index:].startswith(str(j[0])):
                result_numbers.append(j[1])
                break
    print(result_numbers)
    result_list.append(f"{result_numbers[0]}{result_numbers[-1]}")
    result_numbers = int(str(result_numbers[0])+str(result_numbers[-1]))
    result += result_numbers

print(result)
with open("testmio","w") as f:
    for i in result_list:
        f.write(i[0])
        f.write(" ")
        f.write(i[1])
        f.write("\n")
from day16 import dijkstra, Direction
import sys


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print(f'Usage: {sys.argv[0]} <map.txt>')
            raise Exception("")
            sys.exit(1)

        with open(sys.argv[1]) as f:
            maze = f.read().strip().split('\n')
    except Exception:
        with open("2024/16/test_input.txt") as f:
            maze = f.read().strip().split('\n')

    height = len(maze)
    width = len(maze[0])

    dist, path = dijkstra(maze, width, height)

    matrix = []
    for y in range(height):
        res = [" " if maze[y][x]=="." else "#" for x in range(width)]
        matrix.append(res)
    
    for k in path.keys():
        if path[k] is not None:
            matrix[k[0]][k[1]] = "."
    res = []
    for j in range(len(matrix)):
        res.append(" ".join([str(i) for i in matrix[j]]))
        res = matrix[j]
        print(" ".join(res))
        #for row in res:
        #    print(row)
        #    row = row.split(" ")
            #print(" ".join(f"{str(item)}" for item in row))

    score1 = dist[(width - 2, 1, Direction.EAST)]
    score2 = dist[(width - 2, 1, Direction.NORTH)]

    min_score = score1 if score1 < score2 else score2
    print(f'Lowest score a Reindeer could get: {min_score}')
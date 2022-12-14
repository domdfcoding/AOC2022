"""
The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?
"""

# stdlib
import copy
import itertools
import sys

# 3rd party
from domdf_python_tools.paths import PathPlus

# Read input file
cave = PathPlus("input.txt").read_text().strip().split('\n')
cave = PathPlus("example.txt").read_text().strip().split('\n')

# Parse rock layout
routes = []

x_min = sys.maxsize
x_max = 0

y_min = 0
y_max = 0

for row in cave:
	points = [tuple(map(int, x.split(','))) for x in row.split(" -> ")]
	# print(points)
	routes.append(points)
	for point in points:
		x_min = min(x_min, point[0])
		x_max = max(x_max, point[0])

		y_min = min(y_min, point[1])
		y_max = max(y_max, point[1])

cave_layout = []
for i in range(y_max - y_min + 1):
	row = ['.'] * (x_max - x_min + 1)
	cave_layout.append(row)

for path in routes:
	for idx in range(len(path) - 1):
		start, stop = path[idx], path[idx + 1]

		start_x, start_y = start
		stop_x, stop_y = stop
		start_x, stop_x = sorted((start_x, stop_x))
		start_y, stop_y = sorted((start_y, stop_y))

		for x in range(start_x, stop_x + 1):
			x -= x_min
			for y in range(start_y, stop_y + 1):
				y -= y_min
				cave_layout[y][x] = '#'


def print_cave():

	headers = []

	for i in range(x_min, x_max + 1):
		if i % 2:
			headers.append("   ")
		else:
			headers.append(reversed(str(i)))

	for row in reversed(list(map(list, itertools.zip_longest(*headers, fillvalue=' ')))):
		print(' ', ''.join(row))

	for row_idx, row in enumerate(cave_layout):
		print(row_idx + y_min, ''.join(map(str, row)))


print_cave()

sand_origin = (500, 0)
# print([row[sand_origin[0] - x_min] for row in cave_layout])


def simulate():
	iteration = 0
	while True:
		iteration += 1
		print("\n=============")
		print("Sand No.", iteration)
		print("=============")

		# Introduce a new grain of sand
		sand_position = list(sand_origin)
		sand_position[0] -= x_min
		sand_position[1] -= y_min

		while True:
			if sand_position[1] > len(cave_layout):
				print("Sand falls into endless void")
				return iteration

			# Can we move down?
			object_below = cave_layout[sand_position[1] + 1][sand_position[0]]
			# print(f"{object_below=}")
			if object_below == '.':
				# Yep
				sand_position[1] += 1
				continue

			# Nope. Can we move down and left?
			if sand_position[0] > 0:
				object_below_left = cave_layout[sand_position[1] + 1][sand_position[0] - 1]
				# print(f"{object_below_left=}")
				if object_below_left == '.':
					# Yep
					sand_position[1] += 1
					sand_position[0] -= 1
					continue
			else:
				print("Against left edge")
				print("Sand falls into endless void")
				return iteration

			# Nope. Can we move down and right?
			if sand_position[0] < len(cave_layout[0]):
				object_below_right = cave_layout[sand_position[1] + 1][sand_position[0] + 1]
				# print(f"{object_below_right=}")
				if object_below_right == '.':
					# Yep
					sand_position[1] += 1
					sand_position[0] += 1
					continue
			else:
				print("Against right edge")
				print("Sand falls into endless void")
				return iteration

			# Nope. Sand comes to rest.
			cave_layout[sand_position[1]][sand_position[0]] = 'o'
			break

		print_cave()
		# input(">")
		# stdlib
		import time
		time.sleep(0.1)


sand_count = simulate() - 1  # The last grain didn't come to rest
print(sand_count, "grains of sand came to rest.")  # 578

# === Part 2 ===
"""
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->

To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################

Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
"""

# Parse rock layout
routes = []

x_min = sys.maxsize
x_max = 0

y_min = 0
y_max = 0

for row in cave:
	points = [tuple(map(int, x.split(','))) for x in row.split(" -> ")]
	# print(points)
	routes.append(points)
	for point in points:
		x_min = min(x_min, point[0])
		x_max = max(x_max, point[0])

		y_min = min(y_min, point[1])
		y_max = max(y_max, point[1])

x_min = max(0, x_min - 300)
x_max += 300

cave_layout = []
for i in range(y_max - y_min + 1):
	row = ['.'] * (x_max - x_min + 1)
	cave_layout.append(row)

for path in routes:
	for idx in range(len(path) - 1):
		start, stop = path[idx], path[idx + 1]

		start_x, start_y = start
		stop_x, stop_y = stop
		start_x, stop_x = sorted((start_x, stop_x))
		start_y, stop_y = sorted((start_y, stop_y))

		for x in range(start_x, stop_x + 1):
			x -= x_min
			for y in range(start_y, stop_y + 1):
				y -= y_min
				cave_layout[y][x] = '#'

cave_layout.append(['.'] * (x_max - x_min))
cave_layout.append(['#'] * (x_max - x_min))

print_cave()

sand_target = [sand_origin[0] - x_min, sand_origin[1] - y_min]


def simulate_p2():
	iteration = 0
	while True:
		iteration += 1
		print("\n=============")
		print("Sand No.", iteration)
		print("=============")

		# Introduce a new grain of sand
		sand_position = list(sand_origin)
		sand_position[0] -= x_min
		sand_position[1] -= y_min

		while True:
			if sand_position[1] == len(cave_layout):
				# On the floor. Sand comes to rest.
				cave_layout[sand_position[1]][sand_position[0]] = 'o'
				break

			# if sand_position[1] > len(cave_layout):
			# 	print("Sand falls into endless void")
			# 	return iteration

			# Can we move down?
			object_below = cave_layout[sand_position[1] + 1][sand_position[0]]
			# print(f"{object_below=}")
			if object_below == '.':
				# Yep
				sand_position[1] += 1
				continue

			# Nope. Can we move down and left?
			object_below_left = cave_layout[sand_position[1] + 1][sand_position[0] - 1]
			# print(f"{object_below_left=}")
			if object_below_left == '.':
				# Yep
				sand_position[1] += 1
				sand_position[0] -= 1
				continue

			# Nope. Can we move down and right?
			object_below_right = cave_layout[sand_position[1] + 1][sand_position[0] + 1]
			# print(f"{object_below_right=}")
			if object_below_right == '.':
				# Yep
				sand_position[1] += 1
				sand_position[0] += 1
				continue

			# Nope. Sand comes to rest.
			cave_layout[sand_position[1]][sand_position[0]] = 'o'

			print(sand_position)
			if sand_position == sand_target:
				return iteration
			break

		# if iteration % 100 == 0:
		# 	print_cave()
		# 	input(">")
		# 	import time
		# 	time.sleep(0.05)


sand_count = simulate_p2()
print(sand_count, "grains of sand came to rest.")  # 24377

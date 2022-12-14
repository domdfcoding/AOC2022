"""
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
"""

# stdlib
import operator
import pprint
import re
import string

# 3rd party
from domdf_python_tools.paths import PathPlus

# Read input file
# heightmap = list(map(list, PathPlus("input.txt").read_text().strip().split('\n')))
heightmap = list(map(list, PathPlus("example.txt").read_text().strip().split('\n')))

ELEVATION_RANGE = string.ascii_lowercase
CURRENT_POSITION = 'S'
TARGET_POSITION = 'E'

#                  row, col
current_position = [-1, -1]

for row_idx, row in enumerate(heightmap):
	print(row_idx, row)
	# if CURRENT_POSITION in row:
	# 	current_position = [row_idx, row.index(CURRENT_POSITION)]
	if TARGET_POSITION in row:
		current_position = [row_idx, row.index(TARGET_POSITION)]

print(current_position)
# assert heightmap[current_position[0]][current_position[1]] == CURRENT_POSITION, (current_position, heightmap[current_position[0]][current_position[1]])
assert heightmap[current_position[0]
					][current_position[1]
					] == TARGET_POSITION, (current_position, heightmap[current_position[0]][current_position[1]])
current_elevation = 0

possible_moves_from_here = []

# # Up?
# if current_position[0] > 0:
# 	# Not at top of map
# 	up_height = ELEVATION_RANGE.index(heightmap[current_position[0]-1][current_position[1]])
# 	if up_height in {current_elevation, current_elevation + 1, current_elevation - 1}:
# 		print(f"Can move up (elevation {up_height})")

# # Down?
# if current_position[0] < len(heightmap):
# 	# Not at bottom of map
# 	down_height = ELEVATION_RANGE.index(heightmap[current_position[0]+1][current_position[1]])
# 	if down_height in {current_elevation, current_elevation + 1, current_elevation - 1}:
# 		print(f"Can move down (elevation {down_height})")

# # Left?
# if current_position[1] > 0:
# 	# Not at left edge of map
# 	left_height = ELEVATION_RANGE.index(heightmap[current_position[0]][current_position[1]-1])
# 	if left_height in {current_elevation, current_elevation + 1, current_elevation - 1}:
# 		print(f"Can move left (elevation {left_height})")

# # Right?
# if current_position[1] < len(heightmap[0]):
# 	# Not at right edge of map
# 	right_height = ELEVATION_RANGE.index(heightmap[current_position[0]][current_position[1]+1])
# 	if right_height in {current_elevation, current_elevation + 1, current_elevation - 1}:
# 		print(f"Can move right (elevation {right_height})")

# Find interfaces

boundaries = []

for row_idx, row in enumerate(heightmap):
	boundaries.append([])
	for col_idx, col in enumerate(row):
		up_cell = down_cell = left_cell = right_cell = ' '
		if row_idx > 0:
			# Look up
			up_cell = heightmap[row_idx - 1][col_idx]
		if row_idx < len(heightmap) - 1:
			# Look down
			down_cell = heightmap[row_idx + 1][col_idx]

		if col_idx > 0:
			# Look left
			left_cell = heightmap[row_idx][col_idx - 1]
		if col_idx < len(row) - 1:
			# Look right
			right_cell = heightmap[row_idx][col_idx + 1]

		neighbouring_cells = {up_cell, down_cell, left_cell, right_cell}
		if 'S' in neighbouring_cells:
			neighbouring_cells.remove('S')
			neighbouring_cells.add('a')
		boundaries[-1].append(''.join(sorted(neighbouring_cells)).rjust(4))

for row in boundaries:
	print(row)

# Find boundaries between E/z and y
zy_boundaries = []

for row_idx, row in enumerate(boundaries):
	for col_idx, col in enumerate(row):
		height = heightmap[row_idx][col_idx]
		if 'y' in col and height in "Ez":
			zy_boundaries.append((row_idx, col_idx))

print(zy_boundaries)

height_boundaries = {}

for idx in range(2, 25):
	origin = ELEVATION_RANGE[-idx]
	dest = ELEVATION_RANGE[-idx - 1]
	print(origin, dest)

	# Find boundaries between origin and dest
	origin_dest_boundaries = height_boundaries[(origin, dest)] = []

	for row_idx, row in enumerate(boundaries):
		for col_idx, col in enumerate(row):
			height = heightmap[row_idx][col_idx]
			if dest in col and height == origin:
				origin_dest_boundaries.append((row_idx, col_idx))

pprint.pprint(height_boundaries)


def get_neighbouring_coordinates():
	return {(current_position[0] - 1, current_position[1]), (current_position[0] + 1, current_position[1]),
			(current_position[0], current_position[1] - 1), (current_position[0], current_position[1] + 1)}


route = [current_position]
print("Start at", current_position)
# Get to any zy boundary
print(zy_boundaries)
if len(zy_boundaries) == 1:
	target = zy_boundaries[0]
else:
	raise NotImplementedError

# Is target next to us?
if target in get_neighbouring_coordinates():
	route.append(target)
	current_position = target
else:
	raise NotImplementedError

# Get to any subsequent boundaries
for idx in range(2, 25):
	origin = ELEVATION_RANGE[-idx]
	dest = ELEVATION_RANGE[-idx - 1]
	print((origin, dest), height_boundaries[(origin, dest)])

	# Get to any zy boundary
	print(height_boundaries[(origin, dest)])
	if len(height_boundaries[(origin, dest)]) == 1:
		target = height_boundaries[(origin, dest)][0]
	else:
		raise NotImplementedError("Multiple boundaries")

	# Is target next to us?
	if target in get_neighbouring_coordinates():
		route.append(target)
		current_position = target
	else:
		# Need to get from current position to target within <origin> letter
		raise NotImplementedError("Gap")

"""
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
    The top-middle 5 is visible from the top and right.
    The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
    The left-middle 5 is visible, but only from the right.
    The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
    The right-middle 3 is visible from the right.
    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
"""

# 3rd party
from domdf_python_tools.paths import PathPlus

# Read input file
trees = [list(map(int, row)) for row in PathPlus("input.txt").read_text().strip().split('\n')]
# trees = [list(map(int, row)) for row in PathPlus("example.txt").read_text().strip().split("\n")]

# print(trees)

vis_from_left = '>'
vis_from_right = '<'
vis_from_top = 'v'
vis_from_bottom = '^'
vis_from_mutliple = '#'

left_right_visibility = []

for row in trees:
	visibility = []

	# Looking from left
	tallest_from_left = -1

	for tree in row:
		if tree > tallest_from_left:
			# Visible, and new tallest
			visibility.append(vis_from_left)
			tallest_from_left = tree
		else:
			# Obscured
			visibility.append(' ')

	# Looking from right
	tallest_from_right = -1

	for idx, tree in reversed(list(enumerate(row))):
		if tree > tallest_from_right:
			# Visible, and new tallest
			if visibility[idx] == vis_from_left:
				visibility[idx] = vis_from_mutliple
			else:
				visibility[idx] = vis_from_right

			tallest_from_right = tree

	left_right_visibility.append(visibility)

top_bottom_visibility = []

# Rotated 90° clockwise
for row in zip(*reversed(trees)):
	visibility = []

	# Looking from top
	tallest_from_top = -1

	for tree in row:
		if tree > tallest_from_top:
			# Visible, and new tallest
			visibility.append(vis_from_top)
			tallest_from_top = tree
		else:
			# Obscured
			visibility.append(' ')

	# Looking from bottom
	tallest_from_bottom = -1

	for idx, tree in reversed(list(enumerate(row))):
		if tree > tallest_from_bottom:
			# Visible, and new tallest
			if visibility[idx] == vis_from_top:
				visibility[idx] = vis_from_mutliple
			else:
				visibility[idx] = vis_from_bottom

			tallest_from_bottom = tree

	top_bottom_visibility.append(visibility)

# Rotate top_bottom_visibility 90° anticlockwise
top_bottom_visibility = reversed(list(map(list, zip(*top_bottom_visibility))))

combined_visibility = []
total_visible_trees = 0

for lr_vis, tb_vis in zip(left_right_visibility, top_bottom_visibility):
	# print(lr_vis, tb_vis)

	visibility = []
	for lr_tree, tb_tree in zip(lr_vis, tb_vis):
		if lr_tree != ' ' or tb_tree != ' ':
			visibility.append('@')
			total_visible_trees += 1
		else:
			visibility.append(' ')

	combined_visibility.append(visibility)

# for line in combined_visibility:
# 	print(line)

print(f"There are {total_visible_trees} trees visible")  # 1715

# === Part 2 ===
"""
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

    Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
"""

print()

left_right_visibility = []

for row in trees:
	visibility = []

	# Looking from left

	for idx, tree in enumerate(row):
		trees_to_left = tuple(reversed([t for t in row[:idx]]))

		# Number of trees shorter than this tree, looking left
		visible_trees_left = 0

		for t in trees_to_left:
			if t < tree:
				visible_trees_left += 1
			else:
				visible_trees_left += 1
				break

		visibility.append(visible_trees_left)

	# Looking from right
	tallest_from_right = -1

	for idx, tree in enumerate(row):
		trees_to_right = tuple([t for t in row[idx + 1:]])

		# Number of trees shorter than this tree, looking right
		visible_trees_right = 0

		for t in trees_to_right:
			if t < tree:
				visible_trees_right += 1
			else:
				visible_trees_right += 1
				break

		visibility[idx] *= visible_trees_right

	left_right_visibility.append(visibility)

top_bottom_visibility = []

# Rotated 90° clockwise
for row in zip(*reversed(trees)):
	visibility = []

	# Looking from top

	for idx, tree in enumerate(row):
		trees_to_top = tuple(reversed([t for t in row[:idx]]))

		# Number of trees shorter than this tree, looking top
		visible_trees_top = 0

		for t in trees_to_top:
			if t < tree:
				visible_trees_top += 1
			else:
				visible_trees_top += 1
				break

		visibility.append(visible_trees_top)

	# Looking from bottom
	tallest_from_bottom = -1

	for idx, tree in enumerate(row):
		trees_to_bottom = tuple([t for t in row[idx + 1:]])

		# Number of trees shorter than this tree, looking bottom
		visible_trees_bottom = 0

		for t in trees_to_bottom:
			if t < tree:
				visible_trees_bottom += 1
			else:
				visible_trees_bottom += 1
				break

		visibility[idx] *= visible_trees_bottom

	top_bottom_visibility.append(visibility)

# Rotate top_bottom_visibility 90° anticlockwise
top_bottom_visibility = reversed(list(map(list, zip(*top_bottom_visibility))))

combined_visibility = []

for lr_vis, tb_vis in zip(left_right_visibility, top_bottom_visibility):

	visibility = []
	for lr_tree, tb_tree in zip(lr_vis, tb_vis):
		visibility.append(lr_tree * tb_tree)

	combined_visibility.append(visibility)

# print()
# for line in combined_visibility:
# 	print(line)

row_maxima = [max(row) for row in combined_visibility]
print("The highest possible scenic score is:", max(row_maxima))  # 374400

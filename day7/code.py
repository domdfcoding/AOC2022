"""
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
        cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
        cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
"""

# stdlib
import pprint
from collections import defaultdict, deque
from functools import reduce
from operator import itemgetter

# 3rd party
from domdf_python_tools.paths import PathPlus

# Read input file
command_history = PathPlus("input.txt").read_text().strip().split("$ ")
# command_history = PathPlus("example.txt").read_text().strip().split("$ ")

cwd = deque()
# filesystem = defaultdict(defaultdict_dict)  # Keys are files or directories. Values are size (for files) or a map (for directories)
filesystem = {}  # Keys are files or directories. Values are size (for files) or a map (for directories)

unique_paths = []


def getitem(dictionary, key):
	if key not in dictionary:
		dictionary[key] = {}

	return dictionary[key]


for line in command_history:
	if not line:
		continue

	# print(repr(f"$ {line}"))
	command, output = line.split('\n', 1)
	# print(f"$ {command}")
	# print(output)

	op, *args = command.split(' ')

	# print(op, args)
	# print(output)

	if op == "cd":
		assert len(args) == 1
		if args[0] == "..":
			cwd.pop()
		else:
			cwd.append(args[0])

	elif op == "ls":
		assert not args

		for entry in output.rstrip().split('\n'):
			dir_or_size: str
			dir_or_size, name = entry.split(' ', 1)
			if dir_or_size == "dir":
				unique_paths.append((*cwd, name))
				reduce(getitem, [filesystem, *cwd])[name] = {}
			else:
				assert dir_or_size.isdigit()
				reduce(getitem, [filesystem, *cwd])[name] = int(dir_or_size)

	# print("cwd:", list(cwd))
	# print(dict(filesystem))
	# input(">")

# pprint.pprint(dict(filesystem))

directory_sizes = {}


def flatten(xs):
	for x in xs.values():
		if isinstance(x, dict):
			yield from flatten(x)
		else:
			yield x


# for p in unique_paths:
# 	print(p)

# exit()

directory_sizes['/'] = sum(flatten(reduce(getitem, [filesystem, '/'])))

for path in unique_paths:
	# print(reduce(getitem, [filesystem, *path]))
	# print(list(flatten(reduce(getitem, [filesystem, *path]))))
	# print(sum(flatten(reduce(getitem, [filesystem, *path]))))
	directory_sizes[path] = sum(flatten(reduce(getitem, [filesystem, *path])))

sum_of_small_directories = sum(v for v in directory_sizes.values() if v <= 100000)  # 1743217
print("The total size of all directories under 10000 is", sum_of_small_directories)
"""
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

    Delete directory e, which would increase unused space by 584.
    Delete directory a, which would increase unused space by 94853.
    Delete directory d, which would increase unused space by 24933642.
    Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
"""

print()

disk_size = 70000000
required_space = 30000000
space_used = directory_sizes['/']
space_free = disk_size - space_used
space_to_free = required_space - space_free

print(f"Space Available: {space_free:>8}")
print(f"Space Required:  {required_space:>8}")
print(f"Need an extra:   {space_to_free:>8}")

# Find directories which are at least <space_to_free> in size
candidates_for_deletion = {v: k for k, v in directory_sizes.items() if v >= space_to_free}

print("The following directory can be deleted to free up the required space:")
print(sorted(candidates_for_deletion.items(), key=itemgetter(0))[0])  # 8319096

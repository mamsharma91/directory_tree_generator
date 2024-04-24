import argparse
import sys
import pathlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default="./dirtree",
        help="Generate a full directory tree starting at ROOT_DIR",
    )
    args = parser.parse_args()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit()
    tree = DirectoryTree(root_dir)
    tree.generate_tree()

PIPE = "│"
BRANCH = "├──"
PIPE_PREFIX = "│   "

class DirectoryTree:
    def __init__(self, root_dir):
        self._generator = _TreeGenerator(root_dir)

    def generate_tree(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)

class _TreeGenerator:
    def __init__(self, root_dir):
        self._root_dir = pathlib.Path(root_dir)
        self._tree = []

    def build_tree(self):
        self._tree.append(f"{self._root_dir}")
        self._tree.append(PIPE)
        self._create_tree(self._root_dir)
        return self._tree

    def _create_tree(self, directory, prefix=""):
        entries = directory.iterdir()
        for entry in entries:
            if entry.is_dir():
                self._add_directory(entry, prefix)
            else:
                self._add_file(entry, prefix)

    def _add_directory(self, directory, prefix):
        self._tree.append(f"{prefix}{BRANCH} {directory.name}")
        prefix += PIPE_PREFIX
        self._create_tree( directory, prefix)
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix):
        self._tree.append(f"{prefix}{BRANCH} {file.name}")

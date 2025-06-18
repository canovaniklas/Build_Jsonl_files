#!/usr/bin/env python3
"""
compare_dirs.py  <folder_A>  <folder_B>

Example:
    python compare_dirs.py  "/path/to/folder1"  "/path/to/folder2"
"""
import sys
from pathlib import Path

def main(dir_a: Path, dir_b: Path) -> None:
    # 1. collect all regular-file *names* (not sub-folder contents)
    files_a = {p.name for p in dir_a.iterdir() if p.is_file()}
    files_b = {p.name for p in dir_b.iterdir() if p.is_file()}

    only_in_a = files_a - files_b
    only_in_b = files_b - files_a

    print(f"\n► Files only in {dir_a}:")
    if only_in_a:
        for f in sorted(only_in_a):
            print("   ", f)
                
    else:
        print("   (none)")

    print(f"\n► Files only in {dir_b}:")
    if only_in_b:
        for f in sorted(only_in_b):
            print("   ", f)
    else:
        print("   (none)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: compare_dirs.py <folder_A> <folder_B>")

    a, b = map(Path, sys.argv[1:])
    if not (a.is_dir() and b.is_dir()):
        sys.exit("Both arguments must be existing folders.")

    main(a.resolve(), b.resolve())

#!/usr/bin/env python

import os
import sys


def has_fstrings():
    """
    This function verifies whether f-strings are natively supported
    """
    try:
        return eval('f"hi"') == 'hi'
        return True
    except SyntaxError:
        return False


def has_future_fstrings():
    """
    This function verifies whether 'future_fstrings' is installed
    """
    try:
        import future_fstrings
        return True
    except ModuleNotFoundError:
        return False


def add_ffstrings_encoding(src, dst):
    """
    This function will copy recursively Python files from <src> to <dst>.
    The "future_fstrings" coding will be prepended to the files, if needed.

    :param src: the source path
    :param dst: the destination path
    """
    has_fs = has_fstrings()
    has_ffs = has_future_fstrings()

    if not (has_fs or has_ffs):
        raise RuntimeError(
            "This Python version does not natively support f-strings, and "
            "future_fstrings is not installed.")

    for root, dirs, files in os.walk(src):
        if root.endswith("__pycache__") or root.endswith(".egg-info"):
            continue

        dst_dir = root.replace(src, dst)
        os.makedirs(dst_dir, exist_ok=True)

        for filename in files:
            if not filename.endswith(".py"):
                continue

            src_file = os.path.join(root, filename)
            dst_file = os.path.join(dst_dir, filename)

            with open(src_file) as f1, open(dst_file, mode='w') as f2:
                content = f1.read()
                if content and not has_fs:
                    # Only for non-empty files and if f-strings are unsupported
                    f2.write("# -*- coding: future_fstrings -*-\n\n")
                f2.write(content)


if __name__ == "__main__":
    # execute only if run as a script
    add_ffstrings_encoding(*sys.argv[1:])

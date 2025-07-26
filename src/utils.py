import sys


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

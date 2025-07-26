import argparse
import sys
import time

import git
from commit_mirage import CommitMirage
from utils import print_err

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Commit Mirage")
    parser.add_argument("dir", help="Working dir.", default=".")
    parser.add_argument("-s", "--start", type=int, help="Start time for generated commits.")
    parser.add_argument("-e", "--end", type=int, help="End time for generated commits.")
    parser.add_argument("-t", "--times", type=int, help="How many commits to generate.", default=4)
    parser.add_argument("-c", "--commit", type=str, help="Generate commits after this.")
    parser.add_argument("-p", "--provider", choices=["anthropic", "openai"], default="anthropic")
    parser.add_argument("-b", "--base-url", type=str)
    parser.add_argument("-a", "--api-key", type=str)
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    opts = {
        "dir": args.dir,
        "debug": args.debug,
        "commit": args.commit,
        "times": args.times,
        "provider": args.provider,
        "base_url": args.base_url,
        "api_key": args.api_key
    }

    if args.start is None:
        if opts["commit"] is None:
            opts["start"] = int(git.get_head_time(opts["dir"]))
        else:
            opts["start"] = int(git.get_commit_time(opts["commit"], opts["dir"]))
    else:
        opts["start"] = args.start

    if args.end is None:
        opts["end"] = int(time.time())
    else:
        opts["end"] = args.end

    if opts["end"] < opts["start"]:
        print_err("End time should not be earlier than start time.")
        sys.exit(1)

    if opts["times"] < 3:
        print_err("Generate times must be 3 or larger.")
        sys.exit(2)

    generator = CommitMirage(opts)
    generator.run()

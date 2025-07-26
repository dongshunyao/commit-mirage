from random import randrange
from datetime import datetime


from commit_manager import CommitManager

from src.codebase_analyzer import CodebaseAnalyzer
from src.llm_refactorer import LLMRefactorer

from src.utils import printerr

TEMP_BRANCH_NAME = "cmtemp"

class CommitMirage:
    def __init__(self, opts):
        self.opts = opts

    def printdebug(self, *args, **kwargs):
        if self.opts["debug"]:
            printerr(*args, **kwargs)

    def get_random_times(self):
        delta = self.opts["end"] - self.opts["start"]
        interval = delta // (self.opts["times"] + 1)
        results = []
        for i in range(1, self.opts["times"] + 1):
            results.append(self.opts["start"] + i * interval + randrange(-interval, interval))
        return results

    def run(self):
        branch = None
        current = None
        if git.check_dirty(self.opts["dir"]):
            printerr("This program only works with a clean work dir.")
            sys.exit(3)
        if self.opts["commit"] != None:
            branch = git.get_branch_name(self.opts["dir"])
            self.printdebug(f"branch name: {branch}")
            git.new_branch(TEMP_BRANCH_NAME, self.opts["commit"], self.opts["dir"])
        randomTimes = self.get_random_times()
        for t in randomTimes:
            # message = modify_work_space()
            # git.add_all(self.opts["dir"])
            # git.commit_with_time(message, t, self.opts["dir"])
            # current = git.get_head_hash(self.opts["dir"])
            self.printdebug(f"{t} {datetime.fromtimestamp(t).isoformat()}")
        # TODO: Check final state and may add revert.
        if self.opts["commit"] != None:
            git.rebase(TEMP_BRANCH_NAME, branch, self.opts["dir"])
            git.checkout(branch, self.opts["dir"])
            git.deleteBranch(TEMP_BRANCH_NAME, self.opts["dir"])

        return current

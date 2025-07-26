import sys
from pathlib import Path
from datetime import datetime
from random import randrange

from src import git
from src.codebase_analyzer import CodebaseAnalyzer
from src.llm_refactorer import LLMRefactorer
from src.utils import printerr

TEMP_BRANCH_NAME = "cmtemp"


class CommitMirage:
    def __init__(self, opts):
        self.opts = opts
        llm_config = {
            "provider": self.opts["provider"],
            "base_url": self.opts["base_url"],
            "api_key": self.opts["api_key"]
        }
        self.analyzer = CodebaseAnalyzer(llm_config)
        self.refactorer = LLMRefactorer(llm_config)

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
        codebase_summary = self.analyzer.analyze_repository(self.opts["dir"])
        target_files = self.analyzer.select_modification_targets(codebase_summary, commits)
        refactor_plan = self.refactorer.create_refactor_plan(target_files)
        random_times = self.get_random_times()

        if git.check_dirty(self.opts["dir"]):
            printerr("此程序只能在干净的工作目录中运行。")
            sys.exit(3)
        if self.opts["commit"] != None:
            branch = git.get_branch_name(self.opts["dir"])
            self.printdebug(f"branch name: {branch}")
            git.new_branch(TEMP_BRANCH_NAME, self.opts["commit"], self.opts["dir"])
        for i in range(0, len(random_times)):
            t = random_times[i]
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

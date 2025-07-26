import math
import sys
from datetime import datetime
from pathlib import Path
from random import randrange

import git
from codebase_analyzer import CodebaseAnalyzer
from llm_refactorer import LLMRefactorer
from utils import print_err

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

    def print_debug(self, *args, **kwargs):
        if self.opts["debug"]:
            print_err(*args, **kwargs)

    def get_random_times(self):
        delta = self.opts["end"] - self.opts["start"]
        interval = delta // (self.opts["times"] + 1)
        results = []
        for i in range(1, self.opts["times"] + 1):
            results.append(self.opts["start"] + i * interval + randrange(-interval, interval))
        return results

    def run(self):
        if git.check_dirty(self.opts["dir"]):
            print_err("此程序只能在干净的工作目录中运行。")
            sys.exit(3)

        branch = None
        current = None
        self.print_debug("分析仓库……")
        codebase_summary = self.analyzer.analyze_repository(Path(self.opts["dir"]))
        self.print_debug("选择目标……")
        target_files = self.analyzer.select_modification_targets(codebase_summary, self.opts["times"])
        self.print_debug("创建计划……")
        refactor_plan = self.refactorer.create_refactor_plan(target_files, self.opts["dir"])

        # # refactor_plan = ["A+", "A-", "B+", "B-", "C+", "C-", "D+", "D-", "E+", "E-", "F+", "F-", "G+", "G-"]
        # refactor_plan = ["A+", "A-", "B+", "B-", "C+", "C-", "D+", "D-", "E+", "E-", "F+", "F-"]
        # # refactor_plan = ["A+", "A-"]
        # self.opts["times"] = 2

        final_plan = []
        add_plan = []
        delete_plan = []
        for i in range(len(refactor_plan)):
            if i % 2 == 0:
                add_plan.append(refactor_plan[i])
            else:
                delete_plan.append(refactor_plan[i])

        if self.opts["times"] == 2:
            count = len(add_plan) // 2
            final_plan.append([])
            final_plan.append([])
            for i in range(0, count):
                final_plan[0].append(add_plan[i])
                final_plan[0].append(delete_plan[i])
            final_plan[0].append(add_plan[count])
            final_plan[1].append(delete_plan[count])
            for i in range(count + 1, len(add_plan)):
                final_plan[1].append(add_plan[i])
                final_plan[1].append(delete_plan[i])
        else:
            left = len(add_plan) - 1
            count = (left + (left % (self.opts["times"] - 2))) // (self.opts["times"] - 2)
            final_plan.append([add_plan[0]])
            current = 0
            for i in range(0, self.opts["times"] - 2):
                final_plan.append([])
                for i in range(0, count):
                    if current == len(delete_plan) -1:
                        break
                    final_plan[-1].append(delete_plan[i])
                    current += 1
                    final_plan[-1].append(add_plan[current])
            final_plan.append([delete_plan[-1]])

        self.print_debug(final_plan)

        self.print_debug("选择时间……")
        random_times = self.get_random_times()

        if self.opts["commit"] is not None:
            branch = git.get_branch_name(self.opts["dir"])
            self.print_debug(f"branch name: {branch}")
            git.new_branch(TEMP_BRANCH_NAME, self.opts["commit"], self.opts["dir"])
        for i in range(0, len(random_times)):
            t = random_times[i]
            # message = modify_work_space()
            # git.add_all(self.opts["dir"])
            # git.commit_with_time(message, t, self.opts["dir"])
            # current = git.get_head_hash(self.opts["dir"])
            self.print_debug(f"{t} {datetime.fromtimestamp(t).isoformat()}")

        patch = git.diff(f"{current}~{self.opts['times']}", current, self.opts["dir"])
        if len(patch.trim()) != 0:
            git.apply_reverse(patch, self.opts["dir"])
            git.commit_amend_with_time(random_times[-1], self.opts["dir"])

        if self.opts["commit"] is not None:
            git.rebase(TEMP_BRANCH_NAME, branch, self.opts["dir"])
            git.checkout(branch, self.opts["dir"])
            git.delete_branch(TEMP_BRANCH_NAME, self.opts["dir"])

        return current

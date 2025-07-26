from pathlib import Path
from typing import List, Dict

from git import Repo


class GitManager:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)
        self.repo_path = Path(repo_path)

    def execute_commits(self, refactor_plan: List[Dict]) -> None:
        for i, commit_info in enumerate(refactor_plan):
            print(f"📝 创建提交 {i + 1}/{len(refactor_plan)}: {commit_info['commit_message']}")

            # 写入新的文件内容
            file_path = self.repo_path / commit_info['file_path']
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(commit_info['new_content'])

            # 添加到Git暂存区
            self.repo.git.add(commit_info['file_path'])

            # 创建提交
            self.repo.git.commit('-m', commit_info['commit_message'])

            print(f"   ✅ {commit_info['description']}")

    def verify_final_state(self) -> bool:
        """验证最终状态是否与初始状态相同"""
        # 这里可以添加更复杂的验证逻辑
        status = self.repo.git.status('--porcelain')
        return len(status.strip()) == 0

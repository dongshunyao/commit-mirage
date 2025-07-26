from pathlib import Path
from typing import Dict, Any

from commit_manager import CommitManager
from llm_analyzer import CodebaseAnalyzer
from llm_refactor import LLMRefactorer


class CommitMirage:
    def __init__(self, repo_path: str, llm_config: Dict[str, Any]):
        self.repo_path = Path(repo_path)
        self.analyzer = CodebaseAnalyzer(llm_config)
        self.refactorer = LLMRefactorer(llm_config)
        self.commit_manager = CommitManager(repo_path)

    def run(self, commits: int = 3) -> None:
        print("🔍 分析代码仓库结构...")
        codebase_summary = self.analyzer.analyze_repository(self.repo_path)

        print("🎯 选择要修改的文件...")
        target_files = self.analyzer.select_modification_targets(codebase_summary, commits)

        print("🛠️ 生成重构计划...")
        refactor_plan = self.refactorer.create_refactor_plan(target_files)

        print("📝 创建Git提交...")
        self.commit_manager.execute_commits(refactor_plan)

        print(f"✅ 完成！创建了 {len(refactor_plan)} 个提交")

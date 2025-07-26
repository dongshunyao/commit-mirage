import fnmatch
import json
import os
import random
from pathlib import Path
from typing import List, Dict, Any

from call_llm import call_llm
from utils import print_err


class CodebaseAnalyzer:
    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config

        self.supported_languages = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "javascript",
            ".tsx": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".hpp": "cpp",
            ".c": "c",
            ".h": "c",
        }

    def analyze_repository(self, repo_path: Path) -> Dict[str, Any]:
        summary = {
            "total_files": 0,
            "code_files": [],
            "modification_candidates": [],
            "language_distribution": {},
        }

        # 收集基本文件信息
        code_files = self._collect_code_files(repo_path)
        summary["code_files"] = code_files
        summary["total_files"] = len(code_files)

        # 统计语言分布
        summary["language_distribution"] = self._analyze_language_distribution(code_files)

        # 分析文件复杂度和修改候选
        summary["modification_candidates"] = self._analyze_modification_candidates(code_files)

        return summary

    def _collect_code_files(self, repo_path: Path) -> List[Dict[str, Any]]:
        code_files = []

        # 扩展的忽略模式
        ignore_patterns = [
            "*node_modules/*", "*.git/*", "*venv/*", "*__pycache__/*",
            "*target/*", "*build/*", "*dist/*", "*.pytest_cache/*",
            "*vendor/*", "*third_party/*", "*.gradle/*", "*cmake-build-*/*",
            "*.idea/*", "*.vscode/*", "*bin/*", "*obj/*",
            "*node_modules\\*", "*.git\\*", "*venv\\*", "*__pycache__\\*",
            "*target\\*", "*build\\*", "*dist\\*", "*.pytest_cache\\*",
            "*vendor\\*", "*third_party\\*", "*.gradle\\*", "*cmake-build-*\\*",
            "*.idea\\*", "*.vscode\\*", "*bin\\*", "*obj\\*"
        ]

        top_levels = os.listdir(str(repo_path))
        queries = []
        for toplevel in top_levels:
            fullpath = os.path.join(str(repo_path), toplevel)
            if os.path.isdir(fullpath):
                fullpath += os.path.sep
                if not any(fnmatch.fnmatch(fullpath, pattern) for pattern in ignore_patterns):
                    queries.append(fullpath)

        all = []
        for toplevel in top_levels:
            fullpath = os.path.join(str(repo_path), toplevel)
            if os.path.isfile(fullpath):
                all.append(Path(fullpath))

        for query in queries:
            all += Path(query).rglob("*")

        for file_path in all:
            if file_path.is_file() and file_path.suffix in self.supported_languages:
                relative_path = file_path.relative_to(repo_path)
                if any(fnmatch.fnmatch(str(relative_path), pattern) for pattern in ignore_patterns):
                    continue

                try:
                    file_info = {
                        "path": str(relative_path),
                        "absolute_path": str(file_path),
                        "language": self.supported_languages[file_path.suffix],
                        "size": file_path.stat().st_size,
                        "lines": self._count_lines(file_path),
                        "modification_potential": 0.0,
                        "last_modified": file_path.stat().st_mtime
                    }

                    file_info["modification_potential"] = self._calculate_modification_potential(file_info)
                    code_files.append(file_info)

                except Exception as e:
                    print_err(f"跳过文件 {file_path}: {e}")
                    continue

        return code_files

    def _count_lines(self, file_path: Path) -> int:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())

    def _analyze_language_distribution(self, code_files: List[Dict]) -> Dict[str, Dict]:
        distribution = {}

        for file_info in code_files:
            lang = file_info["language"]
            if lang not in distribution:
                distribution[lang] = {
                    "file_count": 0,
                    "total_lines": 0,
                    "total_size": 0,
                    "avg_complexity": 0.0,
                    "functions": 0,
                    "classes": 0
                }

            dist = distribution[lang]
            dist["file_count"] += 1
            dist["total_lines"] += file_info["lines"]
            dist["total_size"] += file_info["size"]

        for lang_data in distribution.values():
            if lang_data["file_count"] > 0:
                lang_data["avg_lines_per_file"] = lang_data["total_lines"] / lang_data["file_count"]

        return distribution

    def _calculate_modification_potential(self, file_info: Dict) -> float:
        score = 1.0
        language = file_info["language"]

        # 根据编程语言调整分数
        language_multipliers = {
            "python": 1.2,
            "javascript": 1.1,
            "typescript": 1.1,
            "java": 1.0,
            "cpp": 0.8,
            "c": 0.7
        }

        multiplier = language_multipliers.get(language, 1.0)
        score *= multiplier

        # 根据文件大小调整分数
        lines = file_info["lines"]
        if 100 <= lines <= 300:
            score += 8
        elif 50 <= lines < 100 or 300 < lines <= 500:
            score += 5
        elif 20 <= lines < 50:
            score += 3

        return round(score, 2)

    def _suggest_operations_for_language(self, file_info: Dict) -> List[str]:
        language = file_info["language"]
        operations = []

        # 通用操作
        operations.extend([
            "add_helper_function",
            "extract_method",
            "add_logging",
            "add_error_handling"
        ])

        # 语言特定操作
        if language == "python":
            operations.extend([
                "add_type_hints",
                "add_docstrings",
                "add_decorators",
                "add_context_manager"
            ])
        elif language in ["javascript", "typescript"]:
            operations.extend([
                "add_async_wrapper",
                "add_validation",
                "add_event_handlers",
                "extract_component"
            ])
        elif language == "java":
            operations.extend([
                "add_builder_pattern",
                "add_exception_handling",
                "add_annotations",
                "extract_interface"
            ])
        elif language in ["cpp", "c"]:
            operations.extend([
                "add_const_correctness",
                "add_memory_management",
                "add_error_codes",
                "extract_header"
            ])

        return operations

    def _analyze_modification_candidates(self, code_files: List[Dict]) -> List[Dict]:
        candidates = []

        for file_info in code_files:
            min_lines = 20
            max_lines = 600

            if min_lines <= file_info["lines"] <= max_lines:
                candidate = {
                    "file_info": file_info,
                    "modification_potential": file_info["modification_potential"],
                    "suggested_operations": self._suggest_operations_for_language(file_info),
                    "language_specific_features": self._get_language_features(file_info)
                }
                candidates.append(candidate)

        # 按修改潜力和语言多样性排序
        candidates.sort(key=lambda x: (
            x["modification_potential"],
            x["file_info"]["language"]  # 优先选择不同语言的文件
        ), reverse=True)

        return candidates[:21]

    def _get_language_features(self, file_info: Dict) -> Dict[str, Any]:
        language = file_info["language"]

        features = {
            "paradigm": self._get_language_paradigm(language),
            "typing": self._get_typing_system(language),
            "common_patterns": self._get_common_patterns(language)
        }

        return features

    def _get_language_paradigm(self, language: str) -> List[str]:
        paradigms = {
            "python": ["object-oriented", "functional", "procedural"],
            "javascript": ["object-oriented", "functional", "event-driven"],
            "typescript": ["object-oriented", "functional"],
            "java": ["object-oriented"],
            "cpp": ["object-oriented", "procedural", "generic"],
            "c": ["procedural"],
        }

        return paradigms.get(language, ["unknown"])

    def _get_typing_system(self, language: str) -> str:
        typing_systems = {
            "python": "dynamic_optional_static",
            "javascript": "dynamic",
            "typescript": "static",
            "java": "static",
            "cpp": "static",
            "c": "static",
        }

        return typing_systems.get(language, "unknown")

    def _get_common_patterns(self, language: str) -> List[str]:
        patterns = {
            "python": ["decorator", "context_manager", "generator", "metaclass"],
            "javascript": ["callback", "promise", "module", "closure"],
            "typescript": ["interface", "generic", "union_types", "decorators"],
            "java": ["singleton", "factory", "observer", "strategy"],
            "cpp": ["RAII", "template", "smart_pointer", "iterator"],
        }
        return patterns.get(language, [])

    def select_modification_targets(self, codebase_summary: Dict, commits: int) -> List[Dict]:
        repo_overview = self._prepare_repo_overview(codebase_summary)

        if codebase_summary["total_files"] < commits - 1:
            print_err(f"没有足够合适的文件")
            raise Exception

        file_count = random.randint(commits - 1, min(codebase_summary["total_files"], round(1.9 * commits)))

        prompt = f"""
        你是一个代码分析专家。我需要你帮我选择在一个代码仓库中要修改的文件，用于创建{commits}个Git提交。

        代码仓库概要：
        {json.dumps(repo_overview, indent=2, ensure_ascii=False)}

        要求：
        1. 选择{file_count}个不同的文件进行修改，不能重复选择文件！
        2. 每个文件要能支持"添加功能->删除功能"的操作序列
        3. 优先选择具有以下特征的文件：
           - 有函数和类可以扩展
           - 大小适中（50-500行）
           - 不是配置文件或测试文件
        4. 对每个选中的文件，建议具体的修改策略

        请直接以JSON格式返回你的选择，不需要其他说明，确保返回结果能被Python的json.loads()解析，不需要返回markdown代码块：
        {{
            "selected_files": [
                {{
                    "file_path": "path/to/file.py",
                    "reason": "选择理由",
                    "modification_strategy": "具体的修改策略",
                    "operations": ["add_function", "add_logging", "remove_additions"]
                }}
            ]
        }}
        """

        try:
            response = call_llm(self.llm_config, prompt)
            result = json.loads(response)
            return result["selected_files"]
        except Exception as e:
            print_err(f"LLM选择失败，使用回退策略: {e}")
            return self._fallback_selection(codebase_summary, file_count)

    def _prepare_repo_overview(self, codebase_summary: Dict) -> Dict:
        overview = {
            "total_files": codebase_summary["total_files"],
            "modification_candidates": []
        }

        # 只发送关键信息，不发送完整文件内容
        for candidate in codebase_summary["modification_candidates"][:15]:
            file_info = candidate["file_info"]
            overview["modification_candidates"].append({
                "path": file_info["path"],
                "language": file_info["language"],
                "lines": file_info["lines"],
                "potential_score": candidate["modification_potential"],
                "suggested_operations": candidate["suggested_operations"]
            })

        return overview

    def _fallback_selection(self, codebase_summary: Dict, file_count: int) -> List[Dict]:
        candidates = codebase_summary["modification_candidates"][:file_count]

        selected = []
        for candidate in candidates:
            file_info = candidate["file_info"]
            selected.append({
                "file_path": file_info["path"],
                "reason": "自动选择：具有良好的修改潜力",
                "modification_strategy": "添加辅助函数和注释",
                "operations": candidate["suggested_operations"][:3]
            })

        return selected

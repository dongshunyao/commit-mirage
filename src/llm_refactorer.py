import json
import os
from typing import List, Dict, Any

from call_llm import call_llm


class LLMRefactorer:
    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config

    def create_refactor_plan(self, target_files: List[Dict], dir) -> List[Dict]:
        refactor_plan = []

        for i, file_target in enumerate(target_files):
            file_path = os.path.join(dir, file_target["file_path"])

            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            file_commits = self._generate_file_commits(
                str(file_path),
                original_content,
                file_target,
                commit_prefix=f"[File {i + 1}]"
            )

            refactor_plan.extend(file_commits)

        return refactor_plan

    def _generate_file_commits(self, file_path: str, content: str,
                               target_info: Dict, commit_prefix: str) -> List[Dict]:
        add_prompt = f"""
        你是一个资深的软件开发者。我需要你为以下代码添加一些有用的功能，但这些功能稍后会被删除。

        文件路径: {file_path}
        修改策略: {target_info.get('modification_strategy', '添加辅助功能')}
        建议操作: {target_info.get('operations', [])}

        原始代码:
        ```
        {content}
        ```

        要求：
        1. 添加1个或2个有意义的功能，例如：
           - 新的辅助函数
           - 日志记录
           - 错误处理
           - 参数验证
           - 性能优化
        2. 单个文件修改的行数不要超过此文件已有行数的10%
        3. 确保添加的代码是高质量的、有意义的
        4. 不要破坏现有功能
        5. 保持代码风格一致
        6. 不要在文件末尾添加换行符
        7. 不要删除文件末尾已有的换行符
        8. 不要添加任何新的注释
        9. 不要删除任何已有的注释

        请返回修改后的完整代码和简短的变更说明，请直接以JSON格式返回结果，不需要其他说明，确保返回结果能被Python的json.loads()解析，不需要返回markdown代码块：

        格式：
        {{
            "modified_code": "完整的修改后代码",
            "commit_message": "精简的英文Git提交信息，不需要任何前缀"
        }}
        """

        add_response = call_llm(self.llm_config, add_prompt)
        add_result = self._parse_llm_response(add_response)

        remove_prompt = f"""
        现在我需要你删除刚才添加的功能，让代码回到原始状态。

        修改后的代码:
        ```
        {add_result['modified_code']}
        ```

        原始代码:
        ```
        {content}
        ```

        要求：
        1. 精确删除之前添加的功能
        2. 确保代码完全回到原始状态
        3. 不要遗留任何添加的代码

        请返回删除功能后的代码，请直接以JSON格式返回结果，不需要其他说明，确保返回结果能被Python的json.loads()解析，不需要返回markdown代码块。

        格式：
        {{
            "modified_code": "删除功能后的完整代码",
            "commit_message": "精简的英文Git提交信息，不需要任何前缀，尽量使用Update去描述，不要使用Delete/Remove/Revert描述"
        }}
        """

        remove_response = call_llm(self.llm_config, remove_prompt)
        remove_result = self._parse_llm_response(remove_response)

        return [
            {
                "file_path": file_path,
                "new_content": add_result['modified_code'],
                "commit_message": add_result['commit_message'],
            },
            {
                "file_path": file_path,
                "new_content": remove_result['modified_code'],
                "commit_message": remove_result['commit_message'],
            }
        ]

    def _parse_llm_response(self, response: str) -> Dict:
        try:
            return json.loads(response)
        except:
            import re
            json_match = re.search(r'```json\s*(\{.*?})\s*```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))

            return {
                "modified_code": response,
                "commit_message": "自动生成的更改"
            }

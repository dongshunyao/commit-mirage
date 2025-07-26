import json
from typing import List, Dict, Any


class LLMRefactorer:
    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config

    def create_refactor_plan(self, target_files: List[Dict]) -> List[Dict]:
        refactor_plan = []

        for i, file_target in enumerate(target_files):
            file_path = file_target["file_path"]

            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            file_commits = self._generate_file_commits(
                file_path,
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
        1. 添加1-3个有意义的功能，例如：
           - 新的辅助函数
           - 日志记录
           - 错误处理
           - 参数验证
           - 性能优化
        2. 确保添加的代码是高质量的、有意义的
        3. 不要破坏现有功能
        4. 保持代码风格一致

        请返回修改后的完整代码和简短的变更说明，请直接以JSON格式返回结果，不需要其他说明，确保返回结果能被Python的json.loads()解析

        格式：
        {{
            "modified_code": "完整的修改后代码",
            "changes_description": "添加了什么功能的简短描述",
            "commit_message": "Git提交信息"
        }}
        """

        add_response = self._call_llm(add_prompt)
        add_result = self._parse_llm_response(add_response)

        # 第二步：删除添加的功能
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

        请返回删除功能后的代码，请直接以JSON格式返回结果，不需要其他说明，确保返回结果能被Python的json.loads()解析

        格式：
        {{
            "modified_code": "删除功能后的完整代码",
            "changes_description": "删除了什么功能的描述",
            "commit_message": "Git提交信息"
        }}
        """

        remove_response = self._call_llm(remove_prompt)
        remove_result = self._parse_llm_response(remove_response)

        return [
            {
                "file_path": file_path,
                "new_content": add_result['modified_code'],
                "commit_message": f"{commit_prefix} {add_result['commit_message']}",
                "description": add_result['changes_description']
            },
            {
                "file_path": file_path,
                "new_content": remove_result['modified_code'],
                "commit_message": f"{commit_prefix} {remove_result['commit_message']}",
                "description": remove_result['changes_description']
            }
        ]

    def _call_llm(self, prompt: str) -> str:
        if self.llm_config["provider"] == "openai":
            import openai
            client = openai.OpenAI(api_key=self.llm_config["api_key"], base_url=self.llm_config["base_url"])
            response = client.chat.completions.create(
                model=self.llm_config["model"],
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        elif self.llm_config["provider"] == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=self.llm_config["api_key"], base_url=self.llm_config["base_url"])
            response = client.messages.create(
                model=self.llm_config["model"],
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.stop_reason == "end_turn":
                return response.content[0].text

        raise Exception

    def _parse_llm_response(self, response: str) -> Dict:
        try:
            return json.loads(response)
        except:
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))

            return {
                "modified_code": response,
                "changes_description": "LLM响应解析失败",
                "commit_message": "自动生成的更改"
            }

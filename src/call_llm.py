from typing import Dict, Any

import anthropic
import openai


def call_llm(llm_config: Dict[str, Any], prompt: str) -> str:
    if llm_config["provider"] == "openai":
        client = openai.OpenAI(api_key=llm_config["api_key"], base_url=llm_config["base_url"])
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    elif llm_config["provider"] == "anthropic":
        client = anthropic.Anthropic(api_key=llm_config["api_key"], base_url=llm_config["base_url"])
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=6500,
            messages=[{"role": "user", "content": prompt}]
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

    raise Exception

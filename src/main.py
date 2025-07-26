import argparse

from src.commit_mirage import CommitMirage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成虚假Git提交的工具")
    parser.add_argument("repo_path", help="Git仓库路径")
    parser.add_argument("--commits", type=int, default=3, help="要创建的提交数量") # 最少三个
    parser.add_argument("--llm-provider", choices=["anthropic", "openai"], default="anthropic")

    args = parser.parse_args()

    # LLM配置
    llm_config = {
        "provider": args.llm_provider,
        # "model": "gpt-4" if args.llm_provider == "openai" else "claude-3-sonnet",
        "url": "",
        "api_key": "your-api-key"  # 从环境变量或配置文件读取
    }

    generator = CommitMirage(args.repo_path, llm_config)
    generator.run(args.commits)

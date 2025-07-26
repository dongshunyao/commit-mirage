工作饱和器
=======

使用 LLM 生成一系列 git commit，看起来工作量很饱和，实际上这些 commit 最后全部互相抵消，并不影响实际功能。

# 特性

- **智能分析**: 使用 LLM 分析代码仓库结构，智能选择修改目标，自动修改代码。
- **多语言支持**: 支持 Python、JavaScript/TypeScript、Java、C++、C 等主流编程语言。
- **多LLM支持**: 支持 OpenAI 和 Anthropic。
- **随机时间**: 在指定时间范围内随机分布提交时间，使提交历史更自然。

# 安装

1. 克隆仓库:
```bash
git clone https://github.com/dongshunyao/commit-mirage.git
cd commit-mirage
```

2. 创建虚拟环境并安装依赖:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# 使用方法

## 基本用法

```bash
python src/main.py -p anthropic -b YOUR_BASE_URL -a YOUR_API_KEY GIT_WORK_DIR
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `dir` | string | - | 目标代码仓库路径 (必需) |
| `-t, --times` | int | 4 | 生成的提交数量 (最少: 2) |
| `-p, --provider` | string | anthropic | LLM 提供商 (`anthropic` 或 `openai`) |
| `-a, --api-key` | string | - | API 密钥 (必需) |
| `-b, --base-url` | string | - | 自定义 API 基础 URL (可选) |
| `-s, --start` | int | HEAD时间 | 提交的开始时间戳 (可选) |
| `-e, --end` | int | 当前时间 | 提交的结束时间戳 (可选) |
| `-c, --commit` | string | - | 在指定提交而不是最新提交之后生成 (可选) |
| `-d, --debug` | flag | false | 开启调试输出 |

# 注意事项

请不要在会给别人带来麻烦的情况下使用本项目，以免造成物理伤害！

# 常见问题

**Q: 工具是否会破坏我的代码？**
A: 不会。工具设计为最终状态会与原始状态完全一致。但是可能会破坏项目提交记录的可读性。

**Q: 为什么最少需要 2 个提交？**
A: 因为增加代码和减少代码需要匹配。

**Q: 生成的提交看起来真实吗？**
A: 如果你觉得 LLM 是可信的，那么生成的提交就可以是真实的。

**Q: 如何控制生成的提交数量？**
A: 使用 `-t` 参数控制。推荐 2-6 个提交，文件过少的情况下可能无法生成足够多的提交。

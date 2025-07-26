# 工作饱和器

**被喷工作不饱和？** 让“工作饱和器”来拯救你的 Git 提交记录！

**让你的 Git 图表全是小绿点** 无论是过去还是未来，时间任你选择！

**看起来忙得不可开交，实际上代码纹丝不动** 演技派打工人的摸鱼神器！

**代码变了又变，最终回到原点** 看似忙碌一整天，实际代码完全不变！

**一天提交几十次，代码最终一成不变** 工作饱和度 1000%，实际产出 0%！

> “工作饱和器”为你生成**指定时间内**的 Git Commit，采用 LLM 智能生成**零副作用**的代码，模拟繁忙的工作日常，让你的工作更**饱和**，从此告别“今天写了什么代码”的灵魂拷问！

> 搭配 GUI 使用效果更佳哦！ **https://github.com/dongshunyao/electron-commit-mirage**

## 特性

- **智能分析**: 使用 LLM 分析代码仓库结构，智能选择目标文件，全自动修改代码
- **多语言支持**: 支持 Python、JavaScript、TypeScript、Java、C++、C 等多种主流编程语言
- **多 LLM 支持**: 支持 OpenAI 和 Anthropic 模型调用，让AI帮你“工作”
- **随机时间**: 在指定时间范围内随机分布提交时间，模拟真实的工作节奏
- **完美伪装**: 生成的代码和功能专业且合理，无人能看出破绽
- **不留痕迹**: 所有修改最终完全抵消，代码回到初始状态

## 安装

> 克隆仓库

```bash
git clone https://github.com/dongshunyao/commit-mirage.git
cd commit-mirage
```

> 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 使用

> 推荐搭配 GUI 使用 **https://github.com/dongshunyao/electron-commit-mirage**

```bash
python src/main.py -p anthropic -b LLM_BASE_URL -a LLM_API_KEY GIT_WORK_DIR
```

| 参数               | 类型     | 默认值       | 说明                                    |
|------------------|--------|-----------|---------------------------------------|
| `dir`            | string | -         | 目标代码 Git 仓库路径                         |
| `-t, --times`    | int    | 2         | 生成 Commit 数量 (可选，最小值：2)               |
| `-p, --provider` | string | anthropic | LLM 服务提供商 (可选，`anthropic` 或 `openai`) |
| `-a, --api-key`  | string | -         | LLM 服务 API Key                        |
| `-b, --base-url` | string | -         | LLM 服务 Base URL                       |
| `-s, --start`    | int    | HEAD时间    | 生成 Commit 起始时间戳 (可选)                  |
| `-e, --end`      | int    | 当前时间      | 生成 Commit 结束时间戳 (可选)                  |
| `-c, --commit`   | string | -         | 在指定 Commit 后生成 (可选)                   |
| `-d, --debug`    | flag   | false     | 开启调试输出 (可选)                           |

## 注意事项

**重要声明**:

- 本项目仅供学习和娱乐使用，请勿在实际工作中欺骗老板
- 请不要在会给别人带来麻烦的情况下使用本项目，以免造成物理伤害！
- 使用前请确保你的老板没有发现这个项目（笑）

**温馨提示**：

- 道德使用: 请将此工具用于合理的演示、测试或教学目的
- 团队协作: 如果在团队项目中使用，请确保团队成员知情
- 备份代码: 理论上代码不会发生实际变化，但是安全第一
- 适度使用: 过于频繁地 Git Commit 可能会暴露你自己

## Q & A

**Q: 工具是否会破坏我的代码？**

> A: 不会。工具设计为最终状态会与原始状态完全一致。但是可能会破坏项目 Git 提交记录的可读性。

**Q: 为什么最少需要 2 个提交？**

> A: 因为增加代码和减少代码需要匹配，推荐 2 至 8 个提交。

**Q: 生成的提交看起来真实吗？**

> A: 如果你觉得 LLM 是可信的，那么生成的提交就可以是真实的。毕竟现在AI写代码也很常见。

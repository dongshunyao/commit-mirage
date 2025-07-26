# 工作饱和器

一个使用 LLM 智能生成"虚假"Git 提交历史的工具。通过添加和删除功能，创建有意义的开发活动记录，同时确保代码最终回到原始状态。

## ✨ 特性

- 🤖 **智能分析**: 使用 LLM 分析代码仓库结构，智能选择修改目标
- 🔄 **功能循环**: 添加有意义的功能，然后在后续提交中删除，形成完整的开发历史
- 🌍 **多语言支持**: 支持 Python、JavaScript/TypeScript、Java、C++、C 等主流编程语言
- 🔗 **多LLM支持**: 支持 OpenAI 和 Anthropic API
- ⏰ **时间分布**: 在指定时间范围内随机分布提交时间，使提交历史更自然
- 🔒 **状态保证**: 确保最终代码完全回到原始状态，无副作用
- 📊 **智能权重**: 根据文件复杂度和语言特性智能评估修改潜力

## 🚀 安装

1. 克隆仓库:
```bash
git clone https://github.com/dongshunyao/commit-mirage.git
cd commit-mirage
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

## 📖 使用方法

### 基本用法

```bash
python src/main.py /path/to/your/repo -p anthropic -a YOUR_API_KEY
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `dir` | string | - | 目标代码仓库路径 (必需) |
| `-t, --times` | int | 4 | 生成的提交数量 (最少: 3，推荐: 4-8) |
| `-p, --provider` | string | anthropic | LLM 提供商 (`anthropic` 或 `openai`) |
| `-a, --api-key` | string | - | API 密钥 (必需) |
| `-b, --base-url` | string | - | 自定义 API 基础 URL (可选) |
| `-s, --start` | int | HEAD时间 | 提交的开始时间戳 (可选) |
| `-e, --end` | int | 当前时间 | 提交的结束时间戳 (可选) |
| `-c, --commit` | string | - | 在指定提交后生成 (可选) |
| `-d, --debug` | flag | false | 开启调试模式 |

### 使用示例

```bash
# 生成 6 个提交，使用 Anthropic API
python src/main.py ./my-project -t 6 -p anthropic -a sk-your-key

# 使用 OpenAI API，指定时间范围
python src/main.py ./my-project -p openai -a your-openai-key -s 1640995200 -e 1641081600

# 在特定提交后生成，开启调试模式
python src/main.py ./my-project -p anthropic -a sk-your-key -c abc123def -d

# 使用自定义API端点
python src/main.py ./my-project -p anthropic -a sk-your-key -b https://api.anthropic.com
```

## 🔧 工作流程

```
1. 📊 仓库分析
   ├── 扫描代码文件
   ├── 分析语言分布
   ├── 计算文件复杂度
   └── 评估修改潜力

2. 🎯 智能选择  
   ├── LLM 分析仓库概要
   ├── 选择最适合的文件
   ├── 确保语言多样性
   └── 生成修改策略

3. 📋 计划生成
   ├── 为每个文件生成添加功能提交
   ├── 生成对应的删除功能提交
   ├── 优化提交顺序
   └── 确保最终状态一致

4. ⚡ 执行提交
   ├── 按时间顺序执行提交
   ├── 写入文件修改
   ├── 创建Git提交
   └── 验证最终状态

5. ✅ 状态验证
   ├── 检查代码一致性
   ├── 清理临时分支
   └── 确保无副作用
```

## 📋 支持的语言

| 语言 | 扩展名 | 特色功能 | 权重 |
|------|---------|----------|------|
| Python | `.py` | 类型提示、装饰器、上下文管理器、文档字符串 | 1.2 |
| JavaScript | `.js` | 异步包装、事件处理、模块系统、回调函数 | 1.1 |
| TypeScript | `.ts` | 接口、泛型、联合类型、装饰器 | 1.1 |
| Java | `.java` | 建造者模式、注解、异常处理、接口提取 | 1.0 |
| C++ | `.cpp`, `.hpp` | RAII、模板、智能指针、迭代器 | 0.8 |
| C | `.c`, `.h` | 内存管理、错误码、常量正确性 | 0.7 |

## 🎨 生成的提交类型

### 功能添加提交
- 🔧 辅助函数
- 📝 日志记录
- 🛡️ 错误处理
- ✅ 参数验证
- ⚡ 性能优化

### 语言特定功能
- **Python**: 类型提示、装饰器、上下文管理器
- **JavaScript/TypeScript**: 异步包装、事件处理、组件提取
- **Java**: 建造者模式、异常处理、注解
- **C/C++**: 内存管理、模板、RAII

## ⚠️ 注意事项

- 🔒 **仅在干净的工作目录中运行** - 工具会检查是否有未提交的更改
- 💾 **备份重要代码** - 虽然工具设计为安全的，但建议先备份重要项目
- ⏳ **耐心等待** - LLM 分析和代码生成需要一些时间（通常1-5分钟）
- 💰 **API 费用** - 使用会产生 LLM API 调用费用
- 📈 **适中的文件大小** - 最适合 20-600 行的代码文件
- 🚫 **避免配置文件** - 工具会自动忽略配置、测试、构建文件

## 📁 项目结构

```
commit-mirage/
├── src/
│   ├── main.py              # 🚪 程序入口
│   ├── commit_mirage.py     # 🧠 主要业务逻辑
│   ├── codebase_analyzer.py # 📊 代码仓库分析
│   ├── llm_refactorer.py    # 🤖 LLM 重构生成
│   ├── call_llm.py         # 📞 LLM API 调用
│   ├── git.py              # 🔧 Git 操作封装
│   └── utils.py            # 🛠️ 工具函数
├── requirements.txt         # 📦 依赖列表
├── .gitignore              # 🙈 Git 忽略规则
└── README.md               # 📖 项目文档
```

## 🤔 常见问题

**Q: 工具是否会破坏我的代码？**
A: 不会。工具设计为完全可逆，最终状态会与原始状态完全一致。所有更改都是临时的。

**Q: 为什么最少需要 3 个提交？**
A: 至少需要"添加功能→修改功能→删除功能"的序列来创建有意义的开发历史。

**Q: 生成的提交看起来真实吗？**
A: 是的，LLM 会根据编程惯例生成符合实际开发流程的提交信息和代码修改。

**Q: 支持哪些 LLM 提供商？**
A: 目前支持 OpenAI (GPT-4) 和 Anthropic (Claude 3)，可以通过自定义 base-url 使用兼容的 API。

**Q: 如何控制生成的提交数量？**
A: 使用 `-t` 参数控制。推荐 4-8 个提交，过多可能影响性能，过少可能不够自然。

## 🔬 技术原理

1. **智能文件选择**: 使用启发式算法和 LLM 分析选择最适合修改的文件
2. **语言特定优化**: 针对不同编程语言生成符合惯例的代码修改
3. **时间分布算法**: 使用随机间隔在指定时间范围内分布提交
4. **状态保证机制**: 通过 Git diff 和代码比较确保最终状态一致

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢 OpenAI 和 Anthropic 提供强大的 LLM API
- 感谢开源社区的持续贡献和反馈

---

⭐ 如果这个项目对你有帮助，请给我们一个 Star！

# LLM Wiki Skill for Claude Code

> **增量构建并维护你的个人知识库** — 知识持续复利，LLM 负责所有簿记工作。 Inspired by Andrej Karpathy's LLM Wiki pattern.

## 特性

- ✨ **从零初始化**一个新的 LLM Wiki 知识库
- 📥 **Ingest 摄入** - 支持单个文件（文章、笔记）
- 📁 **项目整体摄入** - 把整个 Git 仓库抓进来，智能提取文档和代码知识，自动过滤依赖和二进制
- 🔍 **Wiki 查询** - 基于已有知识回答问题，优质问答可以保存回 Wiki
- 🏥 **Lint 健康检查** - 查找孤立页面、死链接、缺失概念
- 🔀 **多知识库支持** - 同时管理多个独立知识库，随时切换
- 🧩 **模块化设计** - 易于扩展支持新文件类型
- 📦 **纯 Markdown** - 兼容 Obsidian 等任何工具

## 📚 文档

- [**完全入门指南**](./docs/GETTING_STARTED.md) - 从零开始，详细讲解所有概念和用法
- [**实战示例**](./docs/EXAMPLE.md) - 完整走一遍从 0 构建知识库的流程，一看就会
- [**强大功能详解**](./docs/ADVANCED_FEATURES.md) - 多知识库、项目摄入、知识复利、高级技巧，带你从入门到精通

## 安装

在 Claude Code 中，安装到全局：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/你的用户名/llm-wiki ~/.claude/skills/llm-wiki
```

然后重启 Claude Code 即可使用。

## 快速开始

### 1. 初始化

```
/llm-wiki init
```

默认会创建在 `~/Documents/llm-wiki/default`。你也可以指定路径：

```
/llm-wiki init ~/Documents/my-knowledge-base "我的知识库"
```

### 2. 添加内容

把你的文章/笔记/项目放到 `raw/untracked/` 目录下，然后：

```
/llm-wiki ingest
```

或者摄入整个项目：

```
/llm-wiki ingest --project path/to/my-project
```

### 3. 查询

```
/llm-wiki query "xxx 这个概念的核心是什么？"
```

回答后可以选择保存问答回 Wiki，知识复利增长。

### 4. 维护

定期运行：

```
/llm-wiki lint
```

检查健康问题，可以 `--fix` 自动修复。

## 命令总览

| 命令 | 功能 |
|------|------|
| `/llm-wiki init [path] [name]` | 初始化新知识库 |
| `/llm-wiki ingest [path]` | 摄入新源 |
| `/llm-wiki ingest --all` | 摄入所有 untracked |
| `/llm-wiki ingest --project` | 摄入整个项目 |
| `/llm-wiki ingest -y` | 跳过确认直接执行 |
| `/llm-wiki query "question"` | 查询问答 |
| `/llm-wiki lint` | 健康检查 |
| `/llm-wiki lint --fix` | 自动修复 |
| `/llm-wiki list` | 列出所有知识库 |
| `/llm-wiki switch <name>` | 切换当前知识库 |
| `/llm-wiki status` | 当前知识库统计 |
| `/llm-wiki config` | 显示配置信息 |

## 架构

```
Skill code (read-only): ~/.claude/skills/llm-wiki/
User data:              User-specified path (anywhere)
Config:                 ~/.llm-wiki/config.json
```

- 技能升级不影响用户数据
- 支持多个独立知识库
- 所有内容都是纯 Markdown，Obsidian 友好

## 理念

> 大多数 RAG 系统：你提问 → AI 每次都从原始文档重新发现知识 → 没有积累
>
> **LLM Wiki**: 添加源 → LLM 一次整合进结构化 Wiki → 知识持续复利 → 查询直接读已经整合好的知识

**分工：**
- 你：提供源、提出好问题、引导方向
- LLM：所有簿记工作（总结、交叉引用、更新索引、维护一致性）

## 相关

- [Andrej Karpathy's original LLM Wiki idea](https://github.com/karpathy/llm-wiki)
- 遵循 [AgentSkills](https://agentskills.io/) 开放标准

## 许可证

MIT

---
name: llm-wiki
description: LLM Wiki 个人知识库构建工具 - 增量构建并维护一个持久化、互相关联的个人知识库，支持单文件和整个项目摄入
author: community
user-invocable: true
---

# LLM Wiki Skill

> **增量构建持久化个人知识库** —— 让 LLM 帮你维护维基，知识持续复利。 Inspired by Andrej Karpathy's LLM Wiki pattern.

**核心思想**：
- 不是每次查询都从原始文档重新发现知识，而是增量构建并维护一个持久化、互相关联的维基
- 知识被编译一次就保持更新，不会每次都重新推导
- LLM 负责所有簿记工作（总结、交叉引用、更新索引），你只负责探索和提问

## 功能

- ✨ 初始化新的 LLM Wiki 知识库
- 📥 Ingest 摄入单个文件（文章、PDF、图片等）
- 📁 Ingest 摄入整个项目（自动过滤，智能提取代码知识）
- 🔍 基于知识库查询回答，优质问答可以保存回知识库
- 🏥 Lint 健康检查（查找矛盾、孤立页面、缺失概念）
- 🔀 支持多个知识库，随时切换
- 🔧 模块化设计，易于扩展支持新文件类型

## 命令

### 初始化

```
/llm-wiki init [path]
```
- 如果不提供 path，默认在 `~/Documents/llm-wiki/default` 初始化

### 摄入新源

```
/llm-wiki ingest [file-or-directory]
/llm-wiki ingest --all       # Ingest 所有 untracked 文件
/llm-wiki ingest -y          # 跳过确认直接执行
/llm-wiki ingest --project  # 明确指定是整个项目摄入
```

### 查询问题

```
/llm-wiki query "你的问题是什么？"
```
- 回答后会询问是否保存问答到知识库

### 健康检查

```
/llm-wiki lint
/llm-wiki lint --fix  # 自动修复问题
```

### 知识库管理

```
/llm-wiki list          # 列出所有已添加的知识库
/llm-wiki switch <name> # 切换当前知识库
/llm-wiki status        # 显示当前知识库状态
/llm-wiki config        # 显示当前配置
```

## 工作流程

1. **Ingest** - 添加原始源 → LLM 提取关键信息 → 创建/更新相关概念页面 → 更新索引 → 更新日志 → 移动原始文件到已处理
2. **Query** - 读取索引 → 查找相关页面 → 综合信息回答 → 可选择保存问答回 Wiki
3. **Lint** - 检查不健康内容 → 提供修复建议 → 可自动修复

## 架构

- **技能代码**：`~/.claude/skills/llm-wiki/`（只读，升级不影响用户数据）
- **用户数据**：用户指定的任意目录（每个知识库独立）
- **配置**：`~/.llm-wiki/config.json` 管理多个知识库

## 相关

- [LLM Wiki 原理念](https://github.com/karpathy/llm-wiki)
- 这个 Skill 遵循 [AgentSkills](https://agentskills.io/) 开放标准

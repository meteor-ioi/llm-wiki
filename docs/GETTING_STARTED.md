# LLM Wiki 完全入门指南

> **让 AI 帮你维护个人知识库，知识持续复利增长**

## 📖 什么是 LLM Wiki

LLM Wiki 是一个 Claude Code Skill 工具，它帮助你**增量构建并持久维护一个个人知识库**。这个想法最初由 Andrej Karpathy 提出，核心理念是：

| 传统 RAG 系统 | LLM Wiki |
|--------------|----------|
| 每次提问都从原始文档重新发现知识 | 添加源 → LLM 一次整合进结构化 Wiki → 知识持续复利 |
| 没有积累，每次都重新开始 | 知识被编译一次，之后只需要保持更新 |
| 你做所有簿记工作 | LLM 负责总结、交叉引用、更新索引 |

**简单说**：你负责提供素材、提出好问题，LLM 负责所有脏活累活。

---

## 🚀 一分钟快速开始

### 1. 安装 Skill

在你的终端执行：

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/你的用户名/llm-wiki.git
```

然后重启 Claude Code，或者重新加载技能。

### 2. 初始化你的第一个知识库

在 Claude Code 中输入：

```
/llm-wiki init
```

你会看到类似这样的输出：

```
✓ 知识库初始化完成！

位置: /Users/你的用户名/Documents/llm-wiki/default

下一步：
1. 把你的笔记、文章、文档放到 `/Users/你的用户名/Documents/llm-wiki/default/raw/untracked/` 目录
2. 然后执行 `/llm-wiki ingest` 开始摄入
```

### 3. 摄入你的第一篇文章

把你的一篇 Markdown 笔记放到 `raw/untracked/` 目录，然后：

```
/llm-wiki ingest
```

LLM Wiki 会：
1. 读取文章内容
2. 提取核心概念
3. 创建概念页面
4. 更新索引和日志
5. 把原始文件移到 `raw/ingested/`

### 4. 开始查询

摄入完成后，你就可以提问了：

```
/llm-wiki query "刚刚那篇文章讲的核心观点是什么？"
```

如果你觉得回答很好想保存，回答"是"就会保存到知识库中，下次查询可以直接用。

---

## 📁 目录结构说明

初始化完成后，你的知识库目录结构是这样的：

```
你的知识库/
├── CLAUDE.md                    # Wiki 维护规则，Claude 会读这个
├── raw/
│   ├── untracked/               # 👈 你把新文件放这里
│   └── ingested/                # 处理完的原始文件会移到这里（按日期分组）
└── wiki/
    ├── index.md                 # 📇 总索引（自动维护）
    ├── log.md                   # 📝 操作日志（自动追加）
    ├── concepts/                # 💡 概念/实体页面
    ├── sources/                 # 📄 原始源摘要页面
    └── answers/                 # ❓ 已保存的问答页面
```

### 各目录作用

| 目录 | 作用 | 你需要做什么 |
|------|------|-------------|
| `raw/untracked/` | 放待处理的新文件 | 把你想加进知识库的东西扔这里 |
| `raw/ingested/` | 已处理的原始文件 | 一般不用管，留作备份 |
| `wiki/concepts/` | 核心概念页面 | LLM 自动创建，你也可以手动编辑 |
| `wiki/sources/` | 来源摘要 | LLM 自动创建 |
| `wiki/answers/` | 优质问答保存 | LLM 自动创建，你批准才会加 |
| `index.md` | 总索引 | 自动维护，不用手动改 |
| `log.md` | 操作日志 | 自动追加 |

---

## 🔍 所有命令详解

### `/llm-wiki init` - 初始化知识库

**用法：**
```bash
# 默认位置初始化
/llm-wiki init

# 指定位置和名称
/llm-wiki init ~/Documents/my-personal-wiki "我的个人知识库"
```

**作用：**
- 创建目录结构
- 从模板复制索引和日志
- 添加到全局配置
- 设为当前激活的知识库

**默认位置：** `~/Documents/llm-wiki/default`

---

### `/llm-wiki ingest` - 摄入新知识

**用法：**
```bash
# 摄入 untracked 目录下所有文件
/llm-wiki ingest

# 摄入单个文件
/llm-wiki ingest path/to/your-note.md

# 摄入整个项目（当前目录）
/llm-wiki ingest --project

# 摄入指定目录的项目
/llm-wiki ingest --project path/to/your-project

# 跳过确认直接执行
/llm-wiki ingest -y

# 重新摄入所有 untracked
/llm-wiki ingest --all
```

**工作流程：**

1. **扫描文件** - 读取你指定的文件，对于项目会自动过滤掉 `node_modules`、`.git`、二进制文件等
2. **分析内容** - LLM 分析内容，识别核心概念
3. **输出计划** - 告诉你会创建哪些页面、更新哪些页面，等你确认（如果用了 `-y` 就跳过）
4. **执行** - 实际创建更新页面
5. **整理** - 把原始文件移到 `raw/ingested/今日日期/`

**对于代码项目的处理规则：**

- ✅ `README.md` - 完整提取
- ✅ 源代码 - 提取模块/类/函数签名、文档注释，**不提取完整实现代码**
- ✅ 文档文件 - 完整提取
- ❌ 测试文件 - 跳过
- ❌ 依赖目录 - 自动跳过
- ❌ 二进制文件 - 跳过
- ❌ 大文件（>1MB）- 跳过

**示例 - 摄入整个项目：**

假设你有一个项目在 `~/code/my-app`，你想把它的架构知识摄入知识库：

```
/llm-wiki ingest --project ~/code/my-app
```

LLM 会：
- 扫描所有源代码文件
- 提取架构、模块关系、关键接口
- 为核心概念创建单独页面
- 生成项目整体文档

---

### `/llm-wiki query` - 查询知识库

**用法：**
```bash
/llm-wiki query "你的问题是什么？"
```

**工作流程：**

1. 从 `index.md` 找出所有相关页面
2. 读取这些页面的内容
3. 如果需要，继续顺着链接找更多内容
4. 整合所有信息给出答案
5. 回答完问你要不要保存这个问答

**什么时候保存问答？**

- 回答解决了一个具体问题
- 这个问题未来可能还会再问
- 答案整理得很清晰有长期价值

保存后会创建一个新页面到 `wiki/answers/`，并更新索引，下次查询就能直接用到这个知识。

**示例：**

```
/llm-wiki query "在这个项目中，认证流程是怎么设计的？"
```

---

### `/llm-wiki lint` - 健康检查

**用法：**
```bash
# 只检查，不修改
/llm-wiki lint

# 检查并自动修复
/llm-wiki lint --fix
```

**检查什么：**

| 检查项 | 说明 | 能自动修复吗？ |
|--------|------|---------------|
| 孤立页面 | 没有任何其他页面链接到它 | ❌ 需要你手动处理 |
| 死链 | 链接到不存在的页面 | ❌ 需要你手动处理 |
| 索引缺失 | 页面存在但没加入索引 | ✅ `--fix` 自动添加 |
| 内容矛盾 | 不同页面说的不一样 | ❌ 需要你手动处理 |
| 缺失概念 | 经常被提到但没有独立页面 | ✅ `--fix` 创建占位页面 |
| 需要扩展 | 内容太肤浅需要扩展 | ❌ 需要你手动处理 |

**示例：**

每月运行一次保持知识库健康：

```
/llm-wiki lint --fix
```

---

### 多知识库管理命令

#### `/llm-wiki list` - 列出所有知识库

```
/llm-wiki list
```

显示所有你添加过的知识库，以及当前哪个是激活的。

#### `/llm-wiki switch <name>` - 切换当前知识库

```
# 按名称切换
/llm-wiki switch "我的个人知识库"

# 按路径切换
/llm-wiki switch ~/Documents/work-wiki
```

切换后，所有操作（ingest/query/lint）都会作用到这个知识库。

#### `/llm-wiki status` - 当前知识库状态

```
/llm-wiki status
```

显示统计信息：多少概念页面、多少来源、多少问答。

#### `/llm-wiki config` - 显示配置信息

```
/llm-wiki config
```

显示全局配置文件位置，所有知识库列表。

---

## 💡 完整使用示例工作流

让我们走一遍完整流程，从新建知识库到不断维护增长。

### 第一步：创建工作知识库

```
/llm-wiki init ~/Documents/work-knowledge "我的工作知识库"
```

输出：
```
✓ 知识库 "我的工作知识库" 初始化完成
路径: /Users/you/Documents/work-knowledge

下一步：添加内容吧！
```

### 第二步：添加项目文档

把你项目的架构文档放到 `raw/untracked/`：

```bash
cp ~/code/my-project/ARCHITECTURE.md ~/Documents/work-knowledge/raw/untracked/
```

然后在 Claude Code 中：

```
/llm-wiki ingest
```

输出会类似：

```
## Ingest 计划

**新建页面:**

| 类型 | 相对路径 | 页面内容概述 |
|------|---------|-------------|
| source | sources/my-project-architecture.md | 系统架构文档，描述了微服务拆分 |
| concept | concepts/认证服务.md | 认证服务的职责和接口设计 |
| concept | concepts/订单服务.md | 订单服务的数据模型和核心流程 |

**更新:**
- wiki/index.md - 添加新页面到索引
- wiki/log.md - 添加操作日志

请确认后执行？
```

你检查一下计划没问题，回复"确认执行"。

执行完成：

```
✓ Ingest 完成！

- 创建了 3 个新页面
- 更新了 2 个页面
- 原始文件已移动到 raw/ingested/2026-04-06/

现在可以提问了！
```

### 第三步：提问查询

```
/llm-wiki query "认证服务是怎么处理 JWT 过期的？"
```

输出：

> 根据 [[认证服务]] 的设计：
>
> JWT 过期处理采用双 Token 机制：
> 1. Access Token 有效期 15 分钟，用于 API 鉴权
> 2. Refresh Token 有效期 7 天，用于获取新的 Access Token
> 3. 当 Access Token 过期，客户端用 Refresh Token 刷新 [src: [[认证服务]]]
>
> 刷新失败（Refresh 也过期）则要求用户重新登录。

然后 LLM 会问：

> 这个问答有长期保存价值吗？是否需要保存为 `wiki/answers/认证服务JWT过期处理.md` 并更新索引？

如果你觉得这个问题以后还会问，回复"是的，保存"。

### 第四步：添加新项目

过了一段时间，你新接手了另一个项目 `user-service`，想加进来：

```
/llm-wiki ingest --project ~/code/user-service -y
```

`-y` 参数跳过确认，直接执行。

### 第五步：定期健康检查

每月一次：

```
/llm-wiki lint --fix
```

它会帮你：
- 找出经常提到但还没有页面的概念，自动创建占位页面
- 把漏了的页面加进索引
- 告诉你哪些内容可能过时了

---

## 🌟 使用最佳实践

### 什么时候用 LLM Wiki？

✅ **适合：**
- 个人笔记整理
- 技术知识积累
- 项目架构文档沉淀
- 学习笔记系统化
- 会议记录整理归档

❌ **不适合：**
- 需要实时同步的团队协作（目前）
- 完全动态的数据
- 超大文件批量导入（一次最好不超过 10 个文件）

### 摄入技巧

1. **分批次摄入** - 一次不要扔 100 个文件进去，分几次效果更好
2. **先摄入后提问** - 摄入整理完再提问，回答质量更高
3. **项目摄入只存知识** - 不需要存所有代码，只存设计决策和架构知识
4. **保持概念颗粒度合适** - 一个概念一个页面，不要把 10 个不相关的概念挤在一页

### 查询技巧

1. **问题越具体越好** - "认证服务怎么处理 JWT 过期" > "说说认证"
2. **跨概念查询** - 可以问"A 概念和 B 概念有什么区别？"，LLM 会自动读两个页面
3. **保存优质问答** - 好的问答是知识库的复利，不要吝啬保存

### 维护技巧

1. **定期 lint** - 每月跑一次 `/llm-wiki lint --fix`
2. **手动编辑没问题** - 所有页面都是纯 Markdown，你可以随时用任何编辑器（比如 Obsidian）手动编辑
3. **删除不用的页面** - 直接删文件就行，下次 `lint` 会发现并提醒你
4. **和 Obsidian 一起用** - 把 LLM Wiki 目录放到 Obsidian 里面可以兼得两者好处

---

## 🔧 自定义配置

### 自定义忽略规则

在知识库根目录创建 `.llm-wiki-ignore` 文件，每行一个规则：

```
# 示例：忽略一些目录
vendor/
*.log
*.tmp
my-cache/
```

语法支持：
- `目录名/` - 匹配整个目录
- `*.ext` - 匹配扩展名

### 多知识库使用场景

什么时候需要多个知识库？

```
# 场景 1：分开工作和个人
/llm-wiki init ~/Documents/work "工作知识"
/llm-wiki init ~/Documents/personal "个人知识"
/llm-wiki switch work
```

```
# 场景 2：按项目分开
/llm-wiki init ~/projects/project-a/wiki "项目A"
/llm-wiki init ~/projects/project-b/wiki "项目B"
```

---

## ❓ 常见问题

### Q: 所有内容都存在哪里？会被上传吗？

A: 所有内容都存在**你自己电脑本地**，不会自动上传到任何地方。只有你主动 git 提交才会出去。Claude Code 只会在你执行命令时读取相关文件。

### Q: 和 Obsidian/Logseq 是什么关系？

A: 互补！LLM Wiki 输出的就是纯 Markdown 文件，完全兼容 Obsidian。你可以：
- 用 LLM Wiki 做自动化维护（摄入、索引更新）
- 用 Obsidian 做日常浏览和手动编辑

### Q: 支持哪些文件类型？

A: 默认支持所有文本格式：.md, .py, .js, .ts, .go, .rs, .java, .c, .cpp, .html, .css, .json, .yaml 等等代码和文档格式。二进制文件（图片、PDF）默认跳过。

### Q: 可以手动编辑页面吗？

A: 当然可以！所有页面都是纯 Markdown，你用任何编辑器编辑都没问题。下次 LLM 操作的时候会读取你编辑后的版本。

### Q: 误删了页面怎么办？

A: 如果你用 git 版本控制你的知识库，直接从 git 恢复。如果没开 git，llm-wiki 只会移动不会删除原始文件，原始文件还在 `raw/ingested/`，可以重新 ingest。

### Q: 升级 Skill 会影响我的数据吗？

A: 不会。Skill 代码和你的用户数据是完全分离的。Skill 代码在 `~/.claude/skills/llm-wiki/`，你的数据在你指定的目录，升级 pull 最新代码不会碰你的数据。

---

## 🛠 架构说明

```
Skill 代码 (升级不影响): ~/.claude/skills/llm-wiki/
├── SKILL.md              # Skill 定义
├── prompts/              # 各命令提示词模板
├── tools/                # Python 工具模块
└── templates/            # 初始化模板

用户配置: ~/.llm-wiki/config.json
用户数据: 你指定的任意目录 (每个知识库独立)
```

**设计原则：**
- 技能代码和用户数据完全分离
- 所有用户内容都是纯 Markdown
- 不锁格式，兼容其他工具
- 模块化易于扩展

---

## 📝 许可证

MIT

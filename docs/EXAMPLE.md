# 实战示例：从 0 构建个人技术知识库

本教程带你一步步，从空白开始构建一个关于 Go 语言学习的个人知识库。

## 准备工作

确保你已经：
1. 安装了 LLM Wiki Skill 到 Claude Code
2. 可以正常使用 `/llm-wiki` 命令

---

## 第一步：创建新知识库

我们创建一个专门的 Go 学习知识库：

```
/llm-wiki init ~/Documents/knowledge/go-learning "Go语言学习笔记"
```

**预期输出：**
```
✓ 知识库 "Go语言学习笔记" 初始化完成

位置: /Users/你的用户名/Documents/knowledge/go-learning

目录结构已创建，下一步：
1. 将你的学习笔记放到 raw/untracked/ 目录
2. 执行 /llm-wiki ingest 摄入
```

---

## 第二步：添加学习笔记

假设你有几篇学习笔记：

- `go-slices-internals.md` - Go Slice 内部实现
- `go-memory-management.md` - Go 内存管理
- `go-concurrency-patterns.md` - Go 并发模式

把这些文件放到 `~/Documents/knowledge/go-learning/raw/untracked/`：

```bash
cp ~/downloads/go-slices-internals.md ~/Documents/knowledge/go-learning/raw/untracked/
cp ~/downloads/go-memory-management.md ~/Documents/knowledge/go-learning/raw/untracked/
cp ~/downloads/go-concurrency-patterns.md ~/Documents/knowledge/go-learning/raw/untracked/
```

---

## 第三步：执行摄入

回到 Claude Code，执行：

```
/llm-wiki ingest
```

LLM Wiki 会扫描 `raw/untracked/` 目录下的三个文件，然后分析内容，给出一个计划：

```
## Ingest 计划

**新建页面:**

| 类型 | 相对路径 | 页面内容概述 |
|------|---------|-------------|
| source | sources/go-slices-internals.md | Go Slice 内部实现分析，讲解结构体、扩容策略 |
| source | sources/go-memory-management.md | Go 内存分配器设计，GC 标记清除算法 |
| concept | concepts/Slice(Go).md | Go Slice 数据结构 |
| concept | concepts/Go内存分配.md | Go 内存分配器工作原理 |
| concept | concepts/GC标记清除.md | Go GC 使用的标记清除算法 |
| concept | concepts/并发模式.md | Go 常见并发设计模式 |

**更新页面:**
- wiki/index.md - 添加新页面到索引
- wiki/log.md - 添加操作日志

请确认后执行？
```

---

## 第四步：确认执行

检查一下计划，确认没问题后回复：

```
确认执行
```

LLM 会开始创建页面：

```
✓ 创建 wiki/sources/go-slices-internals.md
✓ 创建 wiki/sources/go-memory-management.md
✓ 创建 wiki/concepts/Slice(Go).md
✓ 创建 wiki/concepts/Go内存分配.md
✓ 创建 wiki/concepts/GC标记清除.md
✓ 创建 wiki/concepts/并发模式.md
✓ 更新 wiki/index.md
✓ 更新 wiki/log.md
✓ 移动原始文件到 raw/ingested/2026-04-06/

✓ Ingest 完成！

- 创建了 6 个新页面
- 更新了 2 个页面

现在可以提问了！
```

---

## 第五步：开始查询

现在你的知识库已经有了基础知识，试试提问：

```
/llm-wiki query "Go Slice 扩容的时候会发生什么？"
```

**回答示例：**

> 根据 [[Slice(Go)]] 和 [[go-slices-internals]] 的分析：
>
> Go Slice 扩容分几种情况：
>
> | 当前容量 | 扩容策略 |
> |----------|---------|
> | < 1024 | 容量翻倍 |
> | ≥ 1024 | 容量增加 25% 每次 |
>
> 扩容的具体步骤：
> 1. 分配新的底层数组
> 2. 拷贝原数组元素到新数组
> 3. Slice 结构体中的指针指向新数组
> 4. 更新容量字段
>
> 如果是 append 多个元素，计算后的新容量还是不够，会一直扩容直到够 [src: [[go-slices-internals]]]
>
> 注意：扩容后原 Slice 和新 Slice 会指向不同的底层数组，修改互不影响。

然后 LLM 会问你：

> 这个问答有长期保存价值吗？是否需要保存为 `wiki/answers/GoSlice扩容过程.md` 并更新索引？

如果你觉得这个问答以后查起来方便，回复：

```
是的，请保存
```

结果：

```
✓ 已保存问答到 wiki/answers/GoSlice扩容过程.md
✓ 已更新 index.md
✓ 已更新日志
```

---

## 第六步：添加更多知识 - 摄入书籍章节

你买了一本《Go 程序设计语言》，把其中某几章导出为 Markdown，放到 `raw/untracked/`，然后：

```
/llm-wiki ingest -y
```

`-y` 参数跳过确认直接执行。

---

## 第七步：提问跨概念问题

现在知识库有更多内容了，可以提问更复杂的问题：

```
/llm-wiki query "Go 的内存分配和 GC 标记是怎么配合工作的？"
```

LLM 会自动找到相关的几个页面，整合信息给出回答。如果回答很好，保存它！

---

## 第八步：健康检查

积累了一段时间后，运行：

```
/llm-wiki lint --fix
```

**可能的输出：**

```
## 健康检查结果

### 静态问题

- ✓ 没有孤立页面
- ✓ 没有死链

### 语义问题

- ⚠️ 缺失概念: 写屏障 (被提到 3 次，没有独立页面)
- ⚠️ 需要扩展: 并发模式 内容比较简略，可以扩展

### 自动修复

✓ 已创建 concepts/写屏障.md 占位页面
✓ 已添加写屏障 到 index.md

请手动完善新创建的占位页面。
```

你看到 `写屏障` 被创建了占位页面，有空的时候可以补充内容。

---

## 第九步：切换其他知识库

如果你还有另一个 Rust 学习知识库，可以随时切换：

```
/llm-wiki list
```

输出：
```
已配置的知识库:

* [当前] Go语言学习笔记 → /Users/you/Documents/knowledge/go-learning
  Rust学习笔记 → /Users/you/Documents/knowledge/rust-learning
  工作项目知识库 → /Users/you/work/project/wiki
```

切换：

```
/llm-wiki switch "Rust学习笔记"
```

输出：
```
✓ 已切换到知识库: Rust学习笔记
路径: /Users/you/Documents/knowledge/rust-learning
```

现在所有操作都切换到 Rust 知识库了。

---

## 🎉 完成！

现在你已经掌握了 LLM Wiki 的完整工作流：

1. `init` → 创建知识库
2. 扔文件到 `raw/untracked/`
3. `ingest` → LLM 整理成结构化知识
4. `query` → 提问，保存优质问答
5. 定期 `lint --fix` → 保持健康

知识就这样一点点积累，越用越好用！

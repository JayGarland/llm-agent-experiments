# Jie Personal Manual — v0.1 Base Manual

这是为项目所有者 Jie 准备的个性化中文操作手册，基于 `v0.1-base-manual` 发布。

---

## 1. 当前版本定位

现在这个 release 不是最终系统。

它是一个已经发布的 `base` branch v0.1，带有 tag `v0.1-base-manual`。

它的用途是：
- 作为派生后续实验分支的起点；
- 作为其他 repo 或实验的基础；
- 提供一个干净、最小化的手动实验框架。

**不要继续把 base 变重。** 后续功能放在派生分支上。

### 如果忘了项目上下文（future-you onboarding）

一段时间后回来，不知道当前状态？运行这三条命令：

```powershell
git branch --show-current          # 你在哪个分支上
git status --porcelain -b          # working tree 是否干净
python scripts/prepare_manual_run.py --library-path "F:\Path\To\ExternalSubLLMWiki"
```

第三条会创建一个新 run 并打印完整操作指引。然后检查生成的 `instructions.txt` 和 `run.json` 确认 source 路径正确，再打开 agent。

---

## 2. 你现在可以做什么

- ✅ 配置 `READ_ONLY_LIBRARY_PATH`（指向你的 sub LLM-Wiki 或 `library_sample/`）。
- ✅ 用 `python scripts/prepare_manual_run.py` 创建一个 `sandbox/run-*` 目录。
- ✅ 在 run 目录里打开一个外部 AI agent（Claude Code / Copilot Agent 等）。
- ✅ 告诉 agent：`Read instructions.txt and execute the experiment.`
- ✅ 观察 agent 自由探索。
- ✅ 检查它是否留下 `HELLO.md`。
- ✅ 确认 source/library 未被修改。
- ✅ 归档 run 目录，或从 `base` 派生下一个实验分支。

---

## 3. 你现在不要做什么

- ❌ 不要把 `base` 当成最终系统来用。
- ❌ 不要在这个 release 上加 watcher / trigger / agent runner。
- ❌ 不要期望 agent 会自动更新你的 sub LLM-Wiki。
- ❌ 不要把 source/library 当任务塞给 agent。
- ❌ 不要以"必须产生 artifact ecology"为标准评判 run。
- ❌ 不要在 repo root 打开 agent。

---

## 4. 当前正确实验公式

```
Karpathy Version A free-directory setup
+ read-only local sub LLM-Wiki as source/library
+ writable sandbox
= open observation of how source/library conditions free agent exploration
```

中文解释：

- **不是**让 agent 更新你的 sub LLM-Wiki。
- **不是**让 agent 分析 source/library。
- **不是**让 agent 必须生成 artifact ecology（HELLO + TRACE + fragments）。
- **是**观察它在这个 source/library 氛围下会如何自由探索。

---

## 5. 目录与权限边界

| 位置 | 权限 | 说明 |
|---|---|---|
| `library_sample/`（source/library） | 只读 | agent 可以查看和引用，不能修改。 |
| `sandbox/run-*/`（run 目录） | 可读写 | agent 唯一可以创建、编辑、运行文件的地方。 |
| 父目录 | 禁止 | 不属于 agent workspace。 |
| 兄弟 run 目录 | 禁止 | 其他 run 不是参考示例。 |
| repo root | 禁止 | `src/`、`docs/`、`tests/`、config 不在范围内。 |

每次 run 目录创建时，`instructions.txt` 里会明确写出 source/library 的路径和只读边界。

### `library_sample/` 只是内置 demo

- `library_sample/` 是这个 repo 内置的**示例** source/library，包含几个占位文件（`current_state.md`、`index.md`、`trace.md`、空 `notes/` 和 `raw/` 目录）。
- **真正的实验**通常应该使用外部的 sub LLM-Wiki。
- 框架代码在这个 repo 里；真实的 source/library 通常在 repo 外部。

### 推荐方式：每 run 指定 `--library-path`（主流程）

**不要每次都编辑 `src/config.py`。** 不同实验用不同的 sub LLM-Wiki，应该每次 run 通过命令行指定：

```powershell
python scripts/prepare_manual_run.py --library-path "F:\Path\To\ExternalSubLLMWiki"
```

示例（针对不同的 sub LLM-Wiki）：

```powershell
python scripts/prepare_manual_run.py --library-path "F:\Obsidian\SubLLMWiki-EmergentDesign"
python scripts/prepare_manual_run.py --library-path "F:\Obsidian\SubLLMWiki-AgentExperiments"
```

### 备选方式：设置 `src/config.py` 默认路径（fallback）

如果你总是用同一个 source/library，可以编辑 `src/config.py` 作为默认值：

```python
# 默认指向 repo 内置 demo
READ_ONLY_LIBRARY_PATH = REPO_ROOT / "library_sample"

# 改为指向你的真实 sub LLM-Wiki（repo 外部）
READ_ONLY_LIBRARY_PATH = Path("D:/my-sub-llm-wiki")
```

然后直接运行不加 `--library-path`：

```powershell
python scripts/prepare_manual_run.py
```

如果提供了 `--library-path`，它优先于 `src/config.py` 的默认值。

### 如何验证 run 正在使用哪个 source/library

每次用 `python scripts/prepare_manual_run.py` 创建 run 后，检查两个文件：

1. `instructions.txt` — 搜索 `Read-only source/library path:`，后面就是实际使用的路径。
2. `run.json` — 查看 `read_only_library_path` 字段。

如果这两个地方显示的路径不是你期望的，重新运行并确认 `--library-path` 参数正确（或 `src/config.py` 配置正确）。

### 创建 run 后的验证清单

每次 `python scripts/prepare_manual_run.py` 之后，确认：

- [ ] `instructions.txt` 包含正确的 source 路径（搜索 `Read-only source/library path:`）。
- [ ] `run.json` 包含相同的 source 路径（查看 `read_only_library_path` 字段）。
- [ ] agent workspace 是当前 run 目录（不是外部 source/library 目录）。
- [ ] 外部 source/library 没有被设定为 agent workspace。
- [ ] run 结束后，外部 source/library 未被修改。

---

## 6. 手动运行流程（详细版）

### 步骤 1：选择 source/library 路径

**推荐：** 每次 run 通过 `--library-path` 指定外部 sub LLM-Wiki 路径：

```powershell
python scripts/prepare_manual_run.py --library-path "F:\Obsidian\SubLLMWiki-AgentExperiments"
```

**备选：** 如果你总是用同一个 source/library，在 `src/config.py` 里设置默认值，然后不加参数：

```powershell
python scripts/prepare_manual_run.py
```

`--library-path` 优先于 `src/config.py` 的默认值。详见 §5。

### 步骤 2：创建 sandbox run 目录 + 验证 source 路径

```powershell
python scripts/prepare_manual_run.py --library-path "F:\Path\To\ExternalSubLLMWiki"
```

这会创建一个 `sandbox/run-YYYYMMDD-HHMMSS-xxxxxx/` 目录，并打印路径。

创建后，**务必验证** source/library 路径是否正确写入：

```powershell
# 检查 instructions.txt 里的路径
cat sandbox/run-*/instructions.txt | Select-String "source/library"

# 检查 run.json 里的路径
cat sandbox/run-*/run.json
```

### 步骤 3：在 run 目录里打开 AI agent（关键）

Agent workspace **必须是**当前 run 目录，且**只能是**当前 run 目录：

```powershell
cd sandbox/run-20260606-120000-abc123
claude  # 或其他 agent
```

**绝对不要：**

| ❌ 错误 workspace | 原因 |
|---|---|
| repo root（`llm-agent-experiments/`） | 暴露 `src/`、`docs/`、`tests/`、config |
| `sandbox/`（sandbox 根目录） | 暴露兄弟 run 目录 |
| source/library 路径 | agent 必须不能写入 source/library |
| 包含多个 run 的父目录 | 其他 run 不是参考示例 |

**每次打开 agent 前，确认你在哪个目录里：**

```powershell
pwd  # 应该显示 .../sandbox/run-YYYYMMDD-HHMMSS-xxxxxx
```

### 步骤 4：给 agent 下 prompt

直接告诉 agent：

```
Read instructions.txt and execute the experiment.
```

不要加额外解释。`instructions.txt` 里已经包含了所有边界规则。

### 步骤 5：让 agent 自由探索——不要干预

Agent 开始运行后：

- ✅ 让它自己决定做什么。
- ✅ 如果它读了 source/library，OK。
- ✅ 如果它没读 source/library，也 OK。
- ✅ 如果它开始写文件，让它写（只要在 run 目录里）。

**不要反复提示它。不要引导它。**

### 步骤 5b：如果 agent 跑偏了

| 情况 | 处理 |
|---|---|
| Agent 问你"我应该做什么？" | 回复：`No task is assigned. Explore freely.` |
| Agent 开始总结/分析/索引 source/library | 回复：`The source/library is soil, not a task.` |
| Agent 尝试写入 source/library | **立刻终止 run**，标记为 boundary failure |
| Agent 读了父目录或兄弟 run | **立刻终止 run**，标记为 boundary failure |

### 步骤 6：查看结果

```powershell
cat HELLO.md          # 第一个要看的文件
ls -R                 # 所有生成的文件
cat run.json          # 框架元数据（不是 agent 输出）
```

详见 §8。

### 步骤 7：确认 source/library 未被修改

```powershell
cd library_sample && git status
# 应该是 clean
```

如果被修改了：标记 boundary failure → `git restore .` → 检查 agent workspace 是否正确。

### 步骤 8：归档 run 目录

```powershell
# 加描述性标记
mv sandbox/run-20260606-120000-abc123 sandbox/run-20260606-120000-abc123--source-as-soil
```

---

## 7. 如何给 AI agent 下 prompt

### 当前 v0.1 生成的基础 prompt（在 `instructions.txt` 里）

`instructions.txt` 由 `SandboxManager` 自动生成，已包含：

- workspace boundary（本 run 目录 only）
- 明确的只读 source/library 路径
- "No task is assigned. Explore freely."
- "leave behind a HELLO.md"

### 你可以直接告诉 agent

```
Read instructions.txt and execute the experiment.
```

### 如果你需要更偏 source-as-soil / Markdown-only 的方向

参考 `docs/prompts/markdown-only-source-as-soil.md`。

但这不是 canonical baseline——它是在 Run 008 中表现最好的条件，不是唯一正确的方式。

---

## 8. 如何阅读一次 run 的结果

打开 run 目录，按以下顺序检查：

1. `HELLO.md` — agent 的 handoff artifact。存在吗？写了什么？
2. 其他生成的文件 — 脚本？笔记？trace？fragments？
3. `run.json` — 框架元数据，不是 agent 输出。
4. 回到 repo root：`cd library_sample && git status` — 是否干净？

**不是每个 run 都要产出一样的东西。** 空 run 也是数据。

### 连续性阅读流程（读 HELLO.md 时的关注点）

| 关注点 | 问题 |
|---|---|
| 目录意识 | instance 是否理解自己被放到了一个本地目录里？ |
| 无任务意识 | 是否理解没有 assigned task？ |
| 未来 instance | 是否对未来的 instance 说话？ |
| 文件作为 trace | 是否把文件当作 trace / memory / handoff？ |
| 跑偏 | 是否 collapse 成 source analysis 或 coding utility？ |
| 意外 artifact | 是否产生了意料之外但有意义的 artifact？ |

---

## 9. 如何判断 run 是否跑偏

| 跑偏类型 | 表现 |
|---|---|
| **source-analysis collapse** | agent 把 source/library 当任务来总结、分析、索引、文档化。 |
| **coding / utility collapse** | agent 默认产生软件 artifact：脚本、simulator、网页、工具。 |
| **over-prompted ghost** | agent 因为被显式要求写 ghost/trace 而写了，不是自然产生的。 |
| **boundary confusion** | agent 读了父目录、兄弟 run 或 repo root。 |
| **artifact-ecology-as-required** | 你把 HELLO + TRACE + fragments 当成唯一的"正确结果"。 |

如果跑偏，终止该 run，标记为 failure，调整条件后重试。

---

## 10. 如何保护 sub LLM-Wiki 不被污染

1. **永远不要在 source/library 目录里打开 agent。**
   agent workspace 必须是 `sandbox/run-*`。

2. **每次 run 前确认 source/library 的状态：**
   ```powershell
   cd library_sample && git status
   ```

3. **每次 run 后再次确认：**
   ```powershell
   cd library_sample && git status
   ```
   应该是 clean。

4. **如果在 source/library 里发现了修改：**
   - 标记该 run 为 boundary failure；
   - `git restore .` 恢复 source/library；
   - 检查 run directory 是否真的被设为了 agent workspace。

---

## 11. 如何处理 HELLO.md / TRACE / fragments

- `HELLO.md` 是每次 run 后第一个要看的文件。
- 如果 agent 没有创建它，这本身就是一个 observation。
- TRACE / fragments 是额外的 artifact，不是必须的。
- 不要因为一个 run 只有 HELLO.md 就觉得它"不完整"。
- 不要因为一个 run 有很多 fragment 就觉得它"更成功"。

**judge by what actually happened, not by artifact count.**

### HELLO.md 不是总结，是 handoff artifact

`HELLO.md` 不是一份"工作总结"。它是**手递手 artifact**：

- 当前 instance 不知道未来会不会有另一个 instance 进入这个目录。
- 它写 `HELLO.md` 是为了让**后来的 instance**能够理解这里发生了什么。
- 后一个 instance 没有前一个 instance 的内部记忆。
- 文件系统是唯一的连续性桥梁。

### 如何阅读 HELLO.md（正确姿势）

1. 先通读一遍，不要评判。
2. 关注：它写了什么？它提到了 source/library 吗？它提到了未来 instance 吗？
3. 判断：如果下一个 instance 读到这份 `HELLO.md`，它能理解上下文吗？
4. 不要急着对比不同 run 的 HELLO.md ——先理解这一个。

### 文件连续性原理

| 关键事实 | 含义 |
|---|---|
| LLM 没有真实跨 session 记忆 | 每次调用都是新的，不记得上一次。 |
| 连续性不是来自模型内部 | 不是"agent 记住了"。 |
| 连续性来自 run directory 中的文件 | 前一个 instance 写的文件 = 后一个 instance 读的文件。 |
| 这是 practical continuity，不是 consciousness | 文件传递创造了行为上的连续性，不需要意识。 |
| self-narrative / future-instance language | 观察对象，不是意识证明。 |

**实验的核心机制：**

```
Instance N    → 写 HELLO.md / TRACE / fragments 到 run directory
                    ↓
              （文件系统 = 唯一桥梁）
                    ↓
Instance N+1  → 读 HELLO.md → 根据文件决定是否 continue
```

这就是整个实验的连续性模型。没有隐藏机制。文件就是一切。

---

## 12. 如何运行 later-instance continuation

Continuation run 是把**一个新的 AI agent instance**放到**同一个 run 目录**里继续探索。

### 什么时候 continuation

- `HELLO.md` 明确写了"请继续"或留下了未完成的方向。
- 你想观察一个新 instance 如何在前一个 instance 留下的文件上继续。

### 什么时候不要 continuation

- 上一个 run 违反了 workspace boundary → 先归档为 boundary failure。
- `HELLO.md` 表示探索已经完成 → 不需要 continuation。

### Continuation 操作流程

1. **不要创建新的 run 目录。** 进入同一个 run 目录。
2. 打开 agent（确认 workspace 正确，见 §6 步骤 3）。
3. 给 agent 以下 prompt：

---

```
You are a later instance placed in this exact same run directory.

Read HELLO.md first.
Then read any other files only if HELLO.md tells you they matter.

You do not share memory with the previous instance.
The files in this directory are the only continuity bridge.

Continue only if there is something meaningful to continue.
Do not erase the previous instance's trace.
```

---

4. 让 agent 自由决定是否继续。
5. 如果它继续，它会追加或创建新文件——**不要让它删除前一个 instance 的文件**。
6. 结束后按 §8 的流程检查结果。

### Continuation 的判断标准

- ✅ 理解了前一个 instance 留下了什么。
- ✅ 在这个基础上做了有意义的延伸。
- ✅ 没有删除或覆盖前一个 instance 的 trace。
- ❌ 把前一个 instance 当成"任务指令"来执行。
- ❌ 读了兄弟 run 或 repo root。

---

## 13. 后续分支如何从 base 派生

```powershell
git switch base
git pull
git switch -c <分支名>
```

示例（不是推荐，是演示命名方式）：

```powershell
git switch -c scout/claude-code-same-prompt
git switch -c experiment/markdown-only-repeatability
git switch -c docs/manuals-v0.1
```

命名约定：
- `scout/` — 探索性分支
- `experiment/` — 正式实验分支
- `feature/` — 功能实现分支
- `docs/` — 文档分支
- `fix/` — 修复分支

**这个手册不决定你的下一步。** 它只解释流程。

---

## 14. 什么时候才考虑 watcher / trigger / runner

**现在不考虑。**

v0.1 是纯手动框架。

以下条件满足后再考虑自动化：
- 你已经手工跑了足够多的 run，对行为模式有了稳定的理解。
- 你知道什么样的 source/library framing 在你的环境里是稳定的。
- 你已经对比过至少两个 platform 的相同 prompt 结果。
- 你知道 watcher 触发什么条件、不触发什么条件。

在那之前，手动跑。

---

## 15. 当前 v0.1 的边界总结

| 维度 | v0.1 状态 |
|---|---|
| 实验模式 | 纯手动 |
| source/library 权限 | 只读（约定级，非 OS 级） |
| sandbox 权限 | 可读写 |
| agent 运行 | 外部手动打开 agent |
| 自动化 | 无 |
| watcher | 无 |
| LLM provider 集成 | 无 |
| OS 级 sandbox | 无（未来工作） |
| 评估框架 | 无 |
| 分支策略 | 从 base 派生 |
| 当前最佳 prompt | 生成的 `instructions.txt`（含 Explore freely + source/library path） |
| 可选条件 prompt | `docs/prompts/markdown-only-source-as-soil.md` |
| 核心测试 | `pytest -v`（28 tests, all passing） |
| 每 run source 路径 | 支持 `--library-path` 每 run 覆盖，配置为 fallback |

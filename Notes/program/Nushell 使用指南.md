# Nushell 使用指南（Windows）

> 本篇实测环境：Windows 11 (26100)、Nushell 0.114.1（build 2026-07-11，实测即当前最新版）、通过 Scoop 安装。文中所有命令输出均为本机实跑结果，实测日期 2026-08-11。

## 一、Nushell 解决什么问题

传统 shell（bash / cmd / Git Bash）的管道传递的是**纯文本字节流**。这带来一个根本性的麻烦：每个命令都要自己解析上一个命令的文本输出，于是我们不得不写出这种东西：

```bash
# bash：找出内存占用最高的 3 个进程
ps aux | sort -k4 -rn | head -3 | awk '{print $11, $4}'
```

这里的 `-k4`、`$11`、`$4` 是**列位置的硬编码**。换个系统、换个 `ps` 版本、进程名里多个空格，整条命令就崩了。`awk`/`sed`/`cut` 的存在，本质上是在给"文本流"这个错误的抽象打补丁。

PowerShell 走对了一步——管道传对象。但它的命令名冗长（`Get-ChildItem`）、语法笨重、启动慢，且是 Windows 强绑定。

**Nushell 的答案：管道里传的是结构化数据（表格 / 记录 / 列表），命令按列名操作。**

```nu
# nushell：同样的需求
ps | sort-by mem --reverse | first 3 | select name pid mem
```

实测输出：

```
╭───┬──────────────────┬───────┬──────────╮
│ # │       name       │  pid  │   mem    │
├───┼──────────────────┼───────┼──────────┤
│ 0 │ UnrealEditor.exe │  9636 │   8.2 GB │
│ 1 │ maya.exe         │ 30904 │   2.9 GB │
│ 2 │ Weixin.exe       │ 30412 │ 588.7 MB │
╰───┴──────────────────┴───────┴──────────╯
```

注意几个细节：`mem` 自动格式化为人类可读的 `8.2 GB`（内部仍是精确的 filesize 类型，可直接参与数值比较）；没有一处列位置硬编码；输出自带表格边框。

### 定位对比

| Shell | 管道数据 | 跨平台 | 适合 |
|---|---|---|---|
| bash / Git Bash | 文本流 | 是 | 兼容一切现有脚本、POSIX 生态 |
| PowerShell | .NET 对象 | 部分 | Windows 系统管理、注册表、WMI |
| **Nushell** | **结构化表格** | 是（Rust 单文件） | 数据查询/统计/转换、批量资产处理 |

**Nushell 不是 bash 的替代品**，它是**数据处理专用 shell**。它的语法与 POSIX 不兼容，你不能把网上的 bash 脚本粘进去跑。理性的用法是二者并存：Git 操作和现成脚本用 Git Bash（见 [Git Bash 使用指南](Git%20Bash%20使用指南.md)），需要统计/过滤/转格式时切到 Nushell。

> 版本提醒：Nushell 尚未到 1.0，**小版本间存在破坏性变更**。本篇基于 0.114.1，抄旧博客的命令时注意核对 `help <命令>`。

---

## 二、安装

```powershell
# Scoop（推荐，本机即此方式，见 Scoop使用入门）
scoop install nu

# winget
winget install nushell

# cargo（需要 Rust 工具链）
cargo install nu --locked
```

验证：

```nu
$ nu -c 'version | select version build_time'
╭────────────┬────────────────────────────╮
│ version    │ 0.114.1                    │
│ build_time │ 2026-07-11 16:22:26 +00:00 │
╰────────────┴────────────────────────────╯
```

从 Git Bash 里也能直接调用（实测通过），这对渐进式采用很友好：

```bash
$ nu -c 'echo "从 bash 调 nu 成功"'
从 bash 调 nu 成功
```

### 配置文件位置

实测本机路径（Windows 是 `AppData\Roaming\nushell`，**不是** `~/.config`）：

```nu
$ nu -c '$nu.config-path'
C:\Users\dalaotian\AppData\Roaming\nushell\config.nu

$ nu -c '$nu.env-path'
C:\Users\dalaotian\AppData\Roaming\nushell\env.nu
```

- `env.nu` —— 环境变量、`PATH` 设置，先加载
- `config.nu` —— 别名、自定义命令、外观设置，后加载

用 `config nu` / `config env` 命令可直接在编辑器里打开它们。

---

## 三、核心概念：一切皆数据

### 3.1 三种基本形态

| 形态 | 说明 | 例子 |
|---|---|---|
| **记录 record** | 键值对，类似字典 | `{name: "maya", pid: 30904}` |
| **列表 list** | 有序值序列 | `[1 2 3]` |
| **表格 table** | 记录的列表（最常用） | `ls`、`ps` 的输出 |

`describe` 命令随时告诉你手里是什么类型——排查问题的第一手段：

```nu
$ nu -c '$env.Path | describe'
list<string>
```

**这里就有一个 Windows 特有的重要细节**：Nushell 把 `PATH` 环境变量解析成了**字符串列表**而非分号拼接的长字符串。实测本机有 49 个条目：

```nu
$ nu -c '$env.PATH | length'
49
```

所以追加路径是列表操作，不是字符串拼接：

```nu
$env.PATH = ($env.PATH | prepend 'D:\MyTools\bin')
```

> 注意 Windows 上环境变量名大小写不敏感，`$env.PATH` 和 `$env.Path` 都能用。

### 3.2 表格操作核心命令

按使用频率排序，这几个覆盖 80% 场景：

| 命令 | 作用 | 类比 SQL |
|---|---|---|
| `where` | 按条件筛选行 | `WHERE` |
| `select` | 挑选列 | `SELECT` |
| `sort-by` | 排序（`--reverse` 降序） | `ORDER BY` |
| `first n` / `last n` | 取前/后 n 行 | `LIMIT` |
| `get <列>` | 取出某列的值（降维成列表） | — |
| `each {\|it\| ... }` | 逐行处理 | `map` |
| `group-by` | 分组 | `GROUP BY` |
| `length` | 行数 | `COUNT(*)` |
| `math sum` / `math avg` | 聚合 | `SUM` / `AVG` |
| `transpose` | 行列转置 | — |
| `flatten` / `uniq` / `reverse` | 展平 / 去重 / 反转 | — |

Nushell 0.114 实测的命令分布（说明它的重心在哪）：

```nu
$ nu -c 'help commands | select name category | group-by category
         | transpose cat items | each {|r| {分类: $r.cat, 数量: ($r.items | length)}}
         | sort-by 数量 --reverse | first 6'
╭───┬────────────┬──────╮
│ # │    分类    │ 数量 │
├───┼────────────┼──────┤
│ 0 │ filters    │   77 │
│ 1 │ core       │   70 │
│ 2 │ strings    │   48 │
│ 3 │ formats    │   40 │
│ 4 │ math       │   31 │
│ 5 │ filesystem │   25 │
╰───┴────────────┴──────╯
```

`filters`（77 个）是最大的一类——这就是 Nushell 的定位：数据过滤与变换。

### 3.3 文件系统即表格

`ls` 返回的是真表格，可以直接查询：

```nu
# 最大的 3 个文件
$ nu -c 'ls C:\Windows | where type == file | sort-by size --reverse | first 3 | select name size'
╭───┬─────────────────────────┬────────╮
│ # │          name           │  size  │
├───┼─────────────────────────┼────────┤
│ 0 │ C:\Windows\PFRO.log     │ 3.3 MB │
│ 1 │ C:\Windows\setupact.log │ 3.1 MB │
│ 2 │ C:\Windows\explorer.exe │ 3.0 MB │
╰───┴─────────────────────────┴────────╯

# 统计目录内所有 md 文件总大小（实测知识库 program 目录）
$ nu -c 'ls D:\Learning-Notes\Notes\program\*.md | get size | math sum'
136.4 kB

# 递归 glob（注意必须用正斜杠，见第六章）
$ nu -c 'glob "D:/Learning-Notes/Notes/program/**/*.md" | length'
312
```

`size` 是 `filesize` 类型，可以直接写 `where size > 10mb` 这样的比较，无需单位换算。

---

## 四、数据格式转换（最实用的功能）

Nushell 内置 40 个 `formats` 类命令，`open` 会**按扩展名自动解析**结构化文件：

```nu
# CSV 自动解析成表格，直接查询——注意 size 是数字类型，能做数值比较
$ nu -c "open 'C:\...\t.csv' | where size > 15"
╭───┬──────┬──────╮
│ # │ name │ size │
├───┼──────┼──────┤
│ 0 │ b    │   25 │
╰───┴──────┴──────╯
```

支持的格式：`json` `yaml` `toml` `csv` `tsv` `xml` `ini` `sqlite` `parquet` `xlsx` `ods` 等。

`to xxx` 系列做反向输出：

```nu
$ nu -c 'sys host | select name os_version | to json'
{
  "name": "Windows",
  "os_version": "11 (26100)"
}

# 直接生成 Markdown 表格——写笔记时极其方便
$ nu -c 'ls C:\Windows\System32\drivers\etc | select name size | to md'
| name | size |
| --- | --- |
| C:\\Windows\\System32\\drivers\\etc\\hosts | 2.6 kB |
| C:\\Windows\\System32\\drivers\\etc\\hosts.ics | 435 B |
...

$ nu -c 'ps | first 2 | select name pid | to csv'
name,pid
winlogon.exe,1756
svchost.exe,1936
```

`to md` 值得单独说：**它让"统计资产 → 生成报告表格 → 贴进 Obsidian 笔记"变成一条管道**，不用手动排版。

### HTTP 请求内置

不需要 `curl` + `jq` 两级管道，`http get` 直接返回解析好的结构：

```nu
$ nu -c 'http get https://api.github.com/repos/nushell/nushell | select name stargazers_count'
╭──────────────────┬─────────╮
│ name             │ nushell │
│ stargazers_count │ 40244   │
╰──────────────────┴─────────╯
```

对比 bash 里的 `curl -s ... | jq -r '.stargazers_count'`——而且 Git Bash **不自带 `jq`**（实测确认），这一条就省掉一个依赖。

---

## 五、语言特性

### 5.1 变量、循环、自定义命令

```nu
# 变量不可变（let），可变用 mut
let xs = [1 2 3]
$xs | each {|x| $x * 2} | math sum      # 实测输出 12

# 自定义命令，支持类型标注
def greet [name: string] { $"你好, ($name)!" }
greet 世界                              # 实测输出：你好, 世界!
```

`$"...(表达式)..."` 是字符串插值语法——注意用**圆括号**，不是 bash 的 `${}`。

### 5.2 错误处理

```nu
$ nu -c 'try { open nonexist.txt } catch { |e| "捕获到错误" }'
捕获到错误
```

比 bash 的 `if [ $? -ne 0 ]` 清晰得多。

### 5.3 调用外部命令并结构化其输出

这是新旧世界的桥梁。用 `^` 前缀显式调用外部程序，再把文本切成表格：

```nu
$ nu -c '(^git log -1 --format="%h|%s") | split column "|" hash subject'
╭───┬─────────┬───────────────────────────────────╮
│ # │  hash   │              subject              │
├───┼─────────┼───────────────────────────────────┤
│ 0 │ e5a8f73 │ vault backup: 2026-08-11 13:59:57 │
╰───┴─────────┴───────────────────────────────────╯

# 判断工作区是否干净
$ nu -c '^git status --porcelain | lines | length'
0
```

`lines`（切行）、`split column`（切列）、`split row`、`parse`（模式提取）是把任意命令行工具的文本输出接入 Nushell 管道的四件套。

### 5.4 正则与路径处理

```nu
# where 支持 =~ 正则匹配
$ nu -c 'ps | where name =~ "maya|Unreal" | select name pid'
╭───┬───────────────────────┬───────╮
│ # │         name          │  pid  │
├───┼───────────────────────┼───────┤
│ 0 │ maya.exe              │ 30904 │
│ 1 │ UnrealEditor.exe      │  9636 │
│ 2 │ UnrealTraceServer.exe │ 15036 │
╰───┴───────────────────────┴───────╯

# path 命令族处理路径，跨平台安全
$ nu -c 'ls C:\Windows\System32\drivers\etc | get name | path basename'
hosts
hosts.ics
...
```

`path basename` / `path dirname` / `path join` / `path exists` / `path expand` 比手写字符串切割可靠。

### 5.5 从 stdin 读入

**这是个容易踩的坑**：`nu -c` 默认不接管道输入，必须加 `--stdin`。

```nu
# 错误：报 "Pipeline empty"
$ echo '{"a":1}' | nu -c 'from json | get a'
Error: nu::shell::pipeline_mismatch  x Pipeline empty.

# 正确
$ echo '{"a":1,"b":2}' | nu --stdin -c 'from json | get a'
1

# 或显式用 $in 引用输入
$ echo '{"a":1}' | nu --stdin -c '$in | from json | get a'
1
```

`$in` 表示"管道里传进来的值"，在闭包和自定义命令里都用它。

---

## 六、坑点（Windows 重点）

### 6.1 不认 MSYS 的 `/c/` 路径（从 Git Bash 切过来必踩）

Nushell 是**原生 Windows 程序**，不经过 MSYS 路径层。它不认识 `/c/Windows` 这种写法：

```nu
$ nu -c 'ls /c/Windows'
Error: nu::shell::io::not_found
  help: 'C:\c\Windows' does not exist
```

看错误信息——它把 `/c/Windows` 当成了当前盘符下的相对路径 `C:\c\Windows`。

**正确写法**：用 Windows 原生路径。

```nu
ls C:\Windows                      # 反斜杠可以（在 ls 等命令的路径参数里）
ls "C:/Windows"                    # 正斜杠也可以，更安全
```

从 Git Bash 传路径给 `nu` 时，先用 `cygpath` 转换：

```bash
nu -c "open '$(cygpath -w /tmp/t.csv)' | where size > 15"    # 实测可用
```

### 6.2 `glob` 命令必须用正斜杠

这是上一条的延伸，但更隐蔽——`ls` 能吃反斜杠，`glob` **不能**：

```nu
# 失败
$ nu -c 'glob D:\Learning-Notes\Notes\program\**\*.md | length'
Error: x error with glob pattern
  `-- failed to parse glob expression

# 单引号包裹反斜杠也一样失败
$ nu -c "glob 'D:\Learning-Notes\...\*.md' | length"
Error: x error with glob pattern

# 正确：正斜杠 + 引号
$ nu -c 'glob "D:/Learning-Notes/Notes/program/**/*.md" | length'
312
```

原因是 glob 语法里反斜杠是**转义字符**，与 Windows 路径分隔符冲突。**结论：所有 glob 模式一律写正斜杠并加引号。**

### 6.3 不兼容 POSIX，现有脚本一律不能直接跑

- 没有 `&&` / `||` 串联（用 `;` 或 `try`）
- 重定向 `>` 语义不同（Nushell 用 `save` 命令落盘）
- `$?`、`$1`、`$@` 等 bash 变量不存在
- `export` 写法不同

所以别指望把 `.sh` 脚本改个后缀就能用。**迁移策略**：老脚本继续留在 Git Bash 跑，新写的数据处理任务用 Nushell。

### 6.4 版本不稳定，破坏性变更频繁

0.x 阶段每个小版本都可能改命令名或参数。已发生过的例子：`str find-replace` → `str replace`、`all?` → `all`、`build-string` 被移除。

**自保办法**：
- 遇到网上的命令报错，先 `help <命令>` 或 `help commands | where name =~ "关键词"` 查当前版本的真实签名。
- 自己的脚本在文件头注释里写明基于哪个版本（如 `# nu 0.114.1`）。
- 官方 changelog 每个版本都有 breaking changes 章节，升级前扫一眼。

### 6.5 外部命令的 stdout 是纯文本

Nushell 只能对**自己的内置命令**返回结构化数据。`^git`、`^maya`、`^ffmpeg` 的输出仍是字符串，需要手动用 `lines` / `split column` / `parse` / `from json` 转换（见 5.3）。别以为切了 shell 就自动结构化了。

### 6.6 交互体验的小问题

- 补全和语法高亮很强，但对 Windows 上某些 `.exe` 的参数补全无能为力。
- 启动速度比 bash 略慢（Rust 二进制加载 + 配置解析），做 Git 钩子这类高频短命令调用时不划算。
- 表格宽度超出终端会被截断，用 `| table --expand` 或直接 `to json` 看完整数据。

---

## 七、实用场景（TA 向）

结合游戏动画绑定的日常工作，几个立刻能用的组合：

```nu
# 1. 统计资产目录里各类文件的数量和总大小
ls D:\X12RawFile\CharactersArt\**\* | where type == file
  | insert ext {|r| $r.name | path parse | get extension}
  | group-by ext
  | transpose 扩展名 文件
  | each {|r| {扩展名: $r.扩展名, 数量: ($r.文件 | length), 总大小: ($r.文件 | get size | math sum)}}
  | sort-by 总大小 --reverse

# 2. 找出一周内改动过的 Maya 场景文件
ls D:\X12RawFile\**\*.ma | where modified > ((date now) - 7day) | select name modified size

# 3. 查 DCC 软件当前内存占用（排查 Maya/UE 卡顿）
ps | where name =~ "maya|Unreal|MotionBuilder" | select name pid mem cpu | sort-by mem --reverse

# 4. 批量检查绑定脚本里是否残留 print 调试语句
glob "D:/X12RawFile/CharactersArt/Common/X12RigAnimTools/scripts/**/*.py"
  | each {|f| {文件: ($f | path basename), 次数: (open $f | lines | where $it =~ '^\s*print\(' | length)}}
  | where 次数 > 0

# 5. 把统计结果直接变成 Obsidian 笔记里的 Markdown 表格
ls D:\X12RawFile\CharactersArt\**\*.fbx | select name size modified | to md

# 6. 读取项目配置并查询
open pyproject.toml | get project.dependencies
```

第 4 和第 5 条是 Nushell 相对 bash 优势最明显的地方：前者在 bash 里要写嵌套循环 + `grep -c`，后者要手工排版。

---

## 八、参考链接

以下链接均已实测返回 200：

- 官方文档（The Nushell Book）：<https://www.nushell.sh/book/>
- 快速上手：<https://www.nushell.sh/book/quick_tour.html>
- 配置说明：<https://www.nushell.sh/book/configuration.html>
- 命令参考（按分类可查全部命令）：<https://www.nushell.sh/commands/>
- Cookbook（实战范例，含从 bash 迁移的对照）：<https://www.nushell.sh/cookbook/>
- GitHub 仓库（changelog 与 breaking changes）：<https://github.com/nushell/nushell>

---

> 相关笔记：[Git Bash 使用指南](Git%20Bash%20使用指南.md)（POSIX 工具链，与本篇互补；两者路径写法不通用，见本篇 6.1）、[PowerShell入门](PowerShell入门.md)（同为对象管道 shell）、[Scoop使用入门](Scoop使用入门.md)（本篇安装方式）

# Git Bash 使用指南（Windows）

> 本篇实测环境：Windows 11 (26100)、Git for Windows 2.54.0、bash 5.3.9(1)-release (x86_64-pc-cygwin)、MSYSTEM=MINGW64。文中所有命令输出均为本机实跑结果，实测日期 2026-08-11。

## 一、Git Bash 解决什么问题

Windows 原生只有 `cmd` 和 PowerShell，两者的命令名、路径分隔符、脚本语法都与 Linux/macOS 不兼容。而我们日常接触的绝大多数技术资料——Maya/MotionBuilder 的构建脚本、Python 项目的 `Makefile`、开源库的 `README`、CI 配置——都是按 POSIX shell 写的。

Git Bash 是 Git for Windows 附带的一套 **MSYS2 精简运行时 + GNU 工具链**，它让你在 Windows 上直接跑 `ls`、`grep`、`sed`、`awk`、`ssh`、`curl`、`tar` 这些命令，把 Linux 教程里的命令原样粘过来就能用。

它和相关方案的区别：

| 方案 | 本质 | 适合场景 |
|---|---|---|
| **Git Bash** | MSYS2 运行时，POSIX 层模拟，直接操作真实 Windows 文件系统 | 日常 Git 操作、跑 POSIX 脚本、SSH、跨平台工具链 |
| WSL2 | 真正的 Linux 内核虚拟机 | 需要完整 Linux 环境（Docker、systemd、apt） |
| MSYS2（完整版） | 带 `pacman` 包管理的完整 MSYS2 | 需要编译 GNU 工具链、装大量 Unix 软件包 |
| Cygwin | 更彻底的 POSIX 兼容层 | 遗留项目，现在较少用 |
| PowerShell | .NET 对象管道 | Windows 系统管理、注册表、WMI、AD |

**要点**：Git Bash 不是虚拟机，`D:\X12RawFile` 在它眼里就是 `/d/X12RawFile`，读写的是同一份文件。这既是它最方便的地方，也是路径转换坑的根源（见第五章）。

相关笔记：[Windows 命令提示符入门](Windows%20%E5%91%BD%E4%BB%A4%E6%8F%90%E7%A4%BA%E7%AC%A6%E5%85%A5%E9%97%A8.md)、[PowerShell入门](PowerShell%E5%85%A5%E9%97%A8.md)、[Nushell 使用指南](Nushell%20%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)。

---

## 二、安装与启动

### 2.1 安装

Git Bash 随 Git for Windows 一起安装，官方下载：<https://git-scm.com/downloads/win>

也可以用包管理器（推荐，便于统一升级，见 [Scoop使用入门](Scoop%E4%BD%BF%E7%94%A8%E5%85%A5%E9%97%A8.md)）：

```powershell
# Scoop
scoop install git

# 或 winget
winget install --id Git.Git -e
```

安装向导里有几个选项值得注意：

| 选项 | 建议 | 原因 |
|---|---|---|
| Adjusting your PATH environment | **Git from the command line and also from 3rd-party software** | 让 `cmd`/PowerShell/VSCode 都能调 `git` |
| Choosing the SSH executable | Use bundled OpenSSH | 除非你已经在用 Windows 自带 OpenSSH 的 agent |
| Configuring the line ending conversions | **Checkout as-is, commit as-is**（`core.autocrlf=false`） | 见第五章 CRLF 一节。选 `true` 会在跨平台协作和二进制/中文文件上引入隐性差异 |
| Choosing the terminal emulator | MinTTY（默认） | MinTTY 体验好，但对原生控制台程序需要 `winpty`（见 5.3） |
| Enable experimental support for pseudo consoles | 可开 | 开启后 `python -i` 之类的交互程序不再需要 `winpty` 前缀 |

验证安装：

```bash
$ bash --version
GNU bash, version 5.3.9(1)-release (x86_64-pc-cygwin)

$ git --version
git version 2.54.0.windows.1

$ uname -a
MINGW64_NT-10.0-26100 ... x86_64 Msys
```

### 2.2 三种启动方式

1. **开始菜单 / 桌面右键**：安装后资源管理器右键菜单有 "Open Git Bash here"，会直接 `cd` 到当前目录，最常用。
2. **`git-bash.exe`**：位于 `C:\Program Files\Git\git-bash.exe`，可以带参数启动：
   ```cmd
   "C:\Program Files\Git\git-bash.exe" --cd=D:\X12RawFile
   ```
3. **集成到终端/编辑器**：在 Windows Terminal 或 VSCode 里把 Git Bash 设为一个 profile。VSCode 的 `settings.json`：
   ```json
   {
     "terminal.integrated.profiles.windows": {
       "Git Bash": {
         "path": "C:\\Program Files\\Git\\bin\\bash.exe",
         "args": ["--login", "-i"]
       }
     },
     "terminal.integrated.defaultProfile.windows": "Git Bash"
   }
   ```

### 2.3 MSYSTEM 与目录布局

Git Bash 启动时会设置 `MSYSTEM=MINGW64`，这决定了 `PATH` 里 `/mingw64/bin` 的优先级。实测本机工具来源：

```bash
$ which git ssh curl openssl awk sed
/mingw64/bin/git        # MinGW 原生 Windows 编译版
/usr/bin/ssh            # MSYS2 POSIX 层
/mingw64/bin/curl
/mingw64/bin/openssl
/usr/bin/awk
/usr/bin/sed
```

对应的真实磁盘位置：

| Git Bash 路径 | 实际 Windows 路径 |
|---|---|
| `/` | `C:\Program Files\Git\` |
| `/usr/bin` | `C:\Program Files\Git\usr\bin`（MSYS2 工具） |
| `/mingw64/bin` | `C:\Program Files\Git\mingw64\bin`（原生 Windows 工具） |
| `/c`、`/d` | `C:\`、`D:\` |
| `~`、`$HOME` | `C:\Users\<你>`（实测 `HOME=/c/Users/dalaotian`） |

**注意 `/` 不是 `C:\`**，而是 Git 的安装目录。这条是第五章 `/nologo` 误伤坑的直接原因。

---

## 三、随附工具清单

Git Bash 自带的工具比多数人以为的多。本机实测可用（`—` 表示不自带）：

| 类别 | 可用 | 不自带（需另装） |
|---|---|---|
| 文本处理 | `grep` `sed` `awk` `cut` `sort` `uniq` `tr` `wc` `head` `tail` `column` `diff` `patch` | `jq` `rg` `fd` |
| 文件操作 | `ls` `cp` `mv` `rm` `mkdir` `find` `xargs` `ln` `du` `df` `file` `stat` | `rsync` `tree` |
| 网络 | `curl` `ssh` `scp` `sftp` `ssh-keygen` `ssh-agent` `openssl` | `wget` `nc` |
| 压缩 | `tar` `gzip` `bzip2` `unzip` `zip` | `7z` |
| 编辑器 | `vim` `nano` | `emacs` |
| 脚本 | `bash` `perl` `sh` | `python`（用 Windows 的） |
| Windows 特有 | `cygpath` `winpty` `mintty` `start` | |

补装工具最省事的办法是用 Scoop 装 Windows 原生版，它们的 shim 在 `PATH` 里，Git Bash 直接就能调：

```bash
scoop install jq ripgrep fd 7zip
```

> `python` 在 Git Bash 里指向的是 Windows 上的 Python（本机是 `C:\Users\...\venv\Scripts\python.exe`），不是 MSYS 的 Python。这意味着它接收的是 **Windows 风格路径**，传 POSIX 路径给它会出问题——这正是 5.1 要讲的。

---

## 四、日常操作速查

### 4.1 路径与导航

```bash
cd /d/X12RawFile/CharactersArt/Common/X12RigAnimTools   # 盘符写成 /d/
cd ~                       # 回 C:\Users\<你>
cd "/c/Program Files/Git"  # 有空格必须加引号
cd -                       # 回上一个目录

# POSIX 路径 <-> Windows 路径互转，写脚本时的关键工具
$ cygpath -w /d/Learning-Notes    # -w 反斜杠 Windows 风格
D:\Learning-Notes
$ cygpath -m /d/Learning-Notes    # -m 正斜杠 Windows 风格（对付 Python/CMake 最好用）
D:/Learning-Notes
$ cygpath -u 'D:\Learning-Notes'  # -u 转回 POSIX
/d/Learning-Notes
```

`cygpath -m` 是给跨平台工具喂路径的最优解：既是 Windows 能认的绝对路径，又不含需要转义的反斜杠。

### 4.2 查找与文本处理

```bash
# 在代码库里找符号定义（Maya 工具库场景）
grep -rn --include='*.py' "def build_rig" /d/X12RawFile/CharactersArt/Common/X12RigAnimTools/scripts

# 找文件
find . -name "*.ma" -mtime -7          # 7 天内修改的 Maya 场景
find . -type f -name "*.pyc" -delete   # 清理

# 统计代码行数
find scripts -name '*.py' | xargs wc -l | tail -1

# 批量重命名（用 shell 循环，不要用 rename，各发行版行为不一致）
for f in *.jpg; do mv "$f" "prefix_$f"; done
```

### 4.3 Git 操作

Git Bash 最大的加分项是 `__git_ps1`——提示符里直接显示当前分支名，还有开箱即用的 Tab 补全（分支名、remote 名、文件名都能补）。

```bash
git status -sb                    # 简洁状态 + 分支追踪信息
git log --oneline --graph -20
git status --porcelain | wc -l     # 脚本里判断工作区是否干净
```

SSH 密钥配置（比在 PowerShell 里做顺手得多）：

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"   # 现在用 ed25519，不要再用 rsa
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub          # 复制到 GitHub/GitLab
ssh -T git@github.com              # 验证
```

详见 [全面掌握 Git 版本管理](%E5%85%A8%E9%9D%A2%E6%8E%8C%E6%8F%A1%20Git%20%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86.md) 和 [Git入门指南](Git%E5%85%A5%E9%97%A8%E6%8C%87%E5%8D%97.md)。

### 4.4 调用 Windows 程序

```bash
notepad file.txt            # .exe 后缀可省
explorer .                  # 在资源管理器打开当前目录
start .                     # 同上
cmd //c "dir /b"            # 调 cmd 内建命令，注意是双斜杠 //c
powershell -c "Get-Process" # 调 PowerShell

# 打开 Maya 场景
start "D:/X12RawFile/scene.ma"
```

`cmd //c` 的双斜杠不是笔误——单个 `/c` 会被 MSYS 当成路径转换掉，见 5.1。

### 4.5 配置文件

Git Bash 读取 `~/.bashrc`（即 `C:\Users\<你>\.bashrc`）。常用配置：

```bash
# ~/.bashrc
alias ll='ls -alF'
alias gs='git status -sb'
alias gl='git log --oneline --graph -20'

# 项目目录快捷跳转
alias rigtools='cd /d/X12RawFile/CharactersArt/Common/X12RigAnimTools'
alias notes='cd /d/Learning-Notes'

# 让 Windows 原生程序拿到正确路径的辅助函数
winpath() { cygpath -m "$1"; }

export EDITOR=vim
```

改完 `source ~/.bashrc` 生效。

---

## 五、坑点（重点章节）

这一章的每个结论都是本机实跑验证过的，不是从文档抄的。

### 5.1 MSYS 参数路径自动转换（最容易踩、最难 debug）

**现象**：Git Bash 调用 **Windows 原生程序**（`.exe`）时，MSYS 运行时会扫描命令行参数，把看起来像 POSIX 路径的参数自动改写成 Windows 路径。

实测（用一个打印 `sys.argv` 的 Python 脚本验证，**已清除环境中的抑制变量**）：

```bash
# 默认行为
$ python showargs.py /usr/bin /c/Users /nologo //server/share
ARGV: ['C:/Program Files/Git/usr/bin', 'C:/Users', 'C:/Program Files/Git/nologo', '//server/share']
```

看第三个参数：`/nologo` 这个**本来是命令行开关**，被当成路径拼上了 Git 安装目录，变成了 `C:/Program Files/Git/nologo`。任何以 `/` 开头的开关（`/S`、`/Q`、`/nologo`、`/p:Configuration=Release`）都会被这样误伤。这就是 MSBuild、`cmd /c`、部分 Autodesk 命令行工具在 Git Bash 里莫名失败的根因。

**三种解法，实测对照**：

```bash
# 解法1：单参数双斜杠转义（推荐，最精准，无副作用）
$ python showargs.py //nologo
ARGV: ['/nologo']

# 解法2：MSYS_NO_PATHCONV=1 —— 全局关闭转换
$ MSYS_NO_PATHCONV=1 python showargs.py /usr/bin /c/Users /nologo //server/share
ARGV: ['/usr/bin', '/c/Users', '/nologo', '//server/share']

# 解法3：MSYS2_ARG_CONV_EXCL='*' —— 等效，MSYS2 官方变量
$ MSYS2_ARG_CONV_EXCL='*' python showargs.py /usr/bin /c/Users /nologo //server/share
ARGV: ['/usr/bin', '/c/Users', '/nologo', '//server/share']
```

`MSYS2_ARG_CONV_EXCL` 还能只排除特定前缀，但实测它是**前缀匹配而非精确匹配**，且只作用于匹配到的参数，其余参数照常转换：

```bash
$ MSYS2_ARG_CONV_EXCL='/nologo' python showargs.py /usr/bin /nologo
ARGV: ['C:/Program Files/Git/usr/bin', '/nologo']   # /usr/bin 仍被转换
```

**实践建议**：
- 只有个别参数出问题 → 用 `//` 双斜杠。
- 整条命令都不该转换（调 MSBuild、Docker、`p4`）→ 命令前加 `MSYS_NO_PATHCONV=1`。
- 反过来，需要给原生程序传**真实路径**时，用 `cygpath -m` 主动转换，不要依赖自动转换：
  ```bash
  python my_tool.py --scene "$(cygpath -m /d/X12RawFile/scene.ma)"
  ```

> **坑中坑（本次实测踩到的）**：某些终端宿主（如 Hermes Agent 的 terminal 工具）会预设 `MSYS_NO_PATHCONV=1` 和 `MSYS2_ARG_CONV_EXCL=*`。此时你测出来的"默认行为"根本不是默认行为。排查前先 `env | grep -i -E "msys|conv"` 确认，用 `env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL <命令>` 在干净环境下复现。

MSYS2 官方对路径规则的说明：<https://www.msys2.org/docs/filesystem-paths/>

### 5.2 CRLF 行尾

Windows 用 `\r\n`，POSIX 工具期望 `\n`。混用时的典型症状：

```bash
$ printf 'a\r\nb\r\n' > crlf.txt
$ file crlf.txt
crlf.txt: ASCII text, with CRLF line terminators

$ grep -c 'a$' crlf.txt    # 期望 1，行尾锚点被 \r 挡住时会是 0
```

**处理办法**：
```bash
tr -d '\r' < file.txt              # 临时剥离 \r 读取（管道友好）
dos2unix file.txt                  # 永久转换（Git Bash 自带）
sed -i 's/\r$//' file.txt          # 同上
```

**Git 侧配置建议**：

```bash
git config --global core.autocrlf false   # 本机实测为未设置（等效 false）
git config --global core.quotepath false  # 让 git status 正常显示中文文件名，不转义成 \344\275\240
```

对团队项目，比 `core.autocrlf` 更可靠的是在仓库里放 `.gitattributes`：

```gitattributes
* text=auto eol=lf
*.bat text eol=crlf
*.ma binary
*.mb binary
*.fbx binary
*.uasset binary
```

> 一个真实场景：中文密集 + CRLF 的 `.md` 文件会被某些工具误判为二进制（Hermes 的 `read_file` 就会返回 `is_binary: true`），此时 `tr -d '\r' < file.md` 读取是可靠的绕过方式。

### 5.3 交互式程序需要伪终端

MinTTY 不是 Windows 控制台，原生控制台程序（Python REPL、`node`、`mysql`、`ipython`）在里面可能不显示提示符或直接卡死。

```bash
winpty python          # 用 winpty 包一层
winpty node
```

或在安装时勾选 "Enable experimental support for pseudo consoles"，之后就不需要 `winpty` 了（本机已开启，实测 `python -i` 直接可用）。

另一个绕法是显式走管道/非交互模式：`python -c "..."`、`echo 'cmd' | python`。

### 5.4 `cmd //c` 与中文乱码

调 `cmd` 内建命令要写双斜杠：`cmd //c "dir /b"`。若输出中文乱码，是代码页问题：

```bash
cmd //c "chcp 65001 >nul && your_command"
```

MinTTY 本身对 UTF-8 支持良好，中文文件名实测无碍：

```bash
$ ls -1 *.txt
测试文件.txt
```

但要保证 `LANG` 是 UTF-8（Git Bash 默认如此），且 Windows 程序的输出编码通常是 GBK，跨程序管道时可能需要 `iconv -f gbk -t utf-8`。

### 5.5 `/` 不是 C 盘

前面说过 `/` = `C:\Program Files\Git\`。所以 `ls /etc` 看到的是 Git 自己的 `etc`，不是什么系统目录；写脚本时想指 C 盘根必须写 `/c/`。

### 5.6 权限与符号链接

- Git Bash 的 `chmod` 大部分是**摆设**，NTFS 权限模型和 POSIX 不同，`chmod 600 ~/.ssh/id_ed25519` 不会真的生效（好消息是 Git 自带的 OpenSSH 通常不因此报错）。
- `ln -s` 默认是拷贝而非符号链接。需要真链接得先设 `export MSYS=winsymlinks:nativestrict`，且要管理员权限或开启开发者模式。
- 需要提权时不能用 `sudo`（不存在），只能以管理员身份重开 Git Bash。

### 5.7 性能

MSYS 的 `fork()` 模拟开销很大，进程密集型脚本（大循环里反复调外部命令）会明显比 Linux 慢。优化方向：
- 减少子进程：用 bash 内建替代 `$(basename ...)`（写成 `${path##*/}`）。
- 大批量文本处理让 `awk`/`sed` 一次处理完，别在 shell 里逐行循环。
- 真正吃性能的活儿交给 Python 或 WSL2。

---

## 六、什么时候该换工具

Git Bash 不是万能的，以下场景该换：

| 场景 | 换成 |
|---|---|
| 需要 Docker、systemd、apt、原生 Linux 编译 | WSL2 |
| Windows 系统管理：注册表、服务、WMI、AD、COM | PowerShell（[PowerShell入门](PowerShell%E5%85%A5%E9%97%A8.md)） |
| 想要结构化数据管道，少写 `awk`/`sed` | Nushell（[Nushell 使用指南](Nushell%20%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)） |
| 复杂逻辑、跨平台自动化 | Python |
| 要装大量 Unix 软件包并编译 | 完整版 MSYS2（带 `pacman`） |

作为 TA 的日常分工建议：**Git 操作和 POSIX 脚本用 Git Bash，批量数据/资产统计用 Nushell，DCC 自动化用 Python，Windows 系统层面用 PowerShell。**

---

## 七、参考链接

- Git for Windows 下载：<https://git-scm.com/downloads/win>
- MSYS2 文件系统路径规则（路径转换权威说明）：<https://www.msys2.org/docs/filesystem-paths/>
- MSYS2 与 Windows 程序交互：<https://www.msys2.org/docs/windows_path/>
- MinTTY 项目：<https://mintty.github.io/>
- Bash 参考手册：<https://www.gnu.org/software/bash/manual/>

---

> 相关笔记：[Nushell 使用指南](Nushell%20%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)（结构化数据管道，与本篇互补）、[PowerShell入门](PowerShell%E5%85%A5%E9%97%A8.md)、[Windows 命令提示符入门](Windows%20%E5%91%BD%E4%BB%A4%E6%8F%90%E7%A4%BA%E7%AC%A6%E5%85%A5%E9%97%A8.md)、[全面掌握 Git 版本管理](%E5%85%A8%E9%9D%A2%E6%8E%8C%E6%8F%A1%20Git%20%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86.md)、[Scoop使用入门](Scoop%E4%BD%BF%E7%94%A8%E5%85%A5%E9%97%A8.md)

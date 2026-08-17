PowerShell 是一种基于任务的命令行 shell 和脚本语言，专为系统管理和自动化设计。与传统的命令提示符不同，PowerShell 更加强大，能够处理对象（而不仅仅是文本），并且集成了 .NET 框架，具有丰富的功能。下面是 PowerShell 的一些基本用法：

### 1. **启动 PowerShell**
   - 在 Windows 搜索框中输入“PowerShell”并选择 Windows PowerShell。
   - 可以使用 `powershell.exe` 启动命令行界面的 PowerShell，也可以用 `powershell_ise.exe` 打开集成脚本环境（ISE）。

### 2. **基本命令**
   PowerShell 支持多种基本的系统管理命令，类似于传统的命令提示符。以下是一些常见的命令：
   
   - `Get-Help`：显示某个命令的帮助文档。
     ```powershell
     Get-Help Get-Process
     ```
   
   - `Get-Command`：列出系统上所有可用的 PowerShell 命令。
     ```powershell
     Get-Command
     ```

   - `Get-Process`：获取当前系统正在运行的进程列表。
     ```powershell
     Get-Process
     ```

   - `Set-Location` (`cd`)：改变当前工作目录。
     ```powershell
     Set-Location C:\Users
     ```

   - `Get-ChildItem` (`ls`)：列出当前目录下的文件和子目录。
     ```powershell
     Get-ChildItem
     ```

   - `New-Item`：创建新文件
     ```powershell
     New-Item -Path "C:\Path\To\File.txt" -ItemType File
     ```

   - `New-Item`：创建新文件夹
     ```powershell
     New-Item -Path "C:\Path\To\Folder" -ItemType Directory
     ```

   - `Copy-Item`：复制文件或文件夹。
     ```powershell
     Copy-Item -Path "C:\Source\file.txt" -Destination "C:\Destination\file.txt"
     ```

   - `Remove-Item`：删除文件或文件夹。
     ```powershell
     Remove-Item -Path "C:\Source\file.txt"
     ```

   - `Rename-Item`：重命名文件或文件夹。
     ```powershell
     Rename-Item -Path "C:\Source\file.txt" -NewName "newfile.txt"
     ```

### 3. **管道与对象处理**
   PowerShell 使用管道 (`|`) 传递命令的输出到下一个命令，但与传统命令行不同，PowerShell 处理的是对象，而不是纯文本。这允许更灵活的操作。

   ```powershell
   Get-Process | Where-Object { $_.CPU -gt 100 }
   ```
   这段命令会获取所有 CPU 使用率大于 100 的进程。`Where-Object` 用来筛选对象，`$_` 代表管道传输过来的当前对象。

### 4. **变量**
   PowerShell 使用 `$` 作为变量的前缀。变量可以存储任何类型的对象，例如字符串、数字、数组等。

   ```powershell
   $name = "PowerShell"
   $number = 123
   ```

### 5. **控制流**
   PowerShell 支持条件语句和循环。

   **条件语句：**
   ```powershell
   if ($number -gt 100) {
       Write-Output "Number is greater than 100"
   } else {
       Write-Output "Number is less than or equal to 100"
   }
   ```

   **循环：**
   ```powershell
   for ($i = 0; $i -lt 5; $i++) {
       Write-Output "Iteration $i"
   }
   ```

### 6. **脚本执行**
   可以将一系列命令写入 `.ps1` 文件中并执行。例如：
   ```powershell
   # HelloWorld.ps1
   Write-Output "Hello, World!"
   ```
   然后在 PowerShell 中执行该脚本：
   ```powershell
   .\HelloWorld.ps1
   ```

   **注意**：执行脚本时，可能需要修改执行策略，使用以下命令可以允许执行脚本：
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

### 7. **模块与函数**
   PowerShell 允许定义自定义函数和使用模块。

   **定义函数：**
   ```powershell
   function Greet-User {
       param ($name)
       Write-Output "Hello, $name!"
   }
   ```

   **使用模块：**
   模块是 PowerShell 中的一组功能，可以通过 `Import-Module` 来加载模块。
   ```powershell
   Import-Module ActiveDirectory
   ```

### 8. **远程管理**
   PowerShell 支持远程执行命令，例如在远程计算机上运行 PowerShell 脚本：
   ```powershell
   Enter-PSSession -ComputerName "RemoteComputer"
   ```

### 9. **获取系统信息**
   你可以使用 PowerShell 获取系统的详细信息，例如：
   ```powershell
   Get-Host  # 获取 PowerShell 环境信息
   Get-WmiObject -Class Win32_OperatingSystem  # 获取操作系统信息
   ```
### 10.设置代理
```
$env:HTTP_PROXY="http://127.0.0.1:10809"
$env:HTTPS_PROXY="http://127.0.0.1:10809"
```

PowerShell 以其强大的自动化和管理功能成为 Windows 管理员的首选工具，它的对象处理和与 .NET 框架的集成让它具有非常灵活的操作能力。

---

> **相关 shell 笔记**：本篇是 Windows 原生的对象管道 shell。若需要 POSIX 工具链（`grep`/`sed`/`ssh`/`awk`）与 Git 操作，见 [Git Bash 使用指南](Git%20Bash%20%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)；若需要更简洁的结构化数据查询（表格管道、`to md` 直出 Markdown），见 [Nushell 使用指南](Nushell%20%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)。三者分工：PowerShell 管 Windows 系统层（注册表/WMI/服务），Git Bash 管 POSIX 脚本与版本控制，Nushell 管数据统计与格式转换。

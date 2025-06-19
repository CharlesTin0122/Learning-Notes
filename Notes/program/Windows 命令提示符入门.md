Windows 命令提示符（CMD）是一个传统的命令行工具，用于执行各种任务，包括文件操作、进程管理和系统管理等。虽然 CMD 没有 PowerShell 那么强大，但它在 Windows 中依然非常实用。以下是一些常用的 Windows CMD 命令及其用法。

### 1. **文件和目录操作**

- **`dir`**：列出当前目录的文件和子目录。
   ```cmd
   dir
   ```

- **`cd`**：改变当前目录（进入指定目录）。
   ```cmd
   cd C:\Users
   ```

- **`md` 或 `mkdir`**：创建新目录。
   ```cmd
   mkdir NewFolder
   ```

- **`rd` 或 `rmdir`**：删除空目录。
   ```cmd
   rmdir NewFolder
   ```

- **`del`**：删除文件。
   ```cmd
   del file.txt
   ```

- **`copy`**：复制文件。
   ```cmd
   copy file.txt D:\Backup
   ```

- **`move`**：移动或重命名文件。
   ```cmd
   move file.txt D:\Backup
   ```

- **`ren`**：重命名文件或文件夹。
   ```cmd
   ren oldname.txt newname.txt
   ```

### 2. **系统信息**

- **`systeminfo`**：显示有关计算机的详细配置信息。
   ```cmd
   systeminfo
   ```

- **`ipconfig`**：显示网络配置信息。
   ```cmd
   ipconfig
   ```

- **`ipconfig /all`**：显示所有网络适配器的详细配置信息。
   ```cmd
   ipconfig /all
   ```

- **`ping`**：测试与远程主机的网络连接。
   ```cmd
   ping www.google.com
   ```

- **`tasklist`**：列出当前运行的所有进程。
   ```cmd
   tasklist
   ```

- **`taskkill`**：终止进程。
   ```cmd
   taskkill /im notepad.exe /f
   ```

### 3. **磁盘管理**

- **`chkdsk`**：检查磁盘并修复错误。
   ```cmd
   chkdsk C: /f
   ```

- **`diskpart`**：磁盘管理工具，可用于创建、删除、分区磁盘。
   ```cmd
   diskpart
   ```

- **`format`**：格式化磁盘。
   ```cmd
   format D: /fs:ntfs
   ```

### 4. **网络管理**

- **`netstat`**：显示网络连接、端口使用等信息。
   ```cmd
   netstat -an
   ```

- **`tracert`**：追踪数据包到达目标主机所经过的路由。
   ```cmd
   tracert www.google.com
   ```

- **`net user`**：管理本地用户帐户。
   - 查看本地用户：
     ```cmd
     net user
     ```

   - 添加用户：
     ```cmd
     net user username password /add
     ```

   - 删除用户：
     ```cmd
     net user username /delete
     ```

- **`net share`**：管理共享文件夹。
   - 创建共享：
     ```cmd
     net share MyShare=C:\Path\To\Folder
     ```

   - 删除共享：
     ```cmd
     net share MyShare /delete
     ```

### 5. **系统操作**

- **`shutdown`**：关闭、重启或注销计算机。
   - 立即关机：
     ```cmd
     shutdown /s /f /t 0
     ```

   - 立即重启：
     ```cmd
     shutdown /r /f /t 0
     ```

- **`cls`**：清除屏幕上的内容。
   ```cmd
   cls
   ```

- **`echo`**：显示消息或打开/关闭命令回显。
   - 显示文本：
     ```cmd
     echo Hello World
     ```

   - 禁用回显：
     ```cmd
     echo off
     ```

### 6. **批处理脚本**

CMD 支持批处理文件（`.bat` 或 `.cmd` 文件），可以将多个命令写入文件中并一次性运行。例如，创建一个简单的批处理文件 `example.bat`，内容如下：

```bat
@echo off
echo Hello, CMD!
pause
```

运行时，该批处理文件会显示 "Hello, CMD!"，并等待用户按键后退出。

### 7. **其他常用命令**

- **`fc`**：比较两个文件的内容。
   ```cmd
   fc file1.txt file2.txt
   ```

- **`find`**：在文件中查找字符串。
   ```cmd
   find "search_term" file.txt
   ```

- **`assoc`**：查看或修改文件关联（文件扩展名和应用程序之间的关系）。
   - 查看文件关联：
     ```cmd
     assoc
     ```

   - 修改文件关联：
     ```cmd
     assoc .txt=txtfile
     ```

- **`path`**：显示或设置系统的路径环境变量。
   - 查看当前 PATH：
     ```cmd
     path
     ```

   - 添加路径：
     ```cmd
     path C:\NewFolder;%path%
     ```

### 总结

CMD 是一个功能强大的工具，能够执行文件管理、系统信息查询、网络管理等各种任务。虽然 Windows PowerShell 在现代 Windows 系统中更为强大，但 CMD 依然非常实用，尤其是在需要执行一些简单、直接的命令时。


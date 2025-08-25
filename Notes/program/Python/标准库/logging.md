Python 的 `logging` 库是标准库中用于记录日志的模块，提供了灵活的方式来记录程序运行时的信息，如调试信息、错误、警告等。它支持不同级别的日志记录、格式化输出、以及将日志输出到不同目标（如控制台、文件等）。以下是对 `logging` 库的介绍及其使用方法：

---

### 一、`logging` 库概述

`logging` 模块的主要功能：
- **日志级别**：支持多种日志级别，按严重程度从低到高包括：
  - `DEBUG`：调试信息，用于开发和调试。
  - `INFO`：一般信息，记录程序的正常操作。
  - `WARNING`：警告信息，表示可能的问题。
  - `ERROR`：错误信息，程序出现问题但仍可运行。
  - `CRITICAL`：严重错误，程序可能无法继续运行。
- **灵活的输出目标**：支持输出到控制台、文件、远程服务器等。
- **格式化**：可以自定义日志的格式，如时间、级别、消息等。
- **层级结构**：支持基于模块或应用的层级日志记录器（Logger）。

默认情况下，`logging` 模块的日志级别是 `WARNING`，低于此级别的日志（如 `DEBUG`、`INFO`）不会输出。

---

### 二、基本概念

1. **核心组件**：
   - **Logger**：日志记录器，负责接收和处理日志消息。每个 Logger 可以有自己的名称和层级。
   - **Handler**：处理程序，决定日志的输出方式（如控制台、文件等）。
   - **Formatter**：格式化器，定义日志消息的输出格式。
   - **Filter**：过滤器，用于筛选日志消息。

2. **日志级别**：
   - 每个日志消息都有一个级别，`logging` 模块提供以下方法来记录不同级别的日志：
     - `logging.debug(msg)`：记录 DEBUG 级别日志。
     - `logging.info(msg)`：记录 INFO 级别日志。
     - `logging.warning(msg)`：记录 WARNING 级别日志。
     - `logging.error(msg)`：记录 ERROR 级别日志。
     - `logging.critical(msg)`：记录 CRITICAL 级别日志。

3. **默认行为**：
   - 如果不配置，`logging` 会使用默认的 Logger（根 Logger），输出到控制台，级别为 `WARNING` 或以上。

---

### 三、基本使用方法

以下是 `logging` 库的常用使用方式，从简单到复杂逐步介绍。

#### 1. 简单使用（默认配置）
直接使用 `logging` 模块的基本函数，适合简单的脚本。

```python
import logging

# 直接记录日志
logging.debug("This is a debug message")  # 不会输出，因为默认级别是 WARNING
logging.info("This is an info message")   # 不会输出
logging.warning("This is a warning message")  # 输出
logging.error("This is an error message")    # 输出
logging.critical("This is a critical message")  # 输出
```

**输出**（控制台）：
```
WARNING:root:This is a warning message
ERROR:root:This is an error message
CRITICAL:root:This is a critical message
```

**说明**：
- 默认情况下，只有 `WARNING` 及以上级别的日志会输出到控制台。
- 日志格式为：`级别:Logger名称:消息`。

#### 2. 配置日志级别和格式
通过 `logging.basicConfig()` 配置日志的基本设置。

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为 DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 自定义格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

# 记录日志
logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
```

**输出**（控制台）：
```
2025-08-23 22:26:45 - root - DEBUG - Debug message
2025-08-23 22:26:45 - root - INFO - Info message
2025-08-23 22:26:45 - root - WARNING - Warning message
2025-08-23 22:26:45 - root - ERROR - Error message
```

**说明**：
- `level`：设置最低日志级别，低于此级别的日志不会输出。
- `format`：定义日志输出格式，常用占位符包括：
  - `%(asctime)s`：日志记录时间。
  - `%(name)s`：Logger 名称。
  - `%(levelname)s`：日志级别。
  - `%(message)s`：日志消息。
- `datefmt`：设置时间格式。

#### 3. 输出到文件
通过 `filename` 参数将日志输出到文件。

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # 日志输出到文件
    filemode='w'  # 写入模式（'w' 覆盖，'a' 追加）
)

logging.debug("This will be written to app.log")
logging.info("This is an info message")
```

**结果**：
- 日志不会显示在控制台，而是写入 `app.log` 文件。
- 文件内容示例：
```
2025-08-23 22:26:45,123 - DEBUG - This will be written to app.log
2025-08-23 22:26:45,124 - INFO - This is an info message
```

#### 4. 使用自定义 Logger
通过 `logging.getLogger()` 创建自定义 Logger，支持模块化日志记录。

```python
import logging

# 创建自定义 Logger
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)  # 设置 Logger 的级别

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # 设置 Handler 的级别

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# 将处理器添加到 Logger
logger.addHandler(console_handler)

# 记录日志
logger.debug("Debug message from my_app")
logger.info("Info message from my_app")
```

**输出**：
```
2025-08-23 22:26:45,123 - my_app - DEBUG - Debug message from my_app
2025-08-23 22:26:45,124 - my_app - INFO - Info message from my_app
```

**说明**：
- `logging.getLogger('name')`：创建或获取指定名称的 Logger，名称通常反映模块或应用。
- `setLevel`：分别设置 Logger 和 Handler 的日志级别。
- `StreamHandler`：将日志输出到控制台。
- `Formatter`：定义日志格式。

#### 5. 同时输出到控制台和文件
通过添加多个 Handler 实现多目标输出。

```python
import logging

# 创建 Logger
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# 创建控制台 Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建文件 Handler
file_handler = logging.FileHandler('app.log', mode='w')
file_handler.setLevel(logging.INFO)

# 设置格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 添加 Handler 到 Logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 记录日志
logger.debug("This will only go to console")
logger.info("This will go to both console and file")
logger.error("This will go to both console and file")
```

**输出**：
- 控制台：
```
2025-08-23 22:26:45,123 - my_app - DEBUG - This will only go to console
2025-08-23 22:26:45,124 - my_app - INFO - This will go to both console and file
2025-08-23 22:26:45,125 - my_app - ERROR - This will go to both console and file
```
- `app.log` 文件：
```
2025-08-23 22:26:45,124 - my_app - INFO - This will go to both console and file
2025-08-23 22:26:45,125 - my_app - ERROR - This will go to both console and file
```

**说明**：
- `DEBUG` 日志只输出到控制台，因为文件 Handler 的级别设置为 `INFO`。
- 每个 Handler 可以有独立的级别和格式。

#### 6. 异常信息记录
使用 `exception()` 方法记录异常信息，包含堆栈跟踪。

```python
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    1 / 0
except ZeroDivisionError:
    logging.error("An error occurred", exc_info=True)
```

**输出**：
```
ERROR:root:An error occurred
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```

**说明**：
- `exc_info=True`：包含异常的堆栈跟踪信息。

---

### 四、进阶使用

1. **日志过滤**：
通过 `Filter` 筛选特定日志。

```python
import logging

# 创建 Logger
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# 创建 Handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# 创建 Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 创建 Filter，只允许特定模块的日志
class MyFilter(logging.Filter):
    def filter(self, record):
        return record.name == 'my_app'

handler.addFilter(MyFilter())
logger.addHandler(handler)

# 测试
logger.debug("This will be logged")
logging.getLogger('other_app').debug("This will NOT be logged")
```

**输出**：
```
2025-08-23 22:26:45,123 - my_app - DEBUG - This will be logged
```

2. **日志轮转**：
使用 `RotatingFileHandler` 或 `TimedRotatingFileHandler` 控制日志文件大小或按时间轮转。

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# 创建轮转文件 Handler，按文件大小轮转
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 记录日志
for i in range(1000):
    logger.debug(f"Log message {i}")
```

**说明**：
- `maxBytes`：当文件达到指定大小时，触发轮转。
- `backupCount`：保留的备份文件数量。
- 日志文件会命名为 `app.log`, `app.log.1`, `app.log.2` 等。

3. **配置文件**：
通过配置文件（如 `logging.conf`）管理复杂的日志设置。

**logging.conf**：
```ini
[loggers]
keys=root,my_app

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[loggerಸ

[logger_root]
level=DEBUG
handlers=consoleHandler,fileHandler

[logger_my_app]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=my_app

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=simpleFormatter
args=('app.log', 'w')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

**代码**：
```python
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('my_app')

logger.debug("Debug message")
logger.info("Info message")
```

**说明**：
- 配置文件可以简化复杂的日志设置，适合大型项目。

---

### 五、注意事项

1. **性能**：
   - 日志记录可能影响性能，尤其是在高频记录的情况下。合理设置日志级别和过滤器。
2. **线程安全**：
   - `logging` 模块是线程安全的，但在多进程环境中需注意文件锁问题。
3. **避免重复配置**：
   - `basicConfig` 仅在未配置 Logger 时生效，重复调用无效。
4. **模块化**：
   - 在大型项目中，使用命名 Logger（如 `logging.getLogger(__name__)`）避免冲突。

---

### 六、常见问题

1. **为什么 `debug` 和 `info` 日志不输出？**
   - 默认级别是 `WARNING`，需通过 `basicConfig` 或 `setLevel` 设置为 `DEBUG` 或 `INFO`。
2. **如何在模块化程序中避免重复日志？**
   - 使用 `logging.getLogger(__name__)` 为每个模块创建独立的 Logger。
3. **如何记录上下文信息？**
   - 使用 `logging.LoggerAdapter` 或在日志消息中添加上下文。

---

### 七、总结

Python 的 `logging` 库功能强大，适合从简单脚本到复杂应用的日志记录需求。通过合理配置 Logger、Handler 和 Formatter，可以实现灵活的日志管理。建议：
- 小型脚本：使用 `logging.basicConfig` 快速配置。
- 大型项目：使用自定义 Logger 和配置文件，结合 Handler 和 Filter 实现模块化日志记录。
- 生产环境：使用轮转 Handler 管理日志文件大小，按需输出到多个目标。

如需更具体的使用场景或示例，请告诉我！
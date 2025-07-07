- 日志的等级：默认日志级别是warning

| 日志等级（level） | 描述 | 
| -- | -- |
| DEBUG | 最详细的日志信息，典型应用场景是 问题诊断 | 
| INFO | 信息详细程度仅次于DEBUG，通常只记录关键节点信息，用于确认一切都是按照我们预期的那样进行工作 | 
| WARNING | 当某些不期望的事情发生时记录的信息（如，磁盘可用空间较低），但是此时应用程序还是正常运行的 | 
| ERROR | 由于一个更严重的问题导致某些功能不能正常运行时记录的信息 | 
| CRITICAL | 当发生严重错误，导致应用程序不能继续运行时记录的信息 | 


- 相关组件

| 名称 | 作用 | 
| -- | -- |
| Loggers | 记录器，提供应用程序代码直接使用的接口 | 
| Handlers | 处理器，将记录器产生的日志发送至目的地 | 
| Filters | 过滤器，提供更好的粒度控制，决定哪些日志会被输出 | 
| Formatters | 格式化器，设置日志内容的组成结构和消息字段 | 
|   | 


- Formatters格式

| 属性 | 格式 | 描述 | 
| -- | -- | -- |
| asctime | %(asctime)s | 日志产生的时间，默认格式为msecs2003-07-0816:49:45,896 | 
| msecs | %(msecs)d | 日志生成时间的亳秒部分 | 
| created | %(created)f | time.tme)生成的日志创建时间戳 | 
| message | %(message)s | 具体的日志信息 | 
| filename | %(filename)s | 生成日志的程序名 | 
| name | %(name)s | 日志调用者 | 
| funcname | %( funcname)s | 调用日志的函数名 | 
| levelname | %(levelname)s | 日志级別( DEBUG,INFO, WARNING, 'ERRORCRITICAL) | 
| levene | %( leveling)s | 日志级别对应的数值 | 
| lineno | %(lineno)d | 日志所针对的代码行号（如果可用的话） | 
| module | %( module)s | 生成日志的模块名 | 
| pathname | %( pathname)s | 生成日志的文件的完整路径 | 
| process | %( (process)d | 生成日志的进程D（如果可用） | 
| processname | (processname)s | 进程名（如果可用） | 
| thread | %(thread)d | 生成日志的线程D（如果可用） | 
| threadname | %( threadname)s | 线程名（如果可用) | 

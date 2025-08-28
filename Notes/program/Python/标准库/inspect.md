Python 的 `inspect` 模块是标准库中的一个强大工具，用于获取和分析 Python 代码中“活对象”（live objects）的元信息，例如模块、类、函数、方法、 traceback、frame 对象和代码对象等。它主要用于代码自省（introspection），帮助开发者在运行时动态检查对象的属性、源代码、签名等信息，广泛应用于调试、文档生成、测试和动态分析等场景。

以下是对 `inspect` 模块的详细介绍，包括其主要功能、使用场景和示例代码：

---

### **1. inspect 模块的主要功能**
根据 Python 官方文档，`inspect` 模块提供四类主要服务：[](https://docs.python.org/3/library/inspect.html)
1. **类型检查**：判断对象是否为模块、类、函数、方法等。
2. **获取源代码**：提取函数、方法或类的源代码。
3. **检查类和函数**：分析类结构、函数签名、参数等信息。
4. **检查解释器堆栈**：获取调用栈、frame 对象等运行时信息。

---

### **2. 核心功能和常用方法**
以下是 `inspect` 模块中一些常用的函数及其用途：

#### **(1) 类型检查**
`inspect` 提供了一系列以 `is` 开头的方法，用于判断对象的类型。这些方法通常作为 `getmembers()` 的过滤条件（predicate），也可以单独使用。例如：
- `inspect.ismodule(object)`：检查对象是否为模块。
- `inspect.isclass(object)`：检查对象是否为类。
- `inspect.isfunction(object)`：检查对象是否为普通函数。
- `inspect.ismethod(object)`：检查对象是否为绑定方法。
- `inspect.isroutine(object)`：检查对象是否为函数或方法（推荐用于兼容 Python 2/3 的场景）。[](https://www.pythonpool.com/python-inspect/)

**示例**：
```python
import inspect

def my_function(x, y):
    return x + y

class MyClass:
    def my_method(self):
        pass

print(inspect.isfunction(my_function))  # True
print(inspect.ismethod(MyClass().my_method))  # True
print(inspect.isclass(MyClass))  # True
```

#### **(2) 获取对象成员**
- `inspect.getmembers(object[, predicate])`：返回对象的所有成员（属性和方法），可以指定 `predicate` 过滤特定类型的成员。

**示例**：
```python
import inspect
import sys

for name, data in inspect.getmembers(sys, inspect.ismodule):
    print(f"{name}: {data}")
```
输出系统模块中导入的子模块（如 `sys.modules` 中的一部分）。

#### **(3) 获取源代码**
- `inspect.getsource(object)`：获取对象的源代码（字符串形式）。
- `inspect.getsourcelines(object)`：返回源代码行列表和起始行号。
- `inspect.getfile(object)`：返回定义对象的文件路径。
- `inspect.getsourcefile(object)`：返回对象的源文件路径（仅适用于文件中的代码）。

**示例**：
```python
import inspect

def my_function(x, y):
    """Returns the sum"""
    return x + y

print(inspect.getsource(my_function))
# 输出：
# def my_function(x, y):
#     """Returns the sum"""
#     return x + y
```

**注意**：`getsource()` 对于内置函数（如 `max()`）或从字节码加载的函数可能抛出异常，因为这些函数没有可访问的源代码。[](https://stackoverflow.com/questions/427453/how-can-i-get-the-source-code-of-a-python-function)

#### **(4) 获取函数签名**
- `inspect.signature(callable)`：返回函数或方法的签名对象（`Signature`），包含参数名称、默认值、类型注解等信息。
- `inspect.getfullargspec(func)`：返回函数的详细参数信息（Python 3.5+ 推荐使用 `signature()`）。[](https://stackoverflow.com/questions/2677185/how-can-i-read-a-functions-signature-including-default-argument-values)

**示例**：
```python
import inspect

def example_func(a: int, b: str = "hello", *args, **kwargs) -> bool:
    return True

sig = inspect.signature(example_func)
print(sig)  # (a: int, b: str = 'hello', *args, **kwargs) -> bool
for name, param in sig.parameters.items():
    print(f"{name}: {param.kind}, Default={param.default}")
```
输出：
```
a: POSITIONAL_OR_KEYWORD, Default=<class 'inspect._empty'>
b: POSITIONAL_OR_KEYWORD, Default=hello
args: VAR_POSITIONAL, Default=<class 'inspect._empty'>
kwargs: VAR_KEYWORD, Default=<class 'inspect._empty'>
```

#### **(5) 获取文档字符串**
- `inspect.getdoc(object)`：获取对象的文档字符串（docstring），并清理格式。
- `inspect.getcomments(object)`：获取对象前的注释。

**示例**：
```python
import inspect

def my_function():
    """This is a docstring."""
    pass

print(inspect.getdoc(my_function))  # This is a docstring.
```

#### **(6) 检查调用栈**
- `inspect.stack()`：返回当前调用栈的 frame 信息。
- `inspect.currentframe()`：返回当前 frame 对象。

**示例**：
```python
import inspect

def recurse(limit):
    print(inspect.stack()[0][3], inspect.stack()[0][2])
    if limit > 0:
        recurse(limit - 1)

recurse(2)
```
输出：
```
recurse 6
recurse 6
recurse 6
```

---

### **3. 使用场景**
`inspect` 模块在以下场景中非常有用：
1. **调试**：动态检查函数参数、调用栈或对象属性，帮助定位问题。
2. **文档生成**：自动提取函数签名、文档字符串或源代码，用于生成 API 文档。
3. **动态分析**：在运行时检查代码结构，例如分析类层次结构或函数依赖。
4. **装饰器开发**：通过检查函数签名或参数，动态修改函数行为。[](https://reintech.io/blog/python-practical-applications-inspect-method-tutorial-for-developers)
5. **测试框架**：用于验证函数或类的结构，例如 pytest 使用 `inspect` 获取测试函数的签名。[](https://martinheinz.dev/blog/82)
6. **代码自动化**：如自动生成 CLI 工具的帮助信息，或分析模块中的所有类和函数。

**实际案例**：
在 Web 开发中（如使用 Falcon 框架），`inspect.getmembers()` 可以用来提取 API 资源类的所有方法，自动生成路由文档。[](https://www.geeksforgeeks.org/python-falcon-inspect-module/)

---

### **4. 注意事项**
1. **局限性**：
   - 对于内置函数或 C 扩展模块中的函数，`getsource()` 可能无法获取源代码，因为它们没有 Python 源代码。[](https://stackoverflow.com/questions/427453/how-can-i-get-the-source-code-of-a-python-function)
   - 某些功能（如 `co_flags`）是 CPython 特有的，可能在其他 Python 实现（如 PyPy）中不可用。[](https://docs.python.org/3/library/inspect.html)
2. **性能**：
   - 自省操作（如 `getsource()` 或 `stack()`）可能涉及文件 I/O 或复杂解析，需谨慎用于性能敏感场景。
3. **兼容性**：
   - Python 3.5+ 推荐使用 `inspect.signature()` 而不是 `getargspec()`，后者在 Python 3 中已逐步废弃。[](https://stackoverflow.com/questions/2677185/how-can-i-read-a-functions-signature-including-default-argument-values)
4. **私有 API**：
   - 避免使用 `inspect._empty` 等私有属性作为 sentinel 值，因为它们是实现细节，可能在未来版本中更改。[](https://www.reddit.com/r/Python/comments/u3p62s/parts_of_the_standard_library_that_are_considered/)

---

### **5. 示例：综合应用**
以下是一个综合示例，展示如何使用 `inspect` 分析一个模块：
```python
import inspect
import logging

# 获取模块中的所有函数
for name, obj in inspect.getmembers(logging, inspect.isfunction):
    print(f"Function: {name}")
    print(f"Signature: {inspect.signature(obj)}")
    print(f"Docstring: {inspect.getdoc(obj)}\n")
```

输出（部分）：
```
Function: info
Signature: (msg, *args, **kwargs)
Docstring: Log a message with severity 'INFO' on the root logger.
```

---

### **6. 总结**
`inspect` 模块是 Python 标准库中用于代码自省的强大工具，提供了从类型检查到源代码提取的多种功能。它在调试、文档生成和动态分析中尤为有用，尤其适合需要深入了解代码结构的场景。通过合理使用 `inspect`，开发者可以更高效地分析和优化代码，同时避免常见的兼容性或性能陷阱。

更多详细信息可参考官方文档：https://docs.python.org/3/library/inspect.html。[](https://docs.python.org/3/library/inspect.html)
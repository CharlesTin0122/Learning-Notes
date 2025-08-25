JSON（JavaScript Object Notation，JavaScript 对象表示法）是一种轻量级的数据交换格式，易于人和机器读取与编写。它基于 JavaScript 的子集，但独立于语言，广泛用于 Web 应用程序的数据传输。以下是 JSON 的核心介绍：

### 1. **基本特点**
- **轻量**：JSON 语法简洁，数据结构清晰，文件体积小，适合网络传输。
- **跨语言支持**：几乎所有编程语言都支持 JSON 的解析和生成（如 Python、Java、C++ 等）。
- **可读性强**：格式直观，人类易读，机器易解析。

### 2. **基本语法**
JSON 数据由键值对组成，结构简单，主要包括以下元素：
- **对象（Object）**：用大括号 `{}` 包裹，键值对形式，键是字符串，值可以是多种类型。例：
  ```json
  {"name": "Alice", "age": 25}
  ```
- **数组（Array）**：用方括号 `[]` 包裹，包含有序值列表。例：
  ```json
  ["apple", "banana", "orange"]
  ```
- **值（Value）**：可以是字符串（用双引号 `""`）、数字、布尔值（`true`/`false`）、`null`、对象或数组。
- **键值对**：键必须是字符串，用双引号包裹，值跟冒号 `:`，键值对间用逗号 `,` 分隔。

### 3. **数据类型**
JSON 支持以下数据类型：
- **字符串**：如 `"hello"`，必须用双引号。
- **数字**：如 `42` 或 `3.14`，支持整数和浮点数。
- **布尔值**：`true` 或 `false`。
- **空值**：`null`。
- **对象**：嵌套键值对。
- **数组**：有序值集合。

### 4. **示例**
一个复杂的 JSON 示例：
```json
{
  "person": {
    "name": "Bob",
    "age": 30,
    "isStudent": false,
    "hobbies": ["reading", "gaming"],
    "address": {
      "street": "123 Main St",
      "city": "Shanghai"
    }
  }
}
```

### 5. **用途**
- **API 数据交换**：前后端通信中常用 JSON 传输数据（如 RESTful API）。
- **配置文件**：许多应用程序使用 JSON 存储配置信息。
- **数据存储**：NoSQL 数据库（如 MongoDB）常以 JSON 或类似格式存储数据。
- **跨平台传输**：JSON 因其通用性适合不同系统间的数据共享。

### 6. **优缺点**
**优点**：
- 简单易用，解析速度快。
- 跨语言兼容性好。
- 支持复杂嵌套结构。

**缺点**：
- 不支持注释（需依赖外部工具或约定）。
- 相比二进制格式（如 Protobuf），数据体积稍大。
- 不适合存储非常复杂的数据结构。

### 7. **与 XML 的对比**
- JSON 比 XML 更轻量，语法更简洁。
- JSON 解析速度通常更快。
- XML 支持更复杂的结构（如命名空间），但 JSON 在 Web 开发中更流行。

### 8. JSON 在 Python 中的使用

Python 提供了内置的 `json` 模块来处理 JSON 数据，支持将 Python 数据结构与 JSON 格式相互转换。以下是常见操作的详细介绍：

#### 1. 导入 json 模块
```python
import json
```

#### 2. 将 Python 对象转换为 JSON 字符串（序列化）
使用 `json.dumps()` 或 `json.dump()` 将 Python 数据结构（如字典、列表）转换为 JSON 格式。

- **`json.dumps()`**：将 Python 对象转换为 JSON 格式的字符串。
```python
data = {
    "name": "Alice",
    "age": 25,
    "courses": ["Math", "Science"]
}
json_string = json.dumps(data, indent=2, ensure_ascii=False)
print(json_string)
```
输出：
```json
{
  "name": "Alice",
  "age": 25,
  "courses": ["Math", "Science"]
}
```
- `indent=2`：格式化输出，增加缩进。
- `ensure_ascii=False`：支持非 ASCII 字符（如中文）正常显示。

- **`json.dump()`**：将 Python 对象直接写入文件。
```python
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```
这会在当前目录生成 `data.json` 文件，内容与上述 JSON 字符串相同。

#### 3. 将 JSON 转换为 Python 对象（反序列化）
使用 `json.loads()` 或 `json.load()` 将 JSON 数据解析为 Python 数据结构。

- **`json.loads()`**：将 JSON 字符串解析为 Python 对象。
```python
json_string = '{"name": "Alice", "age": 25, "courses": ["Math", "Science"]}'
data = json.loads(json_string)
print(data["name"])  # 输出：Alice
print(type(data))    # 输出：<class 'dict'>
```

- **`json.load()`**：从文件读取 JSON 数据并解析为 Python 对象。
```python
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(data["courses"])  # 输出：['Math', 'Science']
```

#### 4. Python 与 JSON 数据类型的对应关系
| JSON 类型       | Python 类型       |
|-----------------|-------------------|
| object          | dict             |
| array           | list             |
| string          | str              |
| number (int)    | int              |
| number (real)   | float            |
| true/false      | True/False       |
| null            | None             |

#### 5. 处理复杂嵌套数据
JSON 支持嵌套对象和数组，Python 可以通过字典和列表处理：
```python
nested_json = '''
{
  "person": {
    "name": "Bob",
    "address": {
      "city": "Shanghai",
      "zip": "200000"
    }
  }
}
'''
data = json.loads(nested_json)
print(data["person"]["address"]["city"])  # 输出：Shanghai
```

#### 6. 异常处理
JSON 操作可能因格式错误或文件问题抛出异常，建议使用 `try-except`：
```python
try:
    data = json.loads('{"invalid": "json"')  # 缺少结束括号
except json.JSONDecodeError as e:
    print(f"JSON 解析错误: {e}")
```

#### 7. 高级用法
- **自定义序列化**：处理 Python 中非 JSON 支持的类型（如自定义对象）。
```python
from datetime import datetime

class Person:
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday

def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

person = {"name": "Alice", "birthday": datetime(2000, 1, 1)}
json_string = json.dumps(person, default=custom_encoder)
print(json_string)  # 输出：{"name": "Alice", "birthday": "2000-01-01T00:00:00"}
```

- **排序键**：使用 `sort_keys=True` 按键排序输出 JSON。
```python
data = {"b": 2, "a": 1}
print(json.dumps(data, sort_keys=True))  # 输出：{"a": 1, "b": 2}
```

#### 8. 实际应用场景
- **API 数据交互**：Python 通过 `requests` 模块从 API 获取 JSON 数据并解析。
```python
import requests

response = requests.get("https://api.example.com/data")
data = response.json()  # 直接解析 JSON 响应
print(data)
```
- **配置文件**：JSON 常用于存储配置信息，便于读取和修改。
- **数据存储**：JSON 文件用于轻量级数据存储，适合跨平台传输。

### 注意事项
- **编码问题**：处理中文等非 ASCII 字符时，建议设置 `ensure_ascii=False` 和文件编码为 `utf-8`。
- **性能**：对于超大 JSON 数据，考虑使用 `ujson` 等第三方库以提升性能。
- **安全性**：解析不可信来源的 JSON 数据时，注意潜在的安全风险（如恶意构造的数据）。
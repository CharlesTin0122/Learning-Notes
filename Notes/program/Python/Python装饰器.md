# 函数装饰器
```python
"""-------------------装饰器案例-------------------"""


def a_new_decorator(a_func):
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction


def a_function_requiring_decoration1():
    print("I am the function which needs some decoration to remove my foul smell")


a_function_requiring_decoration1()
# outputs: "I am the function which needs some decoration to remove my foul smell"
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration1)
# now a_function_requiring_decoration is wrapped by wrapTheFunction()
a_function_requiring_decoration()
# outputs:I am doing some boring work before executing a_func()
#        I am the function which needs some decoration to remove my foul smell
#        I am doing some boring work after executing a_func()

"""-----------------与以上代码块等价--------------------"""


@a_new_decorator
def a_function_requiring_decoration2():
    """Hey you! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")


a_function_requiring_decoration2()
# outputs: I am doing some boring work before executing a_func()
#         I am the function which needs some decoration to remove my foul smell
#         I am doing some boring work after executing a_func()

# the @a_new_decorator is just a short way of saying:
a_function_requiring_decoration2 = a_new_decorator(a_function_requiring_decoration1)

''' 
print(a_function_requiring_decoration.__name__)
# Output: wrapTheFunction
这并不是我们想要的！Ouput输出应该是"a_function_requiring_decoration"。
这里的函数被warpTheFunction替代了。它重写了我们函数的名字和注释文档(docstring)。
幸运的是Python提供给我们一个简单的函数来解决这个问题，那就是functools.wraps。我们修改上一个例子来使用functools.wraps：
'''


def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction


@a_new_decorator
def a_function_requiring_decoration():
    """Hey yo! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")


print(a_function_requiring_decoration.__name__)
# Output: a_function_requiring_decoration

"""-----------------------------蓝本规范-----------------------------------"""

from functools import wraps


def decorator_name(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print("run befor Function")
        func(*args, **kwargs)
        print("run after Function")

    return decorated


@decorator_name
def func_print():
    print("Function is running")


func_print()
```
# 类方法的装饰器
在Python中，类方法的装饰器是用于修饰类方法或类相关函数的特殊装饰器，主要用于定义和管理类或实例的行为。以下是Python中与类方法相关的主要内置装饰器及其功能的详细介绍：

### 1. `@classmethod`
- **作用**：将一个方法标记为类方法，方法的第一个参数是类本身，通常命名为`cls`。类方法可以访问和修改类的状态（如类属性），而无需创建类的实例。
- **使用场景**：
  - 定义与类相关但不依赖于具体实例的方法。
  - 常用于工厂方法或访问类级别的属性。
- **特点**：
  - 可以直接通过类调用，也可以通过实例调用。
  - 不需要实例化类即可使用。
- **示例**：
  ```python
  class MyClass:
      class_attr = "I am a class attribute"

      @classmethod
      def class_method(cls):
          return f"Called from {cls.__name__}, class attribute: {cls.class_attr}"

  # 调用方式
  print(MyClass.class_method())  # 输出: Called from MyClass, class attribute: I am a class attribute
  obj = MyClass()
  print(obj.class_method())      # 输出: Called from MyClass, class attribute: I am a class attribute
  ```

### 2. `@staticmethod`
- **作用**：将一个方法标记为静态方法，静态方法不接收类或实例的隐式参数（如`self`或`cls`）。它本质上是一个普通的函数，但定义在类的命名空间中。
- **使用场景**：
  - 定义与类逻辑相关但不依赖于类或实例状态的工具函数。
  - 需要在类的上下文中组织代码，但不需要访问类或实例属性。
- **特点**：
  - 不绑定到类或实例，调用时无需传递`self`或`cls`。
  - 可以通过类或实例调用。
- **示例**：
  ```python
  class MyClass:
      @staticmethod
      def static_method(x, y):
          return x + y

  # 调用方式
  print(MyClass.static_method(3, 4))  # 输出: 7
  obj = MyClass()
  print(obj.static_method(3, 4))      # 输出: 7
  ```

### 3. `@property`
- **作用**：将一个方法伪装成属性，允许以属性的方式访问方法（无需加括号调用），常用于实现 getter 方法。
- **使用场景**：
  - 控制属性的访问，提供只读或计算属性的功能。
  - 实现数据封装，隐藏实现细节。
- **特点**：
  - 使用`@property`装饰器定义 getter 方法。
  - 可结合`@<property_name>.setter`和`@<property_name>.deleter`定义 setter 和 deleter 方法。
- **示例**：
  ```python
  class MyClass:
      def __init__(self, value):
          self._value = value

      @property
      def value(self):
          return self._value

      @value.setter
      def value(self, new_value):
          if new_value >= 0:
              self._value = new_value
          else:
              raise ValueError("Value must be non-negative")

  obj = MyClass(10)
  print(obj.value)    # 输出: 10
  obj.value = 20      # 设置新值
  print(obj.value)    # 输出: 20
  # obj.value = -5    # 抛出 ValueError
  ```

### 4. 自定义装饰器
除了内置的装饰器，用户还可以为类方法定义自定义装饰器，用于扩展功能（如日志记录、权限检查、计时等）。
- **实现方式**：
  - 自定义装饰器通常是一个函数或类，返回一个包装函数，包装函数会在调用原始方法前后执行额外的逻辑。
- **示例**：
  ```python
  def log_method(func):
      def wrapper(*args, **kwargs):
          print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
          result = func(*args, **kwargs)
          print(f"{func.__name__} returned: {result}")
          return result
      return wrapper

  class MyClass:
      @log_method
      def my_method(self, x):
          return x * 2

  obj = MyClass()
  obj.my_method(5)
  # 输出:
  # Calling my_method with args: (<__main__.MyClass object at ...>, 5), kwargs: {}
  # my_method returned: 10
  ```

### 注意事项
1. **装饰器的执行顺序**：如果一个方法应用了多个装饰器，装饰器的执行顺序是从内到外（从靠近方法的装饰器开始）。
   ```python
   class MyClass:
       @decorator1
       @decorator2
       def my_method(self):
           pass
   # 等价于 decorator1(decorator2(my_method))
   ```
2. **类方法与实例方法的区别**：
   - 普通实例方法接收`self`作为第一个参数，绑定到实例。
   - 类方法接收`cls`，绑定到类。
   - 静态方法不绑定任何对象，类似独立函数。
3. **性能考虑**：装饰器会增加额外的调用层，复杂装饰器可能影响性能，需谨慎设计。
4. **继承与装饰器**：在继承时，类方法和静态方法的行为会保留，但需要注意父类和子类中装饰器的作用范围。

### 总结
Python中与类方法相关的内置装饰器包括`@classmethod`、`@staticmethod`和`@property`，分别用于定义类方法、静态方法和属性方法。此外，可以通过自定义装饰器为类方法添加额外的功能。这些装饰器提供了灵活的方式来管理类的行为，增强代码的可读性和复用性。

如果你有具体的使用场景或需要更深入的示例，请告诉我！
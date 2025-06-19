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
# 类装饰器
- 在Python中，@符号是一个装饰器（decorator）语法糖，用于修改、增强或包装一个函数或方法的功能。装饰器可以看作是一种特殊的函数，它接受一个函数作为参数，并返回一个新的函数。

- 在class中，装饰器可以用于修饰类的方法，从而增强方法的功能或修改方法的行为。常见的class装饰器包括@property、@classmethod和@staticmethod等。

- @property装饰器用于将一个方法转换为属性，使得该方法可以像属性一样被访问，而无需使用括号调用。例如：

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14 * self.radius ** 2

circle = Circle(5)
print(circle.area)  # 输出 78.5
```

- 在这个示例中，我们定义了一个Circle类，它有一个属性radius和一个方法area。使用@property装饰器将area方法转换为属性，这样我们可以像访问属性一样访问它，而不需要使用括号调用。

- @classmethod装饰器用于定义类方法，类方法可以访问类变量，并且不需要实例化对象。例如：

```
class Car:
    num_of_wheels = 4

    def __init__(self, make, model):
        self.make = make
        self.model = model

    @classmethod
    def get_num_of_wheels(cls):
        return cls.num_of_wheels

print(Car.get_num_of_wheels())  # 输出 4
```

- 在这个示例中，我们定义了一个Car类，它有两个属性make和model，以及一个类变量num_of_wheels。使用@classmethod装饰器定义了一个类方法get_num_of_wheels，该方法返回类变量num_of_wheels的值。

- @staticmethod装饰器用于定义静态方法，静态方法与类方法类似，但它们不访问类变量，也不需要实例化对象。例如：

```
class MathUtils:
    @staticmethod
    def add(x, y):
        return x + y

print(MathUtils.add(3, 5))  # 输出 8
```

- 在这个示例中，我们定义了一个MathUtils类，它拥有一个静态方法add，它可以将两个数字相加并返回计算结果。由于静态方法不需要访问类变量，因此它们通常被用作一种工具函数，可以用来执行与类实例无关的操作。
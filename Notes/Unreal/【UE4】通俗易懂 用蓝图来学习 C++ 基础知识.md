# 【UE4】通俗易懂 用蓝图来学习 C++ 基础知识

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_0.png)

[演奇](https://www.zhihu.com/people/x-tesla)​

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_1.png)

文艺世界，心流宇宙。行于布施，发光发热。勤于修行，因果不虚。

已关注

[Jerish](https://www.zhihu.com/people/chang-xiao-qi-86)、

[CGBull](https://www.zhihu.com/people/flashbull) 等 

160 人赞同了该文章

## 【前言】：

用老罗来学UE蓝图：

[**【UE4】用老罗 多人运动的方式”快速”打开并掌握 UE4蓝图BP(Blueprint)基础知识**](https://zhuanlan.zhihu.com/p/135297007)

再开个脑洞，用蓝图来类比学习C++基础知识。

**C++ 刚开始学，所以本篇知识点不是特别全有些地方也可能不是特别准，望谅解，以后会慢慢补上。如有错误麻烦大佬们指出，感激不尽。**

## 【杂谈】：

另：多少菜鸟的噩梦啊。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_2.png)

之前就是这样学习的，从书上提取知识点笔记记了一大堆，想着把书从薄读到厚，再从厚读到薄。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_3.png)

结果发现屁用都没有，该写程序的时候啥都不会，琐碎的知识点实在太多了。

所以：

1. **知行合一**

1. **抓住重点**

- **总分**

- **分总**

## 【导图】：

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_4.png)

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_5.png)

## 一、 C++ Intro

### 【1.1】C++的诞生

Bjarne Stroustrup （来跟我一起唱，

它是在大佬头发郁郁葱葱的时候于1979年设计开发的，最初命名为带类的C，1983年更名为C++。C艹（四声、谢谢合作）对C进一步扩充和完善，而且随着时间发展会有不同的标准。

下面为五代标准。

- 1998——C++98

- 2003——C++03

- 2011——C++11

- 2014——C++14

- 2017——C++17

你们这些大佬啊，再研究研究这就是你们以后的下场，标准发型！毫无回天之术 。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_6.png)

## 【1.2】重要组成部分

- 核心语言——提供所有构建块，包括变量、数据类型、常量等

- C++ 标准库——提供大量函数，用于操作文件、字符串等等

- 标准模板库（STL）——提供了大量的方法，用于操作数据结构等

### 【1.3】C++面向对象开发的四大特性

1. **Encapsulation 封装**

1. **Abstract 抽象**

1. **Inherited 继承**

1. **Polymorphic 多态——**

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_7.png)

## 二、C++基本语法

### 【2.1】Class类 & Object对象

> 基类——class Shape ;（有宽高属性）基类的对象—— Shape sha; (类只有一个，但是对象可以有很多个，如Shape sha1、Shape sha2）派生类——class Rectangle : public Shape ;（继承自基类，新添加了计算面积函数，宽乘高就行了）派生类的对象——Rectangle Rect;


**【01】：**

**对同一类对象的共同属性和行为**

**【02】：**

对象Object，它是类的实例，用来特定类，所以是对象，

```cpp
#include <iostream>
using namespace std;
class Box
{
   public:
      double length;   // 长度
      double breadth;  // 宽度
      double height;   // 高度
};
int main()
{
  Box Box1;        // 声明 Box1  object对象，类型class为 Box
  // box 1 对象详述
   Box1.height = 5.0; 
   Box1.length = 6.0; 
   Box1.breadth = 7.0;
// box 1 的体积
   volume = Box1.height * Box1.length * Box1.breadth;
   cout << "Box1 的体积：" << volume <<endl;
 return 0;
}
 
```

可以结合一点玄学的东西。[**用科学来理解佛学，用佛学来认识宇宙——转载**](https://zhuanlan.zhihu.com/p/72782575)

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_8.png)

有一个白马非马的故事，感兴趣的可以了解一下。

- 成立——白马属于马，所以白马不是马

- 不成立——白马是马，但是白马并不能完全代表马

- 成立也不成立——白马非马，但是白马不能够代表马这个概念啊。可白马真的是一匹马啊

放在C++这里，白马是对象Object，马是类（动物类的子类），继承inherited自动物类。

高中生物学的 [界门纲目科属种](https://link.zhihu.com/?target=https%3A//baike.baidu.com/item/%25E7%2595%258C%25E9%2597%25A8%25E7%25BA%25B2%25E7%259B%25AE%25E7%25A7%2591%25E5%25B1%259E%25E7%25A7%258D/8738165%3Ffr%3Daladdin) 也适用，大道都是相通的。

当然还有一个 ，他大舅他二舅都是他舅，高桌子低板头都是木头。

**【03】跟UE4对比学习**

对应UE4的话，就是：

- BP 从基类中创建蓝图，ParentClass 父类 就是基类，如Actor。

- C++扩展类，ParentClass 父类为当前扩展类，如ShitActor，那么它是基于Actor之上继承的类，内容上相当于从Actor里git clone一样，我们在它的基础上添加一些新东西。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_9.png)

编辑器右上角可以看到ParentClass，Class Settings中可以更改父类及相关属性。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_10.png)

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_11.png)

我是这样类比的。

- **Content Browser 中的 BP**

- **世界场景中的BP**

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_12.png)

而拿材质来说的话，材质就是类，材质实例就是对象，一个定义变量属性，一个定义值。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_13.png)

### 【2.2】预处理器 Preprocessor（它实际上也是一种

> 宏是一种批量处理的称谓。计算机科学里的宏是一钟抽象，它根据一系列预定义的规则替换一定的文本模式，解释器或编译器在遇到宏时会自动进行这一模式替换。在程序编译时将宏名（#define XXX）替换成字符串的过程被称为 


- 是啥——预处理器是一些指令，指示编译器在实际编译之前所需要完成的预处理

- 注意——预处理器指定不是C++语句，所以它们不会以；分号断句。所有的预处理器指令都以#井号开头

- 作用——将所包含的文件全文复制到#include的位置，相当于是个展开为一个文件的宏

- 常见预处理器指令

- `#include`——相当于复制粘贴文件内容

- `#define`——用于创建符号常量，该符号常量通常称为宏

- `#pragma` once——所在文件仅编译一次

- `#ifndef` A `#define` A `#endif`——可能会有多个cpp文件同时包含一个h头文件，避免头文件的重定义，出现大量重定义的错误

### 【2.3】NameSpace 命名空间

它定义了一个范围，以避免调用多个库中出现的同名函数。

```cpp
#include <iostream>
using namespace std;
 
// 第一个命名空间
namespace first_space{
   void func(){
      cout << "Inside first_space" << endl;
   }
}
// 第二个命名空间
namespace second_space{
   void func(){
      cout << "Inside second_space" << endl;
   }
}
using namespace first_space;  //使用第一个名称空间
int main ()
{
 
   // 调用第一个命名空间中的函数
   func();
   
   return 0;
```

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_14.png)

## 三、 .h(Header) 头文件和. cpp(C Plus Plus)源文件

类和对象分别对应了属性和值，而头文件和源文件分别对应了声明和实现。

- 头文件.h相当于领导（header），对应阳，起主导作用。对员工发号施令（

- 源文件 .cpp相当于员工 ，起配合作用。接收领导的指令，996 地边吃着大饼，边

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_15.png)

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_16.png)

## 四、Class Access Modifier 类访问修饰符（public、private、protected）

- 作用——它防止函数直接访问类类型的内部成员

- 断句——每个标记区域（如private:)在下一个标记区域(如 public:)开始之前或者在遇到类主体结束右括号( int main(){ 

### 【4.1】Public 公有成员

> 公有成员在类的外部是可以Get 和 Set 的。


![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_17.png)

### 【4.2】Protected 受保护成员

> 保护成员在派生类（子类）中是可以Get的。


- 对于蓝图事件图表中的变量来说，就是Variable下的Private，勾选后，子类中只能Get 变量值，而不能够Set 变量值。（Event Graph 中变量的Private其实就相当于C++的 Protected）

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_18.png)

### 【4.3】Private 私有成员

> 私有成员变量或函数在类的外部是不可以访问的，只能够被本类成员（类内）和友元函数Get 。


- 对蓝图函数变量来说，就是函数Function/构造脚本内的Local Variable，只能供函数内部使用。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_19.png)

- 对材质来说，就是Constant，只供材质使用。而不是ScalarParameter可以在实例中（对象）调节参数。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_20.png)

### 【4.4】不同的继承方法

- 注意继承用 ： 冒号继承

```cpp
/*public*/
class A{};
class B: public A{};
/*protected*/
class A{};
class B: protected A{};
/*private*/
class A{};
class B: private A{};
```

- public：类内、类的对象；派生类、派生类对象 都可以访问

- protected： 类内、派生类内 可以访问；类的对象和派生类的对象 不可访问

对象不可以访问，意思就是把类拽到关卡中变成对象的时候，get 不了对象的变量。

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_21.png)

- private： 只有类内部可以访问；类的对象、派生类、派生类的对象，统统不可访问。（就上面【4.3】列举过的，一样）

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_22.png)

## 五、Variable 变量

### 【5.1】基础变量类型

- int—— 整数，不带小数，占4byte(32bit)空间的整数，最大值为2的31次方-1

- float——浮点型，带小数

- double——双精度浮点值，占8byte（64bit）空间的整数，最大值为2的63次方-1

- char——占1byte的字符，取值范围为-128~127或0~255

- void——无类型/空类型/不输入返回任何值

- bool——true false

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_23.png)

### 【5.2】其他变量类型

**【1】Constant常量**

- 说明——常量是固定值，在程序执行期间不会改变，且定义后不能进行修改。

- 两种声明方式

- `#define` 预处理器 —— 

`#define` LENGTH 10

- const 关键字—— 

const int LENGTH=10；

- 注意—— 分号断句、=等号、变量类型 这三点的区别

- 安全检查——const 常量具有类型，编辑器可以进行安全检查，#define宏定义没有数据类型，只是简单的字符串替换，不能进行安全检查

**【2】Array数组**

- 说明

- 声明——

int a[5]; 声明5个类型为int的数字

- 访问单个数组元素——

int b=a[0]——通过索引访问数组的第一个元素（index=0）

**【3】Enum枚举**

- 说明

- 声明——

- enum color{red,green=5,blue}; ——索引从0开始，red值为0，green值为5，blue值为6

- enum color{red,green,blue}c; c=blue;—— 变量类型为color的c，然后c被复制为三个颜色中的一个blue蓝色

**【4】String字符串**

- 说明——字符串

- 声明——

char str[n]="xxxxxxxx";

- 其他——

- strcpy(a,b)—— 把b的字符串复制给a

- strcat(a,b)—— 连接a b 字符串

### 【5.3】typedef

为已有类型取一个新名字,如用int声明整数换成用a声明整数

```cpp
typedef int a;
a shit= 0 ;
```

### 【5.4】变量作用域

- local variable——局部变量——在函数或代码块内部声明的变量——如 int main(){}主函数 { } 括号内声明的变量

- global variable——全局变量——所有函数外部声明的变量——如 int main(){} 主函数前面声明的变量（

- 形式参数——在函数参数的定义中声明的变量——如 int func (int a);

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_24.png)

形式参数

### 【5.5】存储类

存储类定义C++程序变量/函数的范围（Visibility）和生命周期（lifetime）

**【1】Static**

- 作用——static 修饰局部变量可以在函数调用之间保持局部变量的值，而不需要在每次它进入和离开作用域时进行创建和销毁

**【2】Extern**

- 作用

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_25.png)

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_26.png)

## 六、Statement 语句

没啥说的了，看[老罗BP](https://zhuanlan.zhihu.com/p/135297007)吧。相关的循环语句条件语句蓝图版在老罗那篇。

### 【6.1】循环语句

- while

- for

- do while

- 嵌套循环

- break

- continue

- goto

### 【6.2】条件语句

- if

- if else

- if 嵌套

- switch

- switch嵌套

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_27.png)

## 七、Pointers 指针

### 【7.1】指针

- 定义——指针是一个变量，其值为另一个变量的地址。每一个变量都有一个内存位置，每一个内存位置都定义了可使用& 连字号 运算符访问的地址，它表示了在内存中的一个地址

- 符号——

- 访问地址符号——&——它可以输出变量在内存中的地址

- 声明指针符号——*——用来声明一个指针储存地址值

- 注意事项——

- 所有指针的值的实际数据类型（int、float、char等等）都一样，都代表了内存地址的长的16进制数

- *ip=n——带星号输出变量值

- ip=&n=0x0000001——不带星号输出地址值

```cpp
int a;  //&a表示地址
cout<< &a<<endl;
int *a=5;  //声明一个指针
cout<<a<<endl; // 输出地址
```

### 【7.2】NULL 空指针

- 定义——声明变量时，如果没有确切地址可以赋值，通常为指针赋一个NULL值

- 语法——

```cpp
int *ptr=NULL；
cout<<ptr<<endl;
// 输出地址值 00000000 
```

- 注意——

- 访问地址为0的内存是为操作系统保留的

- 内存地址0表示该指针不指向一个可访问的内存地址

- 如果所有未使用的指针都被赋予空值，同时避免使用空指针，就可以防止误用一个未初始化的指针

### 【7.3】指针的算数运算

int32表示32位的整数，而1byte=8bit，所以它占用4个字节，对应内存地址就类似这样，1000递增变1004；而char字符占用1个字节，地址 1000递增变1001

```cpp
ptr++ (ptr--)
```

![](attachments/【UE4】通俗易懂%20用蓝图来学习%20C++%20基础知识_image_28.png)

## 八、Functions 函数

### 【8.1】class functions 类成员函数

- 定义——它是类的一个成员，它可以操作类的任意对象，可以访问对象中的所有成员

- 语法——

```cpp
//类内定义
class Box
{
output funcname (input){}
}
//类外定义，中间加 类名和一个范围解析运算符 即可
output Classname:: funcname (input)
```

- 符号——范围解析运算符（用于类外定义） 

::双冒号

- 格式——

void如果是空的话，可以不用填写

```cpp
output funcname （input){}
 int main(){
return 0;
}
```

### 【8.2】constructor 构造函数

类似Construction Script构造脚本。

[**【UE4】Spline BP 程序化模型/动画轨迹（爆肝般的详细）**](https://zhuanlan.zhihu.com/p/134279765)

- 定义——类的构造函数是类的一种特殊的成员函数，它会在每次创建类的新对象时执行

- 注意——

- 构造函数的名称与类的名称是必须完全相同的

- 并不会返回任何类型，也不会返回void

- 作用——

- 构造函数可用于为某些成员变量设置初始值

- 主要用来创建对象时初始化对象，即为对象成员变量赋初始值

- 格式——

```cpp
// 不带参数
class A
{
public:
   A(); // 声明构造函数
}；
A::A(void){};  //定义构造函数
//带参数
class A
{
public:
   A(int len); // 声明构造函数
}；
A::A(int len){};  //定义构造函数
```

- 使用初始化列表来初始化字段

```cpp
C::C(int a,int b,int c):X(a),Y(b),Z(c){}
//等同于
C::C(int a,int b,int c)
{
  X=a;
  Y=b;
  Z=c;
}
```

### 【8.3】deconstructor 析构函数

- 定义——在每次删除所创建的对象时执行

- 注意——析构函数的名称与类的名称是完全相同的，只是在前面加了个波浪号 ~ 作为前缀

- 作用——析构函数有助于在跳出程序（如关闭文件、释放内存等）前释放资源

- 格式——

```cpp
class A{
public:
  A(); //声明构造函数
 ~A();  //声明析构函数
A::A(void){};  //定义构造函数
A::~A(void){}; //定义析构函数
```

### 【8.4】copy constructor 拷贝构造函数

- 定义——它在创建对象时，是使用同一类中之前创建的对象类初始化新创建的对象

- 作用——

- 它在创建对象时，是使用同一类中之前创建的对象类初始化新创建的对象。

- 复制对象把它作为参数传递给函数

- 复制对象，并从函数返回这个对象

- 格式——

```cpp
classname(const classname &obj){}
//其中 obj是一个对象引用
A(const A &obj);
```

### 【8.5】friend 友元函数

- 定义——类的友元函数是定义在类外部,有权访问类的所有私有（private）和保护（protected）成员

- 注意——尽管友元函数的原型有在类的定义中出现过，但是友元函数不是类成员函数

- 格式——

```cpp
class Box{
public：
 friend void print(Box box);  //定义友元函数
};
void print(Box box){}; //声明友元函数
int main(){
Box box;
box.变量=n；// 访问对象中的变量
print(box);
}
```

### 【8.6】inline 内联函数 （默认就是内联的）

- 定义——如果一个函数是内联的，那么编译时编译器会把该函数的代码副本位置放在每个调用该函数的地方

- 注意——

- **在类定义中的定义的函数都是内联函数，即使没有inline说明符**

- 内联函数一般都是1~5行的小函数

- 内联函数中不允许使用loop循环和switch开关语句

- 内联函数的定义必须出现在内联函数第一次调用之前

- 作用——

- 编译时把函数的定义替换到调用的位置

- 解决程序中函数调用的效率问题

### 【8.7】virtual void 虚函数

【1】虚函数

- 为什么虚——并不能确定被调用的是基类的函数还是派生类的函数，所以被成为”虚“函数

- 哪儿虚？——虚在推迟联编或动态联编上，一个类函数的调用并不是在编译时刻确定的，而是在运行时刻被确定的

- 定义——

- 作用——定义为虚函数是为了允许 用基类的指针来调用子类的这个函数

- 注意——

- 定义一个函数为虚函数，不代表函数为不被实现的函数

- 定义一个函数为纯虚函数，才代表函数没有被实现

【2】纯虚函数

- 定义——纯虚函数是在基类中声明的虚函数，它在基类中没有定义，但要求任何派生类都要定义自己的实现方法

- 作用——定义纯虚函数是为了实现一个接口，起到一个规范的作用

- 通俗——

- 格式——

```cpp
virtual void func()=0
```

编辑于 2020-08-31 19:15
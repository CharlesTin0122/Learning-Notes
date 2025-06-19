# 基本概念和通用格式
- CMake 工具用于为您的插件和应用程序生成项目。
- 插件或应用程序目录中的 `CMakeLists.txt` 文件包含有关生成项目所需的库、源文件和构建函数的信息。它必须位于您的插件或应用程序目录的顶层，以及您的源代码和将与您的插件打包在一起的任何 `mel` 脚本。
- 项目结构
```css
MyProject/
├── src/
│   └── main.cpp
└── CMakeLists.txt

```
通用格式
```cmake
cmake_minimum_required(VERSION 3.16) # CMake最低版本

project(EmployeeManagementSystem) # 项目名称
# File命令通过参数GLOB_RECURSE SRC_FILES递归获取路径下的cpp文件存入SRC_FILES变量中
file(GLOB_RECURSE SRC_FILES
    "${PROJECT_SOURCE_DIR}/src/*.cpp"
    "${PROJECT_SOURCE_DIR}/src/*.h"
    "${PROJECT_SOURCE_DIR}/src/*.c")

# 添加可执行文件CMAKE_PROJECT_NAME是一个宏指向项目名称，SRC_FILES变量是文件列表
add_executable(${CMAKE_PROJECT_NAME} ${SRC_FILES})
```
# 逐行解析
1. 所需的 CMake 最低版本
    
    ```cmake
     cmake_minimum_required(VERSION 3.22.1)
    ```
    
2. `pluginEntry.cmake` 文件的路径。
    
    ```cmake
     include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    ```
    
    例如： 
    
    ```cmake
     cmake_minimum_required(VERSION 3.22.1)
    
      include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    ```
    
3. The project name 项目名称 
    
    ```cmake
     set(PROJECT_NAME <projectName>)
    ```
    
    For example: 例如： 
    
    ```cmake
     cmake_minimum_required(VERSION 3.22.1)
    
      include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    
     set(PROJECT_NAME exampleNode)
    ```
    
4. 所需资源文件的列表（如果需要）。如果您的项目使用多个资源文件，请用空格分隔每个文件
    
    ```cmake
     cmake_minimum_required(VERSION 3.22.1)
    
     include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    
     set(PROJECT_NAME exampleNode)
    
    set(RESOURCES_FILES myResource.xpm)
    ```
    
5. `mel` 文件列表（如果需要）。如果您的项目使用多个 `mel` 文件，请用空格分隔每个文件
    
    ```cmake
     set(MEL_FILES 
         <melFileName1> <melFileName2> <melFileName3>)
    ```
    
    For example: 例如： 
    
    ```cmake
     cmake_minimum_required(VERSION 3.22.1)
    
     include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    
     set(PROJECT_NAME exampleNode)
    
     set(RESOURCES_FILES myResource.xpm)
    
     set(MEL_FILES 
         exampleNode.mel)
    ```
    
6. 源文件列表，包括 `mel` 和资源文件（如果使用）。如果项目使用多个源文件，请在每个文件之间用空格隔开
    
    ```cmake
     set(SOURCE_FILES
         <sourceFileName1> <sourceFileName2> <sourceFileName3>
             ${MEL_FILES}
             ${RESOURCE_FILES})
    ```
    
    For example: 例如 
    
    ```cmake
     cmake_minimum_required(VERSION 3.22.1)
    
     include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    
     set(PROJECT_NAME exampleNode)
    
     set(RESOURCES_FILES myResource.xpm)
    
     set(MEL_FILES 
         exampleNode.mel)
    
     set(SOURCE_FILES
             exampleNode.cpp
             ${MEL_FILES}
         )
    ```
    
7. 所需的 devkit 库的列表。用空格分隔库列表
    
    注意： 所有插件和应用程序必须包含 OpenMaya 和 Foundation 库。
    
    ```cmake
     set(LIBRARIES
         OpenMaya Foundation <additionalLibrary1> <additionalLibrary2>
         )
    ```
    
    For example: 例如 
    
    ```cmake
     cmake_minimum_required(VERSION 3.22.1)
    
     include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    
     set(PROJECT_NAME exampleNode)
    
     set(RESOURCES_FILES myResource.xpm)
    
     set(MEL_FILES 
         exampleNode.mel)
    
     set(SOURCE_FILES
             exampleNode.cpp
             ${MEL_FILES}
         )
    
     set(LIBRARIES
         OpenMaya Foundation
         )
    ```
    
8. 使用 `find_<package_name>` 宏或 `find_package()` 调用添加的所需第三方包的列表。
    
    ```cmake
     find_package(MtoA)
     find_alembic()
    ```
    
    For example: 例如 
    
    ```cmake
       cmake_minimum_required(VERSION 3.22.1)
    
      include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    
     set(PROJECT_NAME exampleNode)
    
     set(RESOURCES_FILES myResource.xpm)
    
     set(MEL_FILES 
         exampleNode.mel)
    
     set(SOURCE_FILES
             exampleNode.cpp
             ${MEL_FILES}
         )
    
     set(LIBRARIES
         OpenMaya Foundation
         )
    
     find_package(MtoA)
     find_alembic()
    ```
    
9. 最后是构建函数。 
    
    如果您要创建插件，请添加 `build_plugin()`。如果您要创建独立应用程序，请添加 `build_application()`。
    
    ```cmake
     cmake_minimum_required(VERSION 3.22.1)
    
     include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)
    
     set(PROJECT_NAME exampleNode)
    
     set(RESOURCES_FILES myResource.xpm)
    
     set(MEL_FILES 
         exampleNode.mel)
    
     set(SOURCE_FILES
             exampleNode.cpp
             ${MEL_FILES}
         )
    
     set(LIBRARIES
         OpenMaya Foundation
         )
    
     find_package(MtoA)
     find_alembic()
     build_plugin()
    ```
# 创建并进入构建路径
```shell
mkdir build 
cd build
```
# MinGW构建
```shell
cmake -G "MinGW Makefiles" ..
```
# MinGW编译
```shell
mingw32-make
```
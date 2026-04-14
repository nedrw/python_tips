# Python Tips

一个实用的 Python 技巧与特性示例集合，帮助你深入理解 Python 的核心概念和高级用法。

## 项目结构

```
python_tips/
├── main.py              # 主入口程序（增强的示例发现机制）
├── tips/                # Python 技巧示例目录
│   ├── __init__.py      # finfo装饰器（支持元数据、执行统计）
│   ├── atexist.py       # atexit模块与程序退出清理
│   ├── decorator.py     # 装饰器用法
│   ├── descriptor.py    # 描述符协议
│   ├── format-string.py # f-string 格式化技巧
│   ├── generator.py     # 生成器与yield机制
│   ├── itertools.py     # itertools 迭代工具
│   ├── matmul.py        # 矩阵乘法运算符
│   ├── protocol.py      # 协议与类型提示
│   ├── single_dispatch.py # 单分派泛函数
│   ├── slots.py         # __slots__内存优化
│   ├── walrus_operator.py # 海象运算符（赋值表达式）
│   ├── chained_operators.py # 链式运算符
│   ├── loop_else.py     # 循环的else子句
│   └── with.py          # 上下文管理器
└── reactive/            # 响应式编程模块
    ├── reactive.py
    └── test.py
```

## 功能特性

### Python核心特性
- **装饰器**：函数装饰器、类装饰器、带参数的装饰器、装饰器组合
- **描述符**：实现 `__get__`、`__set__`、`__delete__` 控制属性访问
- **f-string 格式化**：表达式、日期时间、数字格式化、文本对齐、自定义 `__format__`
- **上下文管理器**：资源管理与上下文协议
- **迭代工具**：高效迭代与组合操作
- **生成器与yield**：基本生成器、生成器表达式、惰性求值、内存优化、无限序列、管道模式、yield from语法、协程基础（send/throw/close）
- **__slots__内存优化**：限制属性集合，节省内存，提升性能
- **循环else子句**：循环正常完成时的处理机制，配合break使用
- **链式运算符**：链式比较、链式赋值、链式方法调用
- **海象运算符**：Python 3.8赋值表达式，在表达式内部赋值
- **协议**：结构化子类型与类型提示
- **单分派**：基于参数类型的函数重载
- **矩阵乘法 (@)**：自定义矩阵运算
- **程序退出清理**：`atexit` 模块的使用

### 增强的示例发现机制
- **自动发现**：自动扫描并加载所有示例模块
- **元数据支持**：每个示例可包含描述、标签、难度等级
- **执行统计**：精确的执行时间统计和状态报告
- **错误处理**：完善的异常捕获和错误提示
- **统一接口**：所有示例遵循统一的结构模式

## 快速开始

### 列出所有可用示例

```bash
python main.py --list
```

输出示例：
```
============================================================
可用的示例模块:
============================================================
  - atexist
  - decorator
  - descriptor
  - format-string
  - itertools
  - matmul
  - protocol
  - single_dispatch
  - with

使用方法:
  python main.py --example <模块名>   # 运行指定示例
  python main.py --all               # 运行所有示例
============================================================
```

### 运行所有示例

```bash
python main.py --all
```

### 运行指定示例

```bash
python main.py --example decorator    # 运行装饰器示例
python main.py --example descriptor   # 运行描述符示例
python main.py --example format-string # 运行 f-string 示例
```

## 示例输出

运行示例时，会显示清晰的格式化输出：

```
============================================================
示例模块: decorator
描述: 演示装饰器的各种用法：简单装饰器、带参数装饰器、类装饰器
标签: decorator, metaprogramming
难度: intermediate
函数: main
============================================================
Before function call
Hello
After function call
Calling greet with args: ('Alice',), kwargs: {'message': 'Hello'}
Hello, Alice
Hi!
Hi!
Hi!
<b><i>Hello, world!</i></b>
An example docstring.
example
Call 1 of say_welcome
Welcome
Call 2 of say_welcome
Welcome

✓ 执行成功 (耗时: 0.0000s)
```

## 开发指南

### 创建新示例

1. 在 `tips/` 目录下创建新的 Python 文件（如 `my_feature.py`）
2. 定义一个 `main()` 函数作为入口
3. 使用 `@finfo` 装饰器标记函数

**基础用法**：
```python
from tips import finfo

@finfo
def main():
    # 你的示例代码
    print("Hello, Python Tips!")
```

**高级用法（带元数据）**：
```python
from tips import finfo

@finfo(
    description="演示Python特性的用法",
    tags=["feature", "example"],
    difficulty="intermediate"
)
def main():
    # 你的示例代码
    pass
```

### @finfo 装饰器参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `description` | str | "" | 示例的描述信息 |
| `tags` | list[str] | None | 标签列表，用于分类 |
| `difficulty` | str | "beginner" | 难度等级：beginner/intermediate/advanced |

## 环境要求

- Python 3.13+
- black (代码格式化)

安装依赖：

```bash
pip install -e .
```

## 项目特色

### 📚 结构化学习
每个示例模块专注于单一主题，配有详细的代码注释和文档字符串。

### 🎯 渐进式难度
从基础到高级，适合不同水平的Python开发者。

### 📊 执行监控
实时显示执行时间和状态，帮助理解代码性能。

### 🔍 智能发现
自动发现和加载示例，无需手动维护列表。

### 🎨 格式化输出
清晰的视觉分隔和状态图标，提升阅读体验。

## 贡献指南

欢迎贡献新的示例或改进现有示例：

1. Fork 本仓库
2. 创建新的示例文件或改进现有文件
3. 确保示例遵循项目结构规范
4. 提交 Pull Request

## 许可证

MIT License

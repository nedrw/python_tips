# Python Tips

一个实用的 Python 技巧与特性示例集合，帮助你深入理解 Python 的核心概念和高级用法。

## 项目结构

```
python_tips/
├── main.py              # 主入口程序
├── tips/                # Python 技巧示例目录
│   ├── __init__.py      # 工具函数
│   ├── atexist.py       # __slots__ 与类存在性检测
│   ├── decorator.py     # 装饰器用法
│   ├── descriptor.py    # 描述符协议
│   ├── format-string.py # f-string 格式化技巧
│   ├── itertools.py     # itertools 迭代工具
│   ├── matmul.py        # 矩阵乘法运算符
│   ├── protocol.py      # 协议与类型提示
│   ├── single_dispatch.py # 单分派泛函数
│   └── with.py          # 上下文管理器
└── reactive/            # 响应式编程模块
    ├── reactive.py
    └── test.py
```

## 功能特性

- **装饰器 (Decorator)**：函数装饰器、类装饰器、带参数的装饰器、装饰器组合
- **描述符 (Descriptor)**：实现 `__get__`、`__set__`、`__delete__` 控制属性访问
- **f-string 格式化**：表达式、日期时间、数字格式化、文本对齐、自定义 `__format__`
- **上下文管理器 (with)**：资源管理与上下文协议
- **迭代工具 (itertools)**：高效迭代与组合操作
- **协议 (Protocol)**：结构化子类型与类型提示
- **单分派 (Single Dispatch)**：基于参数类型的函数重载
- **矩阵乘法 (@)**：自定义矩阵运算
- **类存在性检测**：`__slots__` 与属性内存优化

## 快速开始

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

## 环境要求

- Python 3.13+
- black (代码格式化)

安装依赖：

```bash
pip install -e .
```

## 示例输出

运行 `python main.py --all` 将依次展示各个技巧的用法和输出效果，帮助你直观理解每个特性的行为。
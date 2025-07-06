import importlib
import inspect
import glob


def load_examples():
    """动态加载所有示例模块"""
    example_modules = []
    for file in glob.glob("tips/*.py"):
        if not file.endswith("__init__.py"):
            module_name = file.replace("\\", ".").replace("/", ".")[
                :-3
            ]  # 转换路径为模块路径
            example_modules.append(module_name)
    return example_modules


def run_all_examples():
    """运行所有注册的示例"""
    print("===== 开始运行所有Python技巧示例 =====")
    modules = load_examples()
    print(f"{modules=}")
    for module in modules:
        # 动态导入模块
        mod = importlib.import_module(module)
        # 查找模块中定义的示例函数（非导入函数）
        for name, func in inspect.getmembers(mod, inspect.isfunction):
            if name == "examples" and func.__module__ == module:
                func()  # 执行示例函数
    print("\n===== 所有示例执行完成 =====")


def run_single_example(example_name):
    """运行单个示例"""
    try:
        module = importlib.import_module(f"tips.{example_name}")
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name.endswith("_examples"):
                print(f"\n===== 运行 {example_name} 示例 =====")
                func()
                return
        print(f"错误：在 {example_name} 中未找到示例函数")
    except ImportError:
        print(f"错误：找不到示例模块 {example_name}")


if __name__ == "__main__":
    import argparse

    # 设置命令行参数
    parser = argparse.ArgumentParser(description="Python技巧示例")
    parser.add_argument("--all", action="store_true", help="运行所有示例")
    parser.add_argument("--example", type=str, help="运行指定示例（文件名不含.py）")

    args = parser.parse_args()

    if args.all:
        run_all_examples()
    elif args.example:
        run_single_example(args.example)
    else:
        # 默认显示帮助信息
        parser.print_help()

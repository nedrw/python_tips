import glob
import importlib
import inspect
import time
from typing import List, Tuple


def load_examples() -> List[str]:
    """动态加载所有示例模块路径"""
    example_modules = []
    for file in glob.glob("tips/*.py"):
        if not file.endswith("__init__.py"):
            # 转换路径为模块路径 (tips/decorator.py -> tips.decorator)
            module_name = file.replace("\\", ".").replace("/", ".")[:-3]
            example_modules.append(module_name)
    return example_modules


def run_all_examples() -> Tuple[int, List[Tuple[str, str]]]:
    """
    运行所有注册的示例

    Returns:
        Tuple[int, List[Tuple[str, str]]]: (成功数量, [(失败模块名, 错误信息), ...])
    """
    print("\n" + "=" * 60)
    print("Python Tips - Python技巧与特性学习项目")
    print("=" * 60)

    modules = load_examples()
    success_count = 0
    failed_modules = []

    for module_path in modules:
        try:
            mod = importlib.import_module(module_path)

            # 查找名为main的函数
            found = False
            if hasattr(mod, "main") and callable(mod.main):
                func = mod.main

                # 检查是否有@finfo装饰器
                if hasattr(func, "_is_example") and func._is_example:
                    # 有@finfo装饰器，使用增强显示
                    func()
                else:
                    # 没有@finfo装饰器，显示基本信息
                    module_name = module_path.split(".")[-1]
                    print(f"\n{'=' * 60}")
                    print(f"示例模块: {module_name}")
                    print(f"函数: main")
                    print("=" * 60)

                    start_time = time.perf_counter()
                    try:
                        func()
                        elapsed = time.perf_counter() - start_time
                        print(f"\n✓ 执行成功 (耗时: {elapsed:.4f}s)")
                    except Exception as e:
                        elapsed = time.perf_counter() - start_time
                        print(f"\n✗ 执行失败: {e} (耗时: {elapsed:.4f}s)")
                        raise

                success_count += 1
                found = True

            if not found:
                print(f"\n⚠ 警告: 模块 {module_path} 中未找到 main 函数")

        except Exception as e:
            failed_modules.append((module_path, str(e)))
            print(f"\n✗ 模块 {module_path} 执行失败: {e}")

    # 打印总结
    print("\n" + "=" * 60)
    print(f"执行完成: {success_count} 个成功", end="")
    if failed_modules:
        print(f", {len(failed_modules)} 个失败")
        print("\n失败详情:")
        for module, error in failed_modules:
            print(f"  - {module}: {error}")
    else:
        print()
    print("=" * 60)

    return success_count, failed_modules


def run_single_example(example_name: str) -> bool:
    """
    运行单个示例

    Args:
        example_name: 示例名称（不含.py扩展名）

    Returns:
        bool: 是否成功执行
    """
    try:
        module = importlib.import_module(f"tips.{example_name}")

        # 查找名为main的函数
        if hasattr(module, "main") and callable(module.main):
            func = module.main

            # 检查是否有@finfo装饰器
            if hasattr(func, "_is_example") and func._is_example:
                # 有@finfo装饰器，使用增强显示
                func()
            else:
                # 没有@finfo装饰器，显示基本信息
                print(f"\n{'=' * 60}")
                print(f"示例模块: {example_name}")
                print(f"函数: main")
                print("=" * 60)

                start_time = time.perf_counter()
                try:
                    func()
                    elapsed = time.perf_counter() - start_time
                    print(f"\n✓ 执行成功 (耗时: {elapsed:.4f}s)")
                except Exception as e:
                    elapsed = time.perf_counter() - start_time
                    print(f"\n✗ 执行失败: {e} (耗时: {elapsed:.4f}s)")
                    raise

            return True
        else:
            print(f"错误：在 {example_name} 中未找到 main 函数")
            return False

    except ImportError:
        print(f"错误：找不到示例模块 'tips.{example_name}'")
        return False
    except Exception as e:
        print(f"错误：执行示例 {example_name} 时发生异常: {e}")
        return False


def list_available_examples() -> None:
    """列出所有可用的示例模块"""
    modules = load_examples()

    print("\n" + "=" * 60)
    print("可用的示例模块:")
    print("=" * 60)

    for module_path in sorted(modules):
        module_name = module_path.split(".")[-1]
        print(f"  - {module_name}")

    print("\n使用方法:")
    print("  python main.py --example <模块名>   # 运行指定示例")
    print("  python main.py --all               # 运行所有示例")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    # 设置命令行参数
    parser = argparse.ArgumentParser(
        description="Python技巧示例学习工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --all                    # 运行所有示例
  python main.py --example decorator      # 运行装饰器示例
  python main.py --list                   # 列出所有可用示例
        """,
    )
    parser.add_argument("--all", action="store_true", help="运行所有示例")
    parser.add_argument(
        "--example", type=str, metavar="NAME", help="运行指定示例（文件名不含.py）"
    )
    parser.add_argument("--list", action="store_true", help="列出所有可用的示例模块")

    args = parser.parse_args()

    if args.all:
        run_all_examples()
    elif args.example:
        run_single_example(args.example)
    elif args.list:
        list_available_examples()
    else:
        # 默认显示帮助信息
        parser.print_help()

import functools
import time
from typing import Any, Callable, Optional


def finfo(
    func: Optional[Callable] = None,
    *,
    description: str = "",
    tags: list[str] | None = None,
    difficulty: str = "beginner",
) -> Callable:
    """
    增强的示例函数装饰器

    用于标记和展示Python技巧示例函数，提供元数据、执行时间统计和格式化输出。

    Args:
        func: 被装饰的函数（当不使用参数时自动传入）
        description: 示例描述，说明该示例的核心内容
        tags: 标签列表，用于分类和搜索
        difficulty: 难度等级 (beginner/intermediate/advanced)

    Returns:
        装饰后的函数

    Examples:
        @finfo
        def main():
            pass

        @finfo(description="装饰器示例", tags=["decorator"], difficulty="intermediate")
        def main():
            pass
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs) -> Any:
            # 获取模块信息
            module_name = f.__module__.split(".")[-1]
            func_name = f.__name__

            # 打印示例头部
            print(f"\n{'=' * 60}")
            print(f"示例模块: {module_name}")
            if description:
                print(f"描述: {description}")
            if tags:
                print(f"标签: {', '.join(tags)}")
            print(f"难度: {difficulty}")
            print(f"函数: {func_name}")
            print("=" * 60)

            # 计时执行
            start_time = time.perf_counter()
            try:
                result = f(*args, **kwargs)
                elapsed = time.perf_counter() - start_time
                print(f"\n✓ 执行成功 (耗时: {elapsed:.4f}s)")
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start_time
                print(f"\n✗ 执行失败: {e} (耗时: {elapsed:.4f}s)")
                raise

        # 附加元数据，用于示例发现
        wrapper._is_example = True  # type: ignore
        wrapper._description = description  # type: ignore
        wrapper._tags = tags or []  # type: ignore
        wrapper._difficulty = difficulty  # type: ignore

        return wrapper

    # 支持 @finfo 和 @finfo(...) 两种用法
    if func is not None:
        return decorator(func)
    return decorator

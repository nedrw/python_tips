from tips import finfo


class MyContextManager:
    def __enter__(self):
        print("Entering the context")
        return self  # 可以返回任何对象，通常返回self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting the context")
        if exc_type is not None:
            print(f"An exception occurred: {exc_val}")
        return True  # 抑制异常

@finfo
def main():
    # 使用自定义上下文管理器
    with MyContextManager() as manager:
        print("Inside the context")
        # 如果发生异常，会被__exit__处理
        raise ValueError("Something went wrong!")

# with语句用于简化资源管理，确保资源（如文件、网络连接、锁等）在使用后被正确释放或清理
# 核心原理基于上下文管理器（Context Manager），即实现了`__enter__`和`__exit__`方法的对象。
#
# 1. **`__enter__`方法**：
#    - 在进入`with`块时调用，通常用于资源的初始化（如打开文件）。
#    - 返回值会赋值给`as`后的变量（如果有）。
#
# 2. **`__exit__`方法**：
#    - 在退出`with`块时调用，无论是否发生异常。
#    - 参数`exc_type`, `exc_val`, `exc_tb`用于处理异常（如果发生异常，异常的类型、值和回溯都被当做参数）。
#    - 如果`__exit__`返回`True`，异常会被抑制；否则，异常会继续传播
if __name__ == "__main__":
    main()

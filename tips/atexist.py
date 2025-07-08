import atexit


# 定义一个清理函数
def cleanup():
    print("程序即将退出，正在执行清理操作...")


def first():
    print("First cleanup")


def second():
    print("Second cleanup")


def main():
    print("Starting program")
    # 注册函数，在程序退出时自动调用，LIFO
    atexit.register(cleanup)
    atexit.register(second)
    atexit.register(first)


if __name__ == "__main__":
    main()

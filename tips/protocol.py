from typing import Protocol

from tips import finfo


# 定义一个 Protocol，表示可绘图的对象
class Drawable(Protocol):
    def draw(self) -> None: ...

    def clear(self) -> None: ...


# 实现该协议的类
class Circle:
    def draw(self) -> None:
        print("Drawing a circle")

    def clear(self) -> None:
        print("Clearing the circle")


class Square:
    def draw(self) -> None:
        print("Drawing a square")

    def clear(self) -> None:
        print("Clearing the square")


class NotDrawable:
    def clear(self) -> None:
        print("Can only clear")


# 接受符合 Drawable 协议的对象
def render(shape: Drawable) -> None:
    shape.clear()


# Protocol 是静态类型检查机制的一部分
# 在运行时不会对不符合协议的对象进行阻断
# 如果需要运行时校验是否符合某种接口规范
# 可以考虑使用 ABC + abstractmethod 或手动添加检查逻辑
@finfo
def main():
    # 使用不同实现类的对象
    circle = Circle()
    square = Square()
    ndraw = NotDrawable()

    render(circle)  # 输出：Drawing a circle
    render(square)  # 输出：Drawing a square
    render(ndraw)


if __name__ == "__main__":
    main()

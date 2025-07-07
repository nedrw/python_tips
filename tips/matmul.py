from tips import finfo


class Matrix:
    def __init__(self, data):
        self.data = data

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        # 简单的矩阵乘法实现 (假设两个矩阵可以相乘)
        result_data = [
            [sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*other.data)]
            for row_a in self.data
        ]
        return Matrix(result_data)

    def __rmatmul__(self, other):
        # 如果左侧对象不支持 @ 操作，则尝试调用 __rmatmul__
        result_data = [[a * other for a in row_a] for row_a in self.data]
        return Matrix(result_data)

    def __imatmul__(self, other):
        result = self.__matmul__(other)
        self.data = result.data
        return self

    def __repr__(self):
        return f"Matrix({self.data})"


@finfo
def main():
    # 定义两个矩阵
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])

    result = 2 @ m1
    print(result)

    # 使用 @ 运算符进行矩阵乘法
    result = m1 @ m2
    print(result)  # 输出: Matrix([[19, 22], [43, 50]])

    # 原地矩阵乘法
    m1 @= m2
    print(m1)  # 输出: Matrix([[19, 22], [43, 50]])


if __name__ == "__main__":
    main()

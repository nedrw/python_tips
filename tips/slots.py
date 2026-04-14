"""
__slots__ 机制演示

演示Python的__slots__特性：内存优化、属性限制、继承行为等
"""

from tips import finfo


class PointWithoutSlots:
    """不使用slots的普通类"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class PointWithSlots:
    """使用slots优化的类"""

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class PointWithSlotsAndMethods:
    """slots + 方法的完整示例"""

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_from_origin(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    @property
    def magnitude(self) -> float:
        """属性访问器示例"""
        return self.distance_from_origin()


# 继承示例
class Point3D(PointWithSlots):
    """继承自使用slots的类"""

    __slots__ = ("z",)

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z


class Point3DNoSlots(PointWithoutSlots):
    """继承自不使用slots的类"""

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z


def demonstrate_basic_usage():
    """基本用法：属性限制"""
    print("\n【1. 基本用法 - 属性限制】")
    print("-" * 40)

    # 普通类可以动态添加属性
    p1 = PointWithoutSlots(1.0, 2.0)
    p1.z = 3.0  # 可以添加新属性
    print(f"✓ 普通类可以动态添加属性: p1.z = {p1.z}")

    # slots类限制属性
    p2 = PointWithSlots(1.0, 2.0)
    print(f"✓ slots类可以访问定义的属性: p2.x = {p2.x}, p2.y = {p2.y}")

    try:
        p2.z = 3.0  # 尝试添加未定义的属性
    except AttributeError as e:
        print(f"✗ slots类不能添加未定义的属性: {e}")


def demonstrate_memory_optimization():
    """内存优化对比"""
    print("\n【2. 内存优化对比】")
    print("-" * 40)

    import sys

    # 创建大量实例对比内存占用
    count = 10000

    # 普通类
    points_no_slots = [PointWithoutSlots(i, i) for i in range(count)]
    mem_no_slots = sum(sys.getsizeof(p) for p in points_no_slots[:100])

    # slots类
    points_with_slots = [PointWithSlots(i, i) for i in range(count)]
    mem_with_slots = sum(sys.getsizeof(p) for p in points_with_slots[:100])

    print(f"每个实例的大致内存占用:")
    print(f"  - 普通类:   ~{mem_no_slots / 100:.1f} bytes (含 __dict__ 和 __weakref__)")
    print(f"  - slots类:  ~{mem_with_slots / 100:.1f} bytes")
    print(f"  - 节省:     ~{(mem_no_slots - mem_with_slots) / 100:.1f} bytes/实例")
    print(f"  - 节省比例: ~{(1 - mem_with_slots / mem_no_slots) * 100:.1f}%")

    # __dict__ 的存在与否
    print(f"\n✓ 普通类有 __dict__: {hasattr(PointWithoutSlots(0, 0), '__dict__')}")
    print(f"✗ slots类无 __dict__: {not hasattr(PointWithSlots(0, 0), '__dict__')}")


def demonstrate_access_speed():
    """属性访问速度对比"""
    print("\n【3. 属性访问速度对比】")
    print("-" * 40)

    import time

    iterations = 1000000

    # 测试普通类
    p1 = PointWithoutSlots(1.0, 2.0)
    start = time.perf_counter()
    for _ in range(iterations):
        _ = p1.x
        _ = p1.y
    time_no_slots = time.perf_counter() - start

    # 测试slots类
    p2 = PointWithSlots(1.0, 2.0)
    start = time.perf_counter()
    for _ in range(iterations):
        _ = p2.x
        _ = p2.y
    time_with_slots = time.perf_counter() - start

    print(f"访问属性 {iterations:,} 次:")
    print(f"  - 普通类:  {time_no_slots:.4f}s")
    print(f"  - slots类: {time_with_slots:.4f}s")
    print(f"  - 提升:    {(time_no_slots / time_with_slots - 1) * 100:.1f}%")


def demonstrate_slots_with_property():
    """slots与property结合"""
    print("\n【4. slots与property结合】")
    print("-" * 40)

    p = PointWithSlotsAndMethods(3.0, 4.0)

    print(f"点坐标: ({p.x}, {p.y})")
    print(f"到原点距离: {p.distance_from_origin():.2f}")
    print(f"向量模长(@property): {p.magnitude:.2f}")

    # property不能用slots优化，但依然可以工作
    print(f"\n✓ property在slots类中正常工作")


def demonstrate_inheritance():
    """继承中的slots行为"""
    print("\n【5. 继承中的slots行为】")
    print("-" * 40)

    # 子类继承slots
    p3d = Point3D(1.0, 2.0, 3.0)
    print(f"✓ Point3D继承了父类的slots: ({p3d.x}, {p3d.y}, {p3d.z})")

    # 子类仍然受slots限制
    try:
        p3d.w = 4.0
    except AttributeError as e:
        print(f"✗ 子类也受slots限制: {e}")

    # 普通类的子类不受限制
    p3d_no_slots = Point3DNoSlots(1.0, 2.0, 3.0)
    p3d_no_slots.w = 4.0
    print(f"✓ 普通类的子类可以添加属性: p3d_no_slots.w = {p3d_no_slots.w}")


def demonstrate_gotchas():
    """常见陷阱和注意事项"""
    print("\n【6. 常见陷阱和注意事项】")
    print("-" * 40)

    # 1. 类变量与slots同名的问题
    print("✗ 陷阱1 - 类变量与slot同名会冲突:")
    try:

        class BadExample:
            __slots__ = ("x",)
            x = 10  # 这会在类定义时就冲突
    except ValueError as e:
        print(f"   错误: {e}")
        print(f"   解决: 避免使用与slot同名的类变量")

    # 2. 默认值处理
    class WithDefaults:
        __slots__ = ("x", "y")

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

    obj = WithDefaults()
    print(f"\n✓ 正确处理默认值: ({obj.x}, {obj.y})")

    # 3. __slots__不影响类本身
    print(f"\n✓ __slots__是类变量: {WithDefaults.__slots__}")


def demonstrate_real_world_example():
    """实际应用场景示例"""
    print("\n【7. 实际应用场景 - 高性能数据类】")
    print("-" * 40)

    from dataclasses import dataclass

    # 方案1: 普通dataclass
    @dataclass
    class PointDataClass:
        x: float
        y: float

    # 方案2: slots优化的dataclass
    @dataclass(slots=True)  # Python 3.10+
    class PointSlotsDataClass:
        x: float
        y: float

    p1 = PointDataClass(1.0, 2.0)
    p2 = PointSlotsDataClass(1.0, 2.0)

    print(f"普通dataclass: {p1}")
    print(f"slots dataclass: {p2}")

    # slots dataclass节省内存
    import sys

    print(f"\n内存占用:")
    print(f"  - 普通dataclass: {sys.getsizeof(p1)} bytes")
    print(f"  - slots dataclass: {sys.getsizeof(p2)} bytes")


@finfo(
    description="演示Python __slots__机制：内存优化、属性限制、继承行为、实际应用",
    tags=["slots", "optimization", "memory", "oop"],
    difficulty="intermediate",
)
def main():
    """
    __slots__ 机制完整演示

    主要内容:
    1. 基本用法 - 属性限制
    2. 内存优化对比
    3. 属性访问速度对比
    4. slots与property结合
    5. 继承中的slots行为
    6. 常见陷阱和注意事项
    7. 实际应用场景
    """
    print("\n" + "=" * 60)
    print("Python __slots__ 机制完整演示")
    print("=" * 60)

    demonstrate_basic_usage()
    demonstrate_memory_optimization()
    demonstrate_access_speed()
    demonstrate_slots_with_property()
    demonstrate_inheritance()
    demonstrate_gotchas()
    demonstrate_real_world_example()

    print("\n" + "=" * 60)
    print("✓ __slots__ 演示完成")
    print("=" * 60)
    print("\n【总结】")
    print("__slots__ 的优势:")
    print("  1. 节省内存 - 避免每个实例创建 __dict__")
    print("  2. 提高速度 - 属性访问更快")
    print("  3. 属性限制 - 防止意外添加属性")
    print("\n适用场景:")
    print("  - 大量实例的类（如游戏中的粒子、数据库记录）")
    print("  - 需要严格控制属性的场景")
    print("  - 内存敏感的应用")
    print("\n注意事项:")
    print("  - 无法动态添加新属性")
    print("  - 需要手动处理 __weakref__ 如果需要弱引用")
    print("  - Python 3.10+ dataclass 支持 slots=True")


if __name__ == "__main__":
    main()

# 响应式框架待办事项

## 核心架构

### 类层级结构
- Reactivable（基类）：响应式数据包装、变更通知、undo/redo
- ReactivableDict：字典类型响应式实现
- ReactivableList：列表类型响应式实现

### 核心设计
- 用户主动绑定：`data._controller = self`（控件构造函数中）
- 自动触发更新：数据变更 → `notify()` → `_controller.update(reactive_data)`
- 数据转换流程：JSON → Reactivable递归包装 → 响应式对象树

## P0 - 紧急修复

### 1. 崩溃Bug修复
- [ ] `Reactivable.__setattr__`：首次设置属性时`object.__getattribute__`抛异常
  - 方案：捕获AttributeError或检查`key in self.__dict__`
- [ ] `ReactivableList.__delitem__`：先pop后del导致索引错误
  - 方案：先获取值再删除，避免重复操作

### 2. 嵌套对象追踪
- [ ] 添加`_parent`和`_key`属性记录父对象
- [ ] 实现变更冒泡：子对象变更时通知父对象
- [ ] 实现路径追踪：记录完整变更路径（如`children[0].style.color`）

### 3. Undo/Redo机制重构
- [ ] 基于路径的历史记录：记录`(path, old_value, new_value)`
- [ ] 实现路径解析：根据路径定位属性
- [ ] 不再记录整体对象快照

### 4. 控件引用支持
- [ ] 添加`_controller`属性（默认为None）
- [ ] 实现`notify()`自动调用`_controller.update(self)`
- [ ] 定义标准接口：控件必须实现`update(reactive_data)`方法

## P1 - 功能完善

### 5. 属性访问增强
- [ ] 支持点号访问字典key：`obj.style.color` 等同于 `obj['style']['color']`
- [ ] 完善字典方法：keys(), values(), items(), get(), update()

### 6. 批量更新优化
- [ ] 修复`batch_update`逻辑
- [ ] 支持嵌套事务

### 7. 通知机制增强
- [ ] 传递详细变更信息（path、type、old_value、new_value）
- [ ] 支持选择性监听：`observe('style.color', callback)`

## P2 - 边界与优化

### 8. 类型处理完善
- [ ] 处理基础类型（int/str/float）
- [ ] 处理特殊类型（tuple/set/None）
- [ ] 避免重复包装已包装对象

### 9. 性能优化
- [ ] 惰性包装：只在访问时才包装嵌套对象
- [ ] 防抖高频更新
- [ ] Undo栈深度限制

### 10. 边界情况
- [ ] 循环引用处理
- [ ] 空容器处理
- [ ] 深拷贝支持

## 实现优先级

**阶段1：核心框架（本周）**
- 修复崩溃bug
- 实现嵌套对象追踪
- 重构undo/redo为路径记录
- 添加`_controller`支持

**阶段2：数组支持（下周）**
- 完善`ReactivableList.append`的自动通知
- 实现insert/delete事件
- 测试数组新增触发更新流程

**阶段3：数据描述支持（第三周）**
- 实现数据模板生成器
- 支持模板变量替换（如`${uuid}`）
- 集成到编辑器"添加页面"流程

**阶段4：嵌套对象支持（第四周）**
- 实现嵌套对象的`_controller`绑定
- 测试多层嵌套的自动更新链路
- 性能优化（增量更新）
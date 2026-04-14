# 响应式框架待办事项

## 核心架构

### 类层级结构
- Reactivable（基类）：响应式数据包装、变更通知
- CommandManager（全局单例）：命令管理、undo/redo栈、事务支持
- ReactivableDict：字典类型响应式实现
- ReactivableList：列表类型响应式实现

### 核心设计
- 用户主动绑定：`data._controller = self`（控件构造函数中）
- 自动触发更新：数据变更 → `notify()` → `_controller.update(reactive_data)`
- 数据转换流程：JSON → Reactivable递归包装 → 响应式对象树

## P0 - 紧急修复

### 2. 嵌套对象追踪 ❌ 不需要

- [ ] 实现路径追踪：记录完整变更路径（如`children[0].style.color`）

**决策**：经过讨论，当前的变更冒泡机制已经足够满足需求，不需要路径追踪功能。

### 3. Undo/Redo机制重构（命令模式）✅ 已完成

- [x] Reactivable基类：类属性`_command_manager`，方法`_execute_command()`
- [x] 移除`_history`、`_redo`属性，变更时生成命令并提交
- [x] 实现Command基类和具体命令（SetItemCommand, DelItemCommand, InsertCommand, AppendCommand, PopCommand, CompositeCommand）
- [x] 实现CommandManager全局单例，支持undo/redo栈和事务机制
- [x] ReactivableDict/ReactivableList所有修改操作使用命令模式
- [x] 批量更新（batch_update）使用事务机制，一次性撤销所有变更
- [x] 修复__getattribute__拦截方法访问的bug（将方法名添加到__exclude_attr）
- [x] 所有24个测试通过

**实现亮点**：
- 使用CompositeCommand实现事务，批量更新期间所有命令合并为一个复合命令
- 添加全局批量更新标志`_in_batch`，解决嵌套对象的批量状态同步问题
- 命令模式支持深度限制200，防止内存溢出

### 4. 控件引用支持 ✅ 已完成

- [x] 定义标准接口：控件必须实现`update(reactive_data)`方法
- [x] 定义 ControllerProtocol（使用 Python Protocol）
- [x] 添加 bind_controller 方法（带运行时验证）
- [x] 改进 notify 方法的控件检查（从弱检查改为强制检查并抛出 TypeError）
- [x] 添加测试验证控件引用机制（3 个新测试）

**实现亮点**：
- 使用 Protocol 定义接口，灵活且不强制继承，适合作为标准接口
- bind_controller 方法提供明确的绑定入口，带运行时验证，提供清晰的错误提示
- notify 方法会验证控件接口，如果控件没有 update 方法会抛出 TypeError
- 所有 27 个测试通过（之前 24 个 + 新增 3 个控件引用测试）

## P1 - 功能完善

### 5. 属性访问增强
- [ ] 支持点号访问字典key：`obj.style.color` 等同于 `obj['style']['color']`
- [ ] 完善字典方法：keys(), values(), items(), get(), update()

### 6. 批量更新优化
- [ ] 修复`batch_update`逻辑

### 7. 通知机制增强
- [ ] 传递详细变更信息（path、type、old_value、new_value）
- [ ] 支持选择性监听：`observe('style.color', callback)`

## P2 - 边界与优化

### 8. 类型处理完善
- [ ] 处理基础类型（int/str/float）和特殊类型（tuple/set/None）
- [ ] 避免重复包装已包装对象

### 9. 性能优化
- [ ] 惰性包装：只在访问时才包装嵌套对象
- [ ] 防抖高频更新

### 10. 边界情况
- [ ] 循环引用处理
- [ ] 空容器处理
- [ ] 深拷贝支持

## 实现优先级

**阶段1：核心框架（本周）✅ 已完成**
- ✅ 修复崩溃bug（`__getattribute__`拦截方法访问的bug）
- ❌ 实现嵌套对象追踪（不需要，用户决策）
- ✅ 重构undo/redo（命令模式）
- ✅ 添加`_controller`支持（控件引用标准接口）

**阶段2：数组支持（下周）**
- 完善`ReactivableList`的自动通知
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
# 时装与装备光环修改手册

供调整已有光环范围、目标和效果的代理使用。已读取两个实际 `.ora`、测试样本及其两个 APD 目标。路径均相对 `output`。光环运行时事件与动画表现分别编辑。

## 光环与状态两套编目

`aura/aura.lst:2` 的 `4` 对应 `AvatarAura/eventavatar_arabia.ora`，`10` 对应 `EquipmentAura/80Lv_Unique_Tonfa.ora`。实际提取文件名小写。前者事件引用 APD 109，后者引用 APD 167。`appendage/appendage.lst:2` 分别将这两个整数映射到 `avatar/event_arabia_physical.apd` 和 `equipment/80Lv_Epic_tonfa.apd`。Unique 光环指向文件名为 Epic 的状态是已观察到的事实，不擅自改名。

## 运行时字段

以下行号取自 `aura/equipmentaura/80lv_unique_tonfa.ora` 的全部 59 行。

- 第 3 行顶层 `[type]` 接字符串 `include`。它不同于 effect 块中的 animation 或 particle，不能全局替换 type。
- 第 5 行 `[range] 500` 是单整数，时装样本 `aura/avataraura/eventavatar_arabia.ora:5` 为 `130`。可推断为作用范围，半径、直径和距离单位未证实。
- 第 7 行 `[duration] 0` 为单整数。时装样本为 `1000`，测试样本 `aura/test.ora:7` 为 `10000`。不能仅凭 0 宣称永久。
- 第 9 至 11 行 `[destroy method]` 是两个字符串 `duration` 和 `source destroy`。名称提示到期或来源销毁时移除，精确逻辑仍需运行验证。
- 第 13 至 15 行 `[event time]` 是六个交替 token，`first 500 repeat 0 update 2000`。三种事件名称是字符串，后三个数为整数。时装样本为 `first 500 repeat 0 update 250`。单位及 repeat 0 的特殊语义不明，不把三值都称为冷却。
- 第 17 行标签确实拼作 `[overlab type]`，值为 `overlab`。不要纠正为 overlap。重复覆盖还是叠加的细节未证实。
- 第 19 至 25 行 `[target]` 内 `[object type] all` 与 `[ally type] ally` 各接一个字符串。时装样本 object-type 为 `character`，测试样本 ally-type 为 `dont-care`。只使用已有字符串枚举，不猜 hostile 的拼写。
- 第 27 至 29 行 `[event]` 为字符串 `appendage` 与整数 `167`。测试样本第 28 行则有两组 `appendage 1 appendage 2`，因此 event 可以包含多组，不能定死为两 token。

## 同名 effect 块按挂接目标区分

装备样本第 31 至 47 行是第一个 `[effect]`，第 49 至 59 行是第二个，均有结束标签。

- 第一个 effect 的 `[attach target] delegator`、`[type] animation`、`[attach pos] bottom` 各接单字符串。第 39 行 `[index] -1` 是单整数，-1 的特殊含义未证实。
- 第 41 至 43 行 `[option]` 有六字符串 `floor`、`apply custom color`、`sync speed`、`copy horizon`、`copy vertical`、`resize`。它们是一个列表，不是六个独立标签。
- 第 45 行 `[file name]` 为 `Aura/Effect/Animation/test_aura_range.ani`。当前 output 没有此精确根路径，只有分类目录中的同名测试资源。保留原引用并验证客户端解析，不能凭目录相似就改写。
- 第二个 effect 的 `[attach target] target`、`[type] particle`、`[attach pos] middle` 与 `[file name] Aura/Effect/Particle/test_aura_particle2.ptl` 定义另一表现。该块没有 index 或 option，不强行补齐第一个块的字段。

`appendage/avatar/event_arabia_physical.apd:15` 的 string-data 有 `physical attack physical defense` 两项，int-data 两个 0，float-data 两个 `10.0`。`appendage/equipment/80lv_epic_tonfa.apd:15` 则是 `equipment physical attack equipment magical attack` 两项，float-data 两个 `40.0`。前者 duration 为 30000，后者为 5000，均与 `.ora` duration 不同。光环寿命和所施状态寿命不可混用，数值的百分率含义未证实。

## 实用修改顺序

改范围只改顶层 range。改作用对象只改 target 块。改属性幅度要沿 event 的 APD ID 修改对应状态，不能改 effect 动画宣称改变属性。改表现先按 attach-target 定位两个 effect，保持它们各自原有字段。

保持 `#PVF_File\r\n`、CRLF、TAB 和整数、浮点、字符串原 token 类型。本文空格样例不是覆盖文本。不要引入源归档没有的路径或枚举。交真实重建、重新提取并检查，再在范围内外、友方和来源销毁场景验证。`--verify` 不能替代修改验证。

尚未知晓距离单位、各时间单位、0 与 -1 的特殊值语义、overlab 规则和根表现路径解析行为。未确认前保留这些值。

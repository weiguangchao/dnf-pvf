# 附加状态与属性修正修改手册

供调整已有 APD 状态的代理使用。本页读取五种状态样本，覆盖属性、攻击类型、暴击、技能等级和技能数据。路径均相对 `output`。同名 data 块受 `[type]` 控制，不能跨类型套列定义。

## 编目与公共字段

`appendage/appendage.lst:2` 将 `3` 映射到 `changeStatus/change_status_survivor.apd`，`39` 映射到 `skill_level/39.apd`，`41` 映射到 `critical_hit/41.apd`，`46` 映射到 `skilldataup/102010090.apd`。文件名不是调用 ID，102010090 不等于这里的 APD 编号 46。

- `appendage/changestatus/change_status_survivor.apd:3` 的 `[type]` 为字符串 `change status`。第 5 行 `[duration] 20000` 为单整数。名称支持持续时间的推断，单位未确认。
- 第 7 行 `[effect animation]` 是显式空字符串。第 11 行 `[icon image]` 是空字符串与整数 `0` 的二元组。保留空 token，不删除占位。
- 第 9 行 `[buff] 1` 是单整数，不能只凭名称保证正面状态或可驱散性。技能等级样本该值为 0。
- 第 13 行 `[max overlap] 1` 是单整数。最大叠加层数是按名称推断，重复施加刷新规则未知。

## 属性型数据应按索引一起看

`change_status_survivor.apd:15` 的 `[string data]` 有五项 `physical attack`、`magical attack`、`attack speed`、`move speed`、`cast speed`。第 19 行 `[int data]` 恰有五个 `0`。第 23 行 `[float data]` 恰有 `100.0 100.0 100.0 100.0 150.0` 五项。观察到三个数组等长，支持按位置关联的推断。`int data` 是否控制加算、乘算或百分率，以及 `float data` 的量纲，均未证实。不要把 100.0 自动称为 100%。

`appendage/critical_hit/41.apd` 同为 `change status`。第 5 行 duration 为 `50`，第 13 行 max overlap 为 `3`，第 15 行 string-data 只有 `physical critical hit rate`，int-data 第 20 行只有 `0`，float-data 第 24 行只有 `4.0`。这能定位物理暴击率候选参数，但不能证明 4.0 就是四个百分点。

## 其他 type 的形态不同

- `appendage/changeattackinfo/basic_attack_type_to_magical.apd:3` 的 type 是 `change basic attack type`。第 15 行 int-data 有三整数 `0 1 2`，第 19 行 string-data 有三个相同字符串 `attack type magical`，第 23 至 25 行 float-data 是空块。可推断按三项选择攻击类型，但整数对应普通攻击的哪三段未知。不要填充空 float-data。
- `appendage/skill_level/39.apd:3` 的 type 是 `skill level`。第 5 行 duration 为 `30000`，第 7 行 buff 为 `0`，第 11 行 max overlap 为 `5`。第 13 行 int-data 有六整数 `2 48 1 5 48 1`，其他两个 data 块为空。可按两个三元组观察，职业、技能和等级增量的列意义尚未核实，不能只把两处 48 当作 APD ID。
- `appendage/skilldataup/102010090.apd:3` 的 type 是 `skill data up`。第 13 行 int-data 为空，第 17 行 string-data 的第 18 行有 532 个字符串，按重复形态可分为 76 组七字符串。开头两组为 `` `[fighter]` `18` `[all]` `[level]` `0` `%` `30` `` 和同形的索引 `1` 组。注意 `18`、`0`、`30` 都是带反引号字符串，不是整数 token。
- 同第 18 行还出现 `` `[fighter]` `18` `[all]` `[cooltime]` `0` `%` `30` ``，以及职业字符串 `[at fighter]`。`[level]` 和 `[cooltime]` 位于反引号内，是数据值。名称提示等级数据与冷却修正，`%` 明示比例标记，但增减方向、基数和叠加公式尚未证实。修改时以职业、技能号字符串、数据类和列索引四项共同定位一组，不能替换所有 `30`。

## 编辑与核查

先从调用方的 APD ID 查编目，再确认 type。属性型修改保留三个数组的条数和位置，只改已定位索引。技能数据型保留七字符串分组及原反引号，不将数字字符串转为整数。未知 int-data 模式保留原值。

保留 `#PVF_File\r\n`、CRLF、TAB 以及原 token 类型。本文空格样例不能覆盖原文。源字符串表不允许任意新状态名或枚举。需要真实重建并重新提取，再验证施加、重复施加、到期和移除行为。`--verify` 不验证修改 output。

本页未验证 APD 的施加者、时间单位、叠层公式和技能列定义。文件名中的物品号或技能号只能作为查找线索。

## 技能修正的目标范围

`appendage/skilldataup/102010090.apd` 使用七字符串组，以具体职业 `[fighter]` 和技能 `18` 开头。职业与技能共同限定修改目标，组中的数字仍保持字符串类型。

修改已有状态时保留职业、技能、数据类和列索引，仅调整确认过的目标值。冷却修正的基数、方向与叠加公式尚未确认，不能只凭负值判断最终冷却。不能把职业改成 `[all]` 或批量改所有技能来实现单个技能的需求。

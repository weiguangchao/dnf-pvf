# 塔类副本与祭坛修改手册

本页用于维护塔层映射、塔内限制和祭坛数值。维护者应分清全局配置、每层地下城与选关图。

## 定位

先读 `etc/towerofdespair.etc`，再从 dungeon 索引找到层对应 dgn。`dungeon/dungeon.lst:2` 的 11008 对应 `Towers/ZTowerOfDespair001.dgn`。死亡塔另有 `etc/deathtower.etc`，祭坛配置在 `etc/advancealtar/advancealtarconfig.etc`。

## 参数与证据

- `[enterable count] 3`、`[min Level] 70`、`[top layer] 100` 见 `etc/towerofdespair.etc:3` 至第 8 行。min Level 的大小写必须保留。次数的日重置或账号范围未从文件确认。
- `[each layer matching dungeon]` 第 9 至 11 行有 200 个整数，即 100 对。开头 `1 11008 2 11009`。第 9、10 层都映射到 11016，第 19、20 层都到 11026。重复映射是实物，不能按层号公式自动纠正。
- `[npc layer]` 第 13 至 15 行有十个 0。其含义与 top layer 数量不同，不能扩到一百个。
- `[tower of despair]` 和 `[no fatigue]` 在 `dungeon/towers/ztowerofdespair001.dgn:13`、第 15 行，均没有值。它们是无参标记，不能加 1。
- 单层 `[size] 1 1`、``[greed] `BB` ``、start 与 boss 都为 `0 0`，见 `dungeon/towers/ztowerofdespair001.dgn:25` 至第 37 行。`[limit inout count] 1` 和 `[coin limit] 3` 分别见第 39、41 行，不能与全局 enterable count 合并。
- `[revision table]` 是路径 `Dungeon/Towers/table/TowerOfDespair.tbl`。`[required item]` 为三整数 `4473 1 1`，见 `dungeon/towers/ztowerofdespair001.dgn:49` 至第 52 行。首整数推断物品引用，两个 1 的消费或条件含义未知。
- `[tower high skill initial cool time]` 是 `1 1`，后面的 rate 是 `1.0 1.0`，见第 53 至 56 行。时间单位未证实。`[tower limit of stackable item] 1` 与 `[prohibit practice] 1` 是各自单值。
- `[reward item prob]` 在 `etc/deathtower.etc:3` 后为 `50 49 100`。未证明分母。`[reward gold weight] 11.0` 是浮点。`[reward exp weight]` 有 99 个数值，开头 `1.9869999885559082`，见第 7 至 9 行。`[illusion reward exp weight]` 另有 15 个数值，不能按普通塔表长度覆盖。
- `[reward card num]` 第 15 至 17 行有 99 个整数，开头十个 1。`[illusion reward card num]` 第 19 至 21 行为十五整数 `1 1 1 1 1 2 2 2 2 2 3 3 3 4 4`。对应等级还是层数未证实。
- `[gage upgrade cost percent]` 在 `etc/advancealtar/advancealtarconfig.etc:3` 至第 5 行为浮点 `0.800000011920929`。percent 是标签证据，计算基数未知。`[gage up rate]` 第 7 至 9 行为四组三整数 `0 10 1000`、`1 30 1100`、`2 70 1750`、`3 150 2500`，列义未知。
- `[daily refill ticket]` 在 `etc/advancealtar/advancealtarconfig.etc:11` 接 `3`，结束标签实际为 `[/refill ticket]`。不要把原始不对称标签修成另一种拼写。

## 修改步骤与未知项

换塔层时按显式层号修改配对第二整数，再查目标 dungeon ID 已存在。改入场规则分别核对全局 count、单层 inout、coin、required item。祭坛数值保留原浮点类型与三列宽度。

回归检查对应层入口、消耗、失败后再进入和奖励。重置时点、冷却单位、奖励数组索引域以及 gage 三列算法未确认，不能凭列名给出确定玩法结论。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

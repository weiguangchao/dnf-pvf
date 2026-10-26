# 宠物种类与基础定义修改手册

供修改宠物基础行为的代理使用。本页核对了 `creature/silverpig/silverpig.cre` 全部 111 行和 `creature/creaturesample.cre` 全部 146 行。路径均相对 `output`。样本只证明结构，模板中的默认值不代表全部宠物。

## 找到实际条目

先在 `creature/creature.lst:2` 按整数 ID 找路径。该行是连续的整数与反引号字符串对，不是一行一个宠物。其中 `23` 对应 `SilverPig/SilverPig.cre`，`24` 对应 `GoldPig/GoldPig.cre`。当前提取路径为小写 `creature/silverpig/silverpig.cre`。保留编目内已有大小写，查文件时核对大小写差异。

装备入口是另一套 ID。`equipment/creature/pig_silver.equ:32` 的 `[creature species] 23` 指向上述 creature ID。不要把装备编号或 `[output index] 63038` 当作 creature ID。

## 已观察到的字段

- `[name]` 在银猪第 3 行接一个 ``<16::name_0023`银色皮特兰猪`>`` 内联引用。`creature/creature.kor.str:34` 存在 `name_0023>银色皮特兰猪`。改名应修改对应 `.str` 值，内联显示文本不参与编译。
- `[width]` 在第 6 行接两个整数 `10 10`。字段名提示对象宽度，但两个分量的轴和单位未证实。保持双值，不替换成单一半径。
- `[floating height]` 在第 8 行接整数 `0`。`[layer]` 在第 10 行接字符串 `` `[normal]` ``。模板第 11 行则为 `` `[bottom]` ``。这是层级枚举字符串，不是新的标签。
- `[direction correct]` 在第 16 行接整数 `1`。按名称推断控制朝向修正，是否只允许 0 和 1 未证实。
- `[move speed]` 在第 18 行接五个整数 `286 238 114 95 70`。模板第 19 行同形。五列分别对应什么运动状态尚不明，不能仅凭大小命名走路、跑步或追赶速度。
- `[gravity]` 在第 20 行接整数 `1500`。可推断与运动有关，单位和引擎换算未知。
- `[start level]`、`[permission level]`、`[max level]`、`[parent max level]` 在第 22 至 29 行分别为单整数 `1`、`10`、`50`、`50`。名称支持起始等级、许可等级和等级上限的推断。主人等级限制的精确计算未由数据证实，四者不可互换。
- `[artifact slot]` 在第 30 至 32 行是带结束标签的字符串列表，恰有 `red`、`blue`、`green` 三项。与装备的 `[artifact red]`、`[artifact blue]`、`[artifact green]` 分类相呼应。不能把颜色写成标签。
- `[basic motion]`、`[walk motion]`、`[run motion]` 在第 40、42、44 行各接一个 `.ani` 路径。`Animation/stay.ani` 对应现有 `creature/silverpig/animation/stay.ani`。同目录的 `skill motion` 和 `over skill motion` 属于施技表现，不能用修改基础动作来推断伤害改变。
- `[revision x]` 与 `[revision y]` 在第 70、72 行各接 `0`。按名称推断是偏移量，坐标基准和像素单位尚未证实。

## 操作步骤与边界

1. 从装备的 species 查到 `.lst` 的整数和路径，再记录 `.cre` 原字段与原值。确认修改目标不是同名活动版本。
2. 基础等级调整只改对应单整数。若需要进化或技能解锁，另查成长和技能手册，不联动猜测所有等级字段。
3. 动画替换只选原归档已有字符串和资源。保留原字符串大小写及反引号，不新造路径。
4. 保存原 `#PVF_File\r\n` 头、CRLF 与 TAB。本文空格分隔的样例不能直接覆盖脚本。保留原 token 类型，包括 `{1}/{3}` 和 `{6}/{8}`。
5. 实际重建并重新提取改动条目，逐字段比较，再在客户端看跟随、层级和等级限制。`--verify` 只查源归档往返，不能验证这里的修改。

不能从这两个 `.cre` 样本确定速度五列、重力单位、图层全部枚举或客户端等级钳制规则。没有客户端验证时，将这些语义标为推断。

## 基础动作与技能表现

当前银猪 `.cre` 分别保存 `[basic motion]`、`[walk motion]`、`[run motion]`、`[skill motion]` 和 `[over skill motion]` 动画引用。按动作用途定位对应字段，再核对该宠物已有的资源路径。

只调整已有宠物的基础动作时，从 species 查到 `.cre`，再核对其目录内的 `.ani`。技能表现和技能数值分别定位。空动画字符串是否允许取决于具体字段，保留样本中未改字段的空值，不统一补路径。

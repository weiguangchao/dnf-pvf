# 宠物成长与装备修改手册

供调整已有宠物成长路线和装备属性的代理使用。已读取 `creature/exptable.tbl`、银猪和木偶 `.cre`，以及红、蓝、绿各一个装备样本。路径均相对 `output`。维护者应分别追踪经验数组、creature ID 和装备 ID。

## 经验与进化入口

- `creature/exptable.tbl:2` 是 55 个整数的连续数组。前六个为 `2 5 9 15 23 33`，末六个为 `3564 3879 4229 4629 5079 5579`。该文件没有等级标签。数值递增已观察到，首项对应等级 0 还是等级 1，以及数值是累计经验还是本级需求，均未证实。保留 55 项和顺序，不因 `.cre` 的上限 50 截断数组。
- `creature/silverpig/silverpig.cre:106` 的 `[evolution quest]` 为单整数 `1`。名称提示进化任务开关或任务关联，不能认定它是任务 ID。
- 同文件第 108 行 `[evolution creature id]` 为 `24`。`creature/creature.lst:2` 的 `24` 指向 `GoldPig/GoldPig.cre`，因此此处存在可核对的目标 creature 引用。
- 同文件第 110 行 `[evolution level]` 为 `30`。按名称推断为进化等级条件，不代表满级 50 或终结技能解锁等级 26。
- `creature/woodendoll/woodendoll.cre:52` 至 66 的 `[selective grow creature]` 是独立嵌套块。`[using exp item] 1`、`[grow Atype item index] 8472`、`[grow Btype item index] 8473`、`[grow level] 10`、`[grow Atype creature id] 123`、`[grow Btype creature id] 126` 各为单整数。保留六字段和块边界。`creature/creature.lst:2` 将 123 和 126 分别映射到 `Pinocchio/unfinished_pinocchio_period.cre` 与 `Pinocchia/unfinished_pinocchia_period.cre`。8472、8473 是物品引用候选，未在本页核对所属物品编目，不要据此创造物品。

## 宠物与装备的关联

`equipment/creature/pig_silver.equ` 全部 45 行中，`[equipment type]` 第 28 行接字符串 `` `[creature]` `` 和整数 `0`，第 32 行 `[creature species] 23` 才指向银猪。第 34 行 `[output index] 63038` 是另一单整数，含义尚未跟踪。第 38 行 `[MP MAX rate] 5.0` 是浮点数，字段大小写必须保留，不能认定这等同于宠物技能 MP 消耗。

## 红蓝绿装备参数

- `equipment/creature/artifact_red/eye_griffin.equ:29` 的 `[equipment type]` 为 `` `[artifact red]` 17 ``。第 33 行 `[creature minimum level] 30` 是单整数，按名称推断为宠物装备等级门槛。第 35 行 `[creature physical attack] 333` 是物理攻击数值。第 37 行 `[creature physical critical hit] 1.0` 为浮点数，不能仅按名称承诺为一个百分点。
- 同红装第 25 行 `[icon]` 为 `Item/creature/artifact_red.img` 加整数 `14`，是图集路径与图块索引的二元组。第 27 行 `[field image]` 为 `Item/field_creature.img 0`，属于掉落表现。更改这些字段不会证明攻击属性改变。
- `equipment/creature/artifact_blue/wings_sylph.equ:29` 为 `` `[artifact blue]` 15 ``，第 33 行最低等级为 `30`，第 35 行 `[creature magical attack] 276` 是单整数。不要把蓝装第 35 行按红装同位置解释为物理攻击。
- `equipment/creature/artifact_green/orb_wind.equ:29` 为 `` `[artifact green]` 20 ``，最低等级第 33 行为 `40`。第 35 行 `[creature skill consume mp rate] -12.0` 是带符号浮点数。名称提示 MP 消耗率修正，负数减少消耗是推断，百分比换算和叠加方式未证实。
- 红装第 39 行 `[price] 24500`，蓝装第 37 行为 `15000`，绿装第 37 行为 `45000`，均为单整数。交易币种或出售折算未在样本中编码，不能拿它们替代服务端经济规则。

## 修改与核查

先选已有宠物或已有装备。改进化目标时，核对目标 creature 编目和装备 species，分别记录两个 ID 空间。改选择成长时，只改完整 A 或 B 分支，保留另一路和 `[selective grow creature]` 结束标签。改经验只替换已有数组位置，不插入或删除项，先用客户端确认首项映射。改装备时保留整数与浮点的原 token 类型。

保存 CRLF、TAB 和字面头 `#PVF_File\r\n`。源归档字符串表限制新标签、字符串和路径。新增提取文件会被忽略，不能通过复制 `.equ` 创建新品。删除原文件会移除归档成员。需要真实重建、重新提取并验证成长条件和装备前后数值。`--verify` 不能证明修改生效。

尚未知晓经验索引基准、成长物品的实际编目、rate 数值换算和装备类型第二列的完整枚举。保持这些字段的已知结构，不补造说明。

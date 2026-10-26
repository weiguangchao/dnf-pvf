# 首饰修改手册

## 入口与三个样本

物品 ID 先查 `equipment/equipment.lst:2`。戒指 `24146` 对应 `equipment/character/common/ring/ring_gblritual.equ`。本页另读项链 `equipment/character/common/amulet/neck_2choro329.equ` 与手镯 `equipment/character/common/wrist/brac_2choro1133.equ`。三份样本分别包含套装引用、技能修改与改造输入输出。

## 部位与数值

- `[equipment type]` 在戒指 `equipment/character/common/ring/ring_gblritual.equ:44` 为 `[ring] 21`。项链第 45 行为 `[amulet] 20`，手镯第 49 行为 `[wrist] 20`。部位由字符串表示，第二整数不能作为唯一部位键。
- 戒指 `[grade]` 为 `62`，`[rarity]` 为 `4`，`[minimum level]` 为 `55`，见 `equipment/character/common/ring/ring_gblritual.equ:12` 到第 25 行。手镯最低等级为 `70`。项链样本没有 `[minimum level]`，不能照手镯补默认字段。
- 三个样本 `[usable job]` 都为 `[all]`，`[attach type]` 都为 `[free]`，分别见戒指第 18、22 行，项链第 21、25 行，手镯第 17、21 行。不能据此假定所有首饰都无限制。
- `[equipment magical defense]` 戒指为 `2240 2048`，见 `equipment/character/common/ring/ring_gblritual.equ:38`。项链第 39 行为 `5040 4800`，手镯第 39 行为 `3744 3600`。三例都是两个降序整数，列义和品质算法未确认，不交换为 min、max 顺序。
- 戒指 `[physical attack]`、`[magical attack]` 各为 `38`，`[stuck]` 为 `-1`，见戒指第 26 到 31 行。这里单值属性不同于双值魔防，负数也属实际 token，不能批量消除。
- 戒指 `[price]`、`[repair price]`、`[value]` 分别为 `74400`、`62496`、`59520`，见戒指第 32 到 37 行。项链只有 repair price 和 value，不应为了统一模板补 price。
- 戒指 `[set item master]` 在 `equipment/character/common/ring/ring_gblritual.equ:54` 为 `20107`。手镯 `[part set index]` 在 `equipment/character/common/wrist/brac_2choro1133.equ:15` 为 `15`。两种引用标签不同，不能把 20107 直接当 part set index 替换。

## 技能与改造块

- 项链 `[skill data up]` 在 `equipment/character/common/amulet/neck_2choro329.equ:55` 有四组七 token。第一组 `[swordman] 81 [dungeon type] [static] 3 + 1`。后面三组使用 `[level]` 列 `0`、`1`、`2`，运算符 `%`，末值 `-6`。第 10 行说明写崩山裂地斩多段次数 `+1` 与攻击力 `-6%%`，提供该文件的语义依据。
- 项链 `[emancipate]` 第 59 行内 `[input]` 为 `3290 25`，`[output]` 为 `400817 1`，见项链第 61 到 67 行。按 ID 与数量解释是可核对的引用形状。输入 ID 查堆叠物索引，输出 ID 查装备索引，不当作坐标。
- 手镯 `[physical critical hit]` 与 `[magical critical hit]` 各为整数 `1`，见 `equipment/character/common/wrist/brac_2choro1133.equ:41` 到第 44 行。显示百分比单位需要实机确认。
- 戒指 `[routing priority]` 在 `equipment/character/common/ring/ring_gblritual.equ:56` 是空块。不能据其他装备有职业优先级就填充，也不删结束标签。

## 修改步骤与未知项

1. 先确定首饰部位及 ID。改魔防只改对应双值。未确认双值语义时不能安全重算或交换两列。
2. 改技能加成时明确 mode、数据域和列号。改造必须同时解析输入物品、输出装备及数量，确保没有把堆叠物 ID 当装备路径。
3. 改套装关联先分清 `[set item master]` 与 `[part set index]`。本页未确认前者解析目标，不能安全重指向。
4. 保留 CRLF、TAB、`#PVF_File\r\n` 与原类型。中文改 `.str` 原有键，禁止只改内联显示。Markdown 空格不是源文件分隔。
5. 静态核对魔防双值、四组技能修正和输入输出数量。需要重建后提取及客户端穿戴、技能和改造验证。`--verify` 不是修改验证。

套装叠加、改造是否保留强化、双值计算与重量单位仍未确认。项链说明中的 Lv70 是文本证据，不证明缺失的最低等级字段会自动按 70 执行。

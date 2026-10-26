# 防具修改手册

## 定位与样本

先由 `equipment/equipment.lst:2` 查物品 ID。`100412` 对应 `character/common/jacket/cloth/coat_cl_2choro413.equ`。本页读取磁盘文件 `equipment/character/common/jacket/cloth/coat_cl_2choro413.equ` 和 `equipment/character/common/pants/leather/pant_lt_2choro187.equ`。前者为租借布甲上衣，后者为带技能修改的皮甲下装。

防具目录还包括 `equipment/character/common/shoulder`、`equipment/character/common/belt`、`equipment/character/common/shoes`。定位目标仍要读实际 `.equ`，目录 belt 不能直接当标签枚举。

## 字段与证据

- `[equipment type]` 在上衣 `equipment/character/common/jacket/cloth/coat_cl_2choro413.equ:58` 为 `[coat] 17`。下装 `equipment/character/common/pants/leather/pant_lt_2choro187.equ:54` 为 `[pants] 17`。字符串区分部位，整数 17 在两个部位相同，不能当槽位编号。
- `[sub type]` 在上衣第 60 行为 `0`，下装第 56 行为 `1`。`[item group name]` 分别为 `cl coat` 与 `lt pants`，见上衣第 68 行和下装第 64 行。结合目录可推断对应布甲与皮甲，不能从两例补出完整防具类型表。
- 上衣 `[grade]` 为 `73`，`[minimum level]` 为 `70`，见 `equipment/character/common/jacket/cloth/coat_cl_2choro413.equ:12` 和第 26 行。下装对应 `72` 和 `70`。不要联动修改 grade 与最低等级。
- 上衣 `[usable job]` 为 `[all]`，`[attach type]` 为 `[trade delete]`，见上衣第 20 和 24 行。下装 attach type 则为 `[free]`。这些是原有字符串枚举，不能根据中文交易描述重写。
- 上衣 `[equipment physical defense]` 为两个整数 `936 900`，见 `equipment/character/common/jacket/cloth/coat_cl_2choro413.equ:52`。下装同标签为 `1540 1480`，见下装第 48 行。顺序为降序，不是已确认的 min、max。面板品质算法未确认，保留双值及顺序。
- 上衣 `[physical attack]` 为单整数 `19`，`[magical attack]` 为 `49`，`[magical defense]` 为 `44`，见上衣第 28 到 33 行。它们与双值装备防御不同。不要把所有含 attack 或 defense 的字段统一按面板攻防修改。
- 上衣 `[HP MAX]` 为 `54`、`[MP MAX]` 为 `106`、`[MP regen speed]` 为 `2`，见上衣第 38 到 43 行。下装分别为 `76`、`82`、`2`。字段名提示生命、魔法与恢复，恢复单位未确认。
- `[anti evil]` 在两个样本均为 `12`，见上衣第 46 行和下装第 42 行。可定位抗魔相关值，但不能凭名称确认客户端倍率。
- 上衣 `[part set index]` 在第 18 行为 `217`。它是套装关联候选，应去 `etc/equipmentpartset.etc` 找首整数为 217 的 `[equipment part set]`。下装样本没有这个标签，不因它是勇者装备就补一个。
- 上衣 `[impossible contents]` 在 `equipment/character/common/jacket/cloth/coat_cl_2choro413.equ:72` 有六个字符串 `upgrade`、`amplify upgrade`、`disjoint`、`gift`、`separate upgrade`、`charac cargo`。同文件第 10 行说明也写有不可强化、增幅等限制。只改说明不会移除实际限制。
- 下装 `[skill data up]` 在 `equipment/character/common/pants/leather/pant_lt_2choro187.equ:68` 有两组七 token。第一组 `[gunner] 2 [dungeon type] [level] 3 % 9`，第二组职业为 `[at gunner]`。第 10 行说明写冰冻弹攻击力 `+9%%`，支持末尾 `% 9` 的显示解释。技能 ID `2`、等级数据列 `3` 必须分别查对应技能文件，不能当所有技能统一伤害列。

## 修改配方

1. 修改上衣面板防御先定位双值标签。保留两个整数。修改生命值则只动 `[HP MAX]`，不改同名套装奖励。
2. 修改租借限制时逐项核对 `[impossible contents]` 与说明。不要通过删除整文件实现解禁，删除既有输出会从归档移除该物品。
3. 修改技能加成时保留职业枚举、技能 ID、模式、数据域、列索引、运算符、数值的七 token 顺序。只改已确认的末值，核对男、女职业是否都应改变。
4. 保留 CRLF、TAB、原 token 类型和 `#PVF_File\r\n`。只能复用原归档已有字符串。中文需改 `.str` 原有键，本文空格不能覆盖源文件。
5. 核对双值、六项限制和技能组数。真实重建与提取，再检查面板、穿戴等级、租借限制和技能效果。单跑 `--verify` 不验证修改。

## 未知项

未确认装备双值计算、全部 sub type 枚举、速度和恢复单位。对未读过的肩、腰、鞋，必须先以该部位文件补证据再编辑。

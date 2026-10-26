# 辅助装备与魔法石修改手册

## 定位入口

`equipment/equipment.lst:2` 将 `440118` 映射到 `character/common/support/support_440118.equ`，将 `450063` 映射到 `character/common/magicstone/magicstone_450063.equ`。本页读取两个对应输出文件，各为 63 行。辅助装备与魔法石各自有部位枚举，不按文件名猜槽位。

## 参数与引用

- `[equipment type]` 在 `equipment/character/common/support/support_440118.equ:47` 是 `[support] 21`。在 `equipment/character/common/magicstone/magicstone_450063.equ:47` 是 `[magic stone] 21`。第二整数相同，字符串不同。`magic stone` 中间空格属于一个枚举 token。
- 辅助装备 `[grade]` 为 `65`、`[minimum level]` 为 `60`。魔法石为 `70` 和 `65`，分别见两个文件第 9、21 行。grade 与穿戴门槛不可合并。
- 辅助装备 `[usable job]` 是 `[swordman]`，魔法石是 `[at gunner]`，见两个文件第 15 行。名称中的狱血魔神或漫游枪手不能替代真实允许列表。
- `[physical attack]`、`[physical defense]`、`[magical attack]`、`[magical defense]` 在辅助装备第 23 到 30 行各为 `68`，魔法石同位置各为 `95`。本样本没有 `[equipment physical attack]` 或 `[equipment magical defense]` 的双值字段，不能照武器补双值。四个单值与力量、体力、智力、精神的对应可参照称号说明推断，修改前仍应核对面板。
- 辅助装备 `[skill levelup]` 在 `equipment/character/common/support/support_440118.equ:39` 为两组三元组 `[swordman] 85 2` 和 `[swordman] 24 2`。魔法石同标签为 `[at gunner] 101 2`、`[at gunner] 104 2`。形状是职业枚举、技能 ID、整数增量。分别查 `skill/swordmanskill.lst` 与 `skill/atgunnerskill.lst`，不能仅改数字而漏改职业。
- `[creation rate]` 辅助装备为 `50`，魔法石为 `30`，见两个文件第 37 行。它不是已确认的百分率，也没有证据表明改它能改变全部掉落率。
- 辅助装备 `[price]`、`[repair price]`、`[value]` 为 `78000`、`65520`、`62400`，魔法石为 `84000`、`70560`、`67200`，见两个文件第 31 到 36 行。三种金额分开保留，维修公式未确认。
- `[weight]` 辅助装备为 `700`、魔法石为 `300`，见两个文件第 51 行。单位未确认。
- `[routing priority]` 辅助装备第 59 行为字符串 `swordman` 加整数 `3`，魔法石为 `at gunner` 加整数 `1`。这里职业字符串没有方括号。可推断为职业分配优先信息，具体规则未确认。
- 两份文件各有两次 `[icon mark]`。第 13 行均是 `Item/IconMark.img 68`，第 57 行辅助装备是帧 `6`、魔法石是帧 `27`。不能假定只保留最后一次。
- 镶嵌映射在 `etc/chn_equipmentsockettypelist.etc:53` 与第 59 行。`[support]`、`[magic stone]` 下的 `[socket info]` 各为单字符串 `[S socket]`。这与其他装备双孔不同，不能套两孔模板。

## 修改配方

1. 先从索引确认物品 ID。改职业技能加成前查对应技能 `.lst`，再确认其等级上限与实际效果。
2. 调整单值属性时每次改一个字段，核对角色面板，不能用含 attack 的英文名直接判断是武器基础攻击。
3. 改穿戴门槛只动 `[minimum level]`。改镶嵌时核对独立孔映射，不把 `[equipment type]` 后的 21 改成孔数。
4. 保留 CRLF、TAB、`#PVF_File\r\n`、原字符串与数字类型。中文在 `.str` 原有键修改。本文展示空格不可覆盖源文件。
5. 核对三元组数、两个职业引用、重复 icon mark 和孔数。执行真实重建、提取与客户端穿戴、技能、镶嵌检查。`--verify` 不验证修改输出。

## 未知项

未确认 creation rate 的概率基数、routing priority 的竞争规则、四维属性最终换算和重量单位。仅改名称不能把辅助装备改成魔法石。

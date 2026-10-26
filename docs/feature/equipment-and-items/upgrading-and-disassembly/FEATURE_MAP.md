# 强化、增幅与分解修改手册

## 入口与样本

本页读取 `etc/upgrade.etc`、`etc/amplifyupgrade.etc`、`etc/disjoint.etc`、`etc/reseal.etc`、`etc/upgrade_separate.etc` 和 `etc/amplifyitem.etc`。强化与增幅有相似标签，但费用、材料、销毁门槛与专用数组不同。副职业分解机器另见 `character/expertjob/disjointer.exj`，不能用普通分解表覆盖。

装备自身也可能通过 `[impossible contents]` 禁用强化、增幅或分解，例如 `equipment/character/common/jacket/cloth/coat_cl_2choro413.equ:72`。先确认目标物品是否允许操作，再改全局表。

## 强化与增幅参数

- `[table]` 在 `etc/upgrade.etc:3` 有 4335 个数字 token，混合整数与浮点。开头 `2 0.017999999225139618 0.10000000149011612 0.032999999821186066 0.20000000298023224 0.6000000238418579 0 1 0 3037 10 1 ...`。增幅 `etc/amplifyupgrade.etc:3` 同为 4335 个 token，但对应位置为材料 ID `3242` 和整数 `1`。本页没有解释所有表列，不能把整行当纯成功率数组。
- `[notice]` 在两个文件第 7 行均为单整数 `12`。`[level]` 第 9 行均为四整数 `8 8 8 24`。通知与四列等级的完整含义未确认，不因标签叫 level 就按强化级别逐项递增。
- `[cost weights by rarity]` 在强化 `etc/upgrade.etc:13` 为六个数字 `0.5 1.5 3 5 8 4`，增幅同位置为 `0.25 0.75 1.5 2.5 4 2`。名称支持品质费用权重解释，但数组位置对应品质的顺序需确认，不能仅凭六种常见品质补全。
- `[stat weights by rarity]` 在强化 `etc/upgrade.etc:17` 与增幅同位置均有六个数字，开头 `0.4000000059604645 0.699999988079071 1`。它与 cost weights 独立，不应改费用时一起改属性。
- `[type]` 在 `etc/upgrade.etc:21` 有 12 个数字，开头 `1.2000000476837158 0 1`。增幅开头 `2.0 0 0.699999988079071`。类型槽映射未确认，不能把数字 0 当可删占位。
- `[cost]` 在 `etc/upgrade.etc:25` 为 100 个整数，前六个 `0 120 160 220 260 320`，末值 `70515`。增幅同标签也是 100 个整数，前六个 `0 600 800 1100 1300 1600`，末值 `87600`。没有显式等级键，索引对应装备等级还是其他维度需验证，不把它与后面的强化等级键值表混淆。
- `[repair cost rate by upgrade level]` 在两个文件第 29 行各有 100 个浮点 token，实测均为 `1.0`。维修倍率不等于强化成本，不把浮点改成整数 1。
- `[destroy level by rarity]` 在强化 `etc/upgrade.etc:33` 为 `common 10 uncommon 10`，增幅 `etc/amplifyupgrade.etc:33` 为 `common 8 uncommon 8`。这是字符串、整数对，不能替换成六元素数组。
- `[max upgrade level by rarity]` 在两个文件第 37 行均为 `common 50 uncommon 50`。未列出的品质不表示上限为零，也不能仅改这里保证所有品质都能到 50。
- `[cost weight by upgrade level]` 只在本次强化样本 `etc/upgrade.etc:59` 出现，为 19 对数字，键 `0` 到 `18`。首对 `0 0.5`，键 10 对 `1.5`，末对 `18 16`。该表有显式强化等级键，与无键 `[cost]` 分开定位。
- `[amplification const]` 在 `etc/amplifyupgrade.etc:59` 有 1020 个整数。开头 `0 0 0 0 1 1 1 1 2 2 2 2`。四列重复形状可观察，但四维属性排列和等级索引未确认，不能直接按四列四维全部重算。

## 锻造与异次元属性入口

- `[separate upgrade max]` 在 `etc/upgrade_separate.etc:7` 为单整数 `7`，`[level]` 第 9 行为单整数 `8`。它们与强化文件四整数的 level 形状不同，不能共用覆盖模板。
- 锻造 `[table]` 在 `etc/upgrade_separate.etc:3` 为 40 个混合数字 token，前两组可观察为 `2 1 10000 1` 与 `4 2 5000 1.1100000143051147`。列义不全，不能按强化大表套公式。
- `[item weights by grade]` 在 `etc/upgrade_separate.etc:11` 有 297 个整数，可观察为 99 组三元组。首组 `1 3326 1`，后续组含相同物品 ID `3326`。第一列递增，第三列改变，具体费用取整规则未确认。`[weapon weights]` 第 23 行另有 66 个浮点 `1.0`，不是同一数组。
- `[separate upgrade effect]` 在 `etc/upgrade_separate.etc:27` 有 54 个整数，首组六值 `255 255 255 0 50 2000`。形似颜色和表现参数，但没有协议证据，不能安全改成自造 RGB、透明度和时间列。
- `[option mapping table]` 在 `etc/amplifyitem.etc:3` 为六对字符串和整数，实际为 `[NONE] 0 [physical defense] 1 [magical defense] 2 [physical attack] 3 [magical attack] 4 [all] 5`。这是异次元属性编号映射，与品质数组分开。
- `[amplification rate by rarity]` 在 `etc/amplifyitem.etc:7` 为六整数 `0 0 12 2061 2000 2000`。`[option data]` 第 11 行则为四组三元组，首组 `[physical defense] 2500 5`。这些数值不证明概率分母是 10000，也不证明末列 5 为属性固定值。
- `[purify material]` 在 `etc/amplifyitem.etc:23` 为 `1183 1`，`[purify only material]` 第 25 行为 `10000408 1`。先查堆叠物索引确认净化材料，两个标签不能混用。
- `[invest option]` 在 `etc/amplifyitem.etc:27` 为属性枚举、材料 ID、数量的重复形状，首组 `[physical defense] 1186 1`。`[reinvest option]` 第 31 行首组为 `[physical defense] 1190 1`。赋予与重新赋予使用不同材料，修改某属性时按完整枚举定位。

## 失败补偿与普通分解

- 强化 `[disjoint]` 第 41 行内的 `[disjoint bonus item]` 为 `3243`，增幅同位置为 `3244`，见 `etc/upgrade.etc:43` 与 `etc/amplifyupgrade.etc:43`。堆叠物索引分别解析为 `material/vestiges_intensive.stk` 和 `material/crystal_pure.stk`，不能当成同一补偿材料。
- 该上下文 `[equip level const]` 为 `40`，`[upgrade const for bonus item count]` 为 `10`。`[upgrade failed bonus weight by rarity]` 在强化第 47 行是 `rare 1.0 unique 1.2000000476837158 epic 1.5 chronicle 1.0`。这是失败补偿权重，不是强化成功率。
- `[correction grade by rarity]` 在 `etc/upgrade.etc:53` 为六对 `common 1 uncommon 1 rare 2 unique 4 epic 5 chronicle 3`。键显式存在，可核对名称，但不能凭此断言其他无键品质数组同序。
- `[cube index]` 在 `etc/disjoint.etc:3`、第 7、11、15、19 行重复五次。首字符串分别是 `[no element]`、`[fire element]`、`[water element]`、`[light element]`、`[dark element]`。每块各有十个整数 ID。无属性块全为 `3037`，火块全为 `3035`。按元素字符串定位，不替换所有 cube index。
- `[legacy info]` 在 `etc/disjoint.etc:23` 以 `1 3037` 开头，后面是 `20002 5000` 等六组整数对。第 27 行另一个块以 `2 3037` 开头。记录形状像档位、基础材料和候选权重，完整列义未确认。
- `[skill info]` 在 `etc/disjoint.etc:43` 是混合 token `179 [swordman] 2 42 [dark element] [fighter] 1 41 [light element]`。职业、技能与元素关联需查技能列表，不把所有整数当物品 ID。
- `[cube creation const]` 在 `etc/disjoint.etc:49` 为七个数字，首值 `150`，随后含浮点 `1.2000000476837158`。`[additional result]` 第 51 行为 `0 4 3033 3034 3035 3036 1 3166 1 3167 1 3260 1 3228`。它与第 53 行 `[additional result const]` 的 21 个数字分开，未知列不能安全重排。
- `[avatar disjoint info]` 第 55 行内按职业标签分块。`etc/disjoint.etc:65` 的 `[swordman]` 内有 15 个整数，首五值 `2559000 2559003 2559006 2559009 2559006`。第 103 行另有 `[avatar disjoint for parts info]`。职业表与部位表是两个结构，不能混用。

## 重新封装与修改步骤

- `[grade]` 在 `etc/reseal.etc:3` 为五整数 `1 2 3 5 5`。`[rarity weight]` 第 7 行为六整数 `1 2 3 4 8 8`，`[extended rarity weight]` 第 11 行为六整数 `0 0 1 1 1 1`。三个数组长度不同，不能按同一维度拉齐。具体费用公式与扩展品质含义未确认。

1. 先确定改强化、增幅、普通分解、时装分解还是重新封装。改费用优先选择已确认的单字段或显式键值，不在混合 `[table]` 猜列。
2. 改品质门槛保留显式字符串键。改失败补偿需解析材料 ID，并留在 `[disjoint]` 内。改分解结果按元素、职业或部位上下文定位。
3. 未解释的 4335 token 大表和封装数组不能安全重算。不能因为名称有 rate 或 weight 就写为百分比。
4. 保留 CRLF、TAB、`#PVF_File\r\n`、整数与浮点 token 类型。只复用已有字符串。本文空格不是源文件分隔。
5. 核对费用与维修数组各 100 项、显式键值、补偿物品及未改文件。需要真实重建与提取，再实机验证成功、失败、费用、维修和分解边界。`--verify` 只检查原归档往返。

## 强化成本与成功率边界

`etc/upgrade.etc` 的 `[table]` 有 4335 个混合 token，其中含材料 ID `3037`。完整列义与成功率公式尚未确认，不能把材料、消耗数量和成功率参数混为一列，也不能把某值改为 0 就认定强化必定成功。

修改已有装备的强化成本时，先区分 `[cost]`、品质权重、强化等级权重与失败补偿。只改已有证据支持的目标字段。增幅与强化分别核对数据，不按相似标签直接复制数列。

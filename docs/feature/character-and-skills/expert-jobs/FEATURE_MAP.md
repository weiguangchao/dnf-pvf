# 副职业修改手册

## 定位与样本

`character/expertjob.lst:2` 有四组编号与路径。`1` 为 `expertjob/enchanter.exj`，`2` 为 `expertjob/alchemist.exj`，`3` 为 `expertjob/disjointer.exj`，`4` 为 `expertjob/doll_controller.exj`。本页读取了这四个完整文件和 `character/expertjob.etc`。配方与产物还要通过 `stackable/stackable.lst` 解 ID，不能只改副职业目录名。

## 共有字段

- `[clear quests]` 是带结束标签的整数列表。`character/expertjob/alchemist.exj:3` 为 `2708`，分解师为 `2710`，附魔师为 `2702`，控偶师为 `2712`。字段名提示前置任务，任务编号仍需去任务索引确认。
- `[giveup cost]` 在四个样本第 7 行均有四整数 `100000 200000 400000 1000000`。名称提示放弃成本，但四列对应哪些等级未确认，不能当四职业各自的费用。
- `[expertness exp]` 在四个样本第 11 行均含 11 组整数、整数、本地化引用。炼金第一组 `50 0 <0::alchemist_1` 加中文名称，末组为 `620 0 <0::alchemist_11`，见 `character/expertjob/alchemist.exj:12` 到第 22 行。经验是累计门槛还是逐级消耗未确认。第二整数不能凭始终为 0 就删除。
- `[compound rate]` 在 `character/expertjob/alchemist.exj:26` 有 20 个整数，可分五组四元组，首组 `-2 100 0 0`，末组 `2 50 3 4`。附魔同位置末组 `2 50 7 9`，控偶末组 `2 50 6 8`。名称提示合成概率，负数和每列概率基数未确认，不能把全部列当百分比。
- `[items]` 在炼金、附魔、控偶各文件第 30 行分别有 328、760、212 个整数。炼金首组 `0 2600149 1110 1`，附魔首组 `0 2600141 2610034 1`，控偶首组 `0 2600083 2600029 1`。序号、配方 ID、产物 ID、需求等级的四列解释需结合具体 `.stk` 验证，不能只凭数值位数认定。
- `[skill]` 在炼金 `character/expertjob/alchemist.exj:34` 为 `193 1`，附魔为 `191 1`，控偶为 `192 1`，分解师在 `character/expertjob/disjointer.exj:58` 为 `194 1`。这是两整数形状。需在对应职业技能列表核对 ID，不能当物品引用。
- `[expertjob level limit]` 在 `character/expertjob.etc:7` 是 11 组整数对，开头 `1 20 2 20 3 30`，结尾 `11 70`。名称提示副职业等级与角色等级限制的映射，边界规则未确认。

## 分解师专用表

- `[upgrade cost]` 在 `character/expertjob/disjointer.exj:26` 有 22 个整数，按 11 对读取，首对 `1 0`，末对 `11 600000`。与 `[endurance repair cost]` 第 30 行的 22 个整数分开修改，后者首对 `10000 300`、末对 `60000 700`，没有从 1 递增的键。
- `[limit disjoint gold]` 第 34 行为 `10000`，`[endurance reduce]` 第 36 行为 `1 3`，`[endurance initial value]` 第 38 行为 `300`，见 `character/expertjob/disjointer.exj`。可分别推断收费上限、耐久变化范围、初始耐久，金币和耐久的精确计算还需验证。
- `[additional result]` 在 `character/expertjob/disjointer.exj:46` 有 78 个数字 token，可按 13 组六元组观察。首组 `1 0 99 3033 2500 7.800000190734863`。`[big win result]` 第 50 行有 66 个数字 token，首组末值为 `0.28999999165534973`。两张表不能按相同行数覆盖。
- `[disjoint result]` 在 `character/expertjob/disjointer.exj:54` 有 688 个数字 token，可按 86 组八元组观察。首组 `0 0 0 3037 0.800000011920929 0 0 0`。混合整数、浮点以及多组筛选值，列义不全，不能安全整表重算。
- `[disjoint self service]` 在 `character/expertjob/disjointer.exj:66` 为 `80 2610045 1`。名称提示自助分解，物品引用 `2610045` 需查堆叠物索引，其他两列不能凭名称定单位。

## 其他专用表

- 炼金 `[potion info]` 在 `character/expertjob/alchemist.exj:38` 是三对整数 `2600018 5000 2600025 100 690000190 10000`。`[alchemist extraction result item]` 第 50 行则为物品、字符串类别、整数的重复形状，首组 `2610001 food 200`。`food`、`life`、`jewel` 是实际枚举字符串，不能翻译。
- 附魔 `[monstercard bind info]` 在 `character/expertjob/enchanter.exj:38` 为九整数 `0 100 0 1 200 0 2 300 0`。`[monstercard bind list]` 第 46 行首组三整数 `3619 0 500`。列表中的物品需解析到卡片，不能把末列 500 直接写成成功率。
- 控偶 `[shop doll info]` 在 `character/expertjob/doll_controller.exj:38` 为三对 `0 1 1 2 2 3`。`[doll_controller extraction result item]` 第 46 行为 16 个整数，首组 `2610042 1 30 500`，末组 `2610048 71 80 500`。中间两列呈连续范围，是否角色等级仍待确认。

## 修改步骤与未知项

1. 先按 `.lst` 选副职业。改经验只动 `[expertness exp]` 的目标整数，保留 11 组和本地化引用。改中文只改原 `.str` 键值，不能只改内联显示文字。
2. 改配方先查 `.stk` 的配方块和结果 ID，再核对 `[items]` 中对应四元组。改机器升级费用和耐久维修费用时分别定位标签，不共用解释。
3. 未确认的结果矩阵与概率列不能安全编辑。保留小数 token，不把 `2500` 或 `500` 自行换算为百分比。
4. 保存 CRLF、TAB、`#PVF_File\r\n` 与原类型。保留已存在的字符串与路径。本文空格不是源文件分隔。
5. 核对修改表的组数、索引及关联物品。执行真实重建与提取，再检查升级、制作或分解的实际结果。`--verify` 不是修改验证。

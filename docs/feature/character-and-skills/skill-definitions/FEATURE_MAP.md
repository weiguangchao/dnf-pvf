# 技能定义与技能列表修改手册

## 定位入口

`skill/skilllist.lst:2` 有 11 组职业编号与列表路径，`0` 对应 `SwordmanSkill.lst`。`skill/swordmanskill.lst:2` 的技能 `8` 对应 `Swordman/TripleSlash.skl`。输出文件是 `skill/swordman/tripleslash.skl`。本页完整读取其 95 行，以下数据均来自该样本，不能推广为所有技能共用的列定义。

## 基础字段与 token

- `[name]` 在 `skill/swordman/tripleslash.skl:3` 是 `<12::name_18090` 加显示文字三段斩。`[basic explain]` 第 9 行是另一个本地化引用。要改中文需改 `skill/skill.kor.str` 中对应既有键，改引用内显示文字不会进入编译结果。
- `[type]` 在 `skill/swordman/tripleslash.skl:23` 为单个字符串 `[active]`。`[skill class]` 第 25 行为单个整数 `1`。前者是枚举，后者具体分类映射未确认。
- `[maximum level]` 在 `skill/swordman/tripleslash.skl:27` 为 `70`。`[growtype maximum level]` 第 29 行为六整数 `50 50 50 50 50 50`。全局上限与转职数组不是同一字段。
- `[skill fitness growtype]` 在 `skill/swordman/tripleslash.skl:31` 为五整数 `0 1 2 3 4`，有结束标签。它与六元素上限数组长度不同，不能按位置直接合并。
- `[weapon effect type]` 在 `skill/swordman/tripleslash.skl:39` 为 `[physical]` 字符串。它与动作 `.atk` 的无值 `[physic]` 标签拼写、类型均不同。
- `[icon]` 在 `skill/swordman/tripleslash.skl:41` 为四 token，路径、整数、同路径、整数，帧索引为 `18` 和 `19`。路径为 `Character/Swordman/Effect/SkillIcon.img`。不能换成不存在的新字符串。
- `[command]` 在 `skill/swordman/tripleslash.skl:43` 到第 48 行含 ``{6=`(RIGHT)`}``、``{8=`&`}``、``{6=`(SKILL)`}``。类型 6 和 8 必须保留，普通反引号 token 不能替代。

## 模式块与等级数组

- `[dungeon]` 第 55 行下的 `[consume MP]` 是两个整数 `12 120`，见 `skill/swordman/tripleslash.skl:57`。这是两个端点形状，插值规则未确认，不能当成两级的完整数组。
- 副本 `[cool time]` 为 `6000 6000`，见 `skill/swordman/tripleslash.skl:59`。`[pvp]` 第 71 行内同标签为 `8000 8000`。毫秒单位是常见解释，但本样本未声明单位，本文不据此保证六秒或八秒。
- 副本 `[static data]` 在 `skill/swordman/tripleslash.skl:61` 为两个整数 `600 -1000`。列义未确认，不能把负数视为异常。
- 副本 `[level info]` 在 `skill/swordman/tripleslash.skl:65` 有 421 个整数。首值为 `6`，余下 420 个能分成 70 组六元组。第一组 `158 198 198 47 138 158`，第二组 `177 266 266 53 186 212`。这支持首值为列宽的解释，不能因此把首值当一级伤害。
- PVP `[level info]` 在 `skill/swordman/tripleslash.skl:75` 同样有 421 个整数，首值 `6`，第一组六值 `30 43 55 3 4 6`。改副本数组不应同步覆盖 PVP 数组。
- `[level property]` 在 `skill/swordman/tripleslash.skl:89` 用 `1 99`、本地化说明及后续映射描述等级显示。第 91 行有 `-1 0 1.0 -2 3 1.0` 等三元组。说明含 `<int>%% + <int>`，提示部分列参与百分比和固定值展示，但六列全部运行时语义、映射负号规则仍未确认。
- `[feature skill index]` 在 `skill/swordman/tripleslash.skl:94` 为单整数 `143`。应在相同职业技能列表解析该引用，不要当作物品 ID。

## 修改与验证

1. 先通过两层 `.lst` 定位职业和技能 ID。记录模式块。只修改需求明确的一种模式。
2. 改等级表时保留首值 `6`、70 组六元组和整数类型。没有列语义证据时不能安全批量改六列。先结合显示映射与实机单级对照确认目标列。
3. 改 MP 或冷却时保留两整数形状。改指令时保留 `{6}` 与 `{8}` 类型。改文本时改 `.str` 原有键并保留原编码。
4. 保存 CRLF、TAB 与 `#PVF_File\r\n`。本文摘出的空格序列不是可覆盖文件。
5. 核对副本与 PVP 的 token 数、首尾等级及未改模式。需要真实重建、重新提取及客户端各等级验证。`--verify` 只检查原归档往返。

## 未知项

本页没有确认六列全部伤害意义、端点插值、冷却单位或技能分类枚举。空的 `[death tower]` 与 `[warroom]` 块保留，不推断为空即禁用。

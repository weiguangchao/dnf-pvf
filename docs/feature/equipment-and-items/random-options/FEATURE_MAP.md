# 随机词条与重置修改手册

## 入口与引用顺序

本页读了 `etc/randomoption` 下的 `randomoption.lst`、`optiongrouping.etc`、`optiongroupselection.etc`、`optionquantity.etc`、`partselection.etc`、`optionnumbering.etc`、`regenerationrandomoption.etc`、`optiontext.etc` 和具体中毒效果样本。先确定装备的 `[item group name]`，再追部位选择、词条组、词条 ID 与效果。目录名不能代替这条引用链。

`etc/randomoption/randomoption.lst:2` 有 125 对整数与路径，其中 `8` 对 `Options/RandomOptions_8_poison.etc`，输出文件为 `etc/randomoption/options/randomoptions_8_poison.etc`。另有 `etc/randomoption/randomoptionskill.lst:2` 从 `180` 起映射技能类词条路径，不能把 180 直接当某职业技能 ID。

## 抽取与数量

- `[quantity ratio]` 在 `etc/randomoption/optionquantity.etc:3` 为六整数 `1 10000 2 5000 3 900`，呈数量、权重对形状。总和不是 100，不能把 10000 说成百分之百。
- `[option quantity]` 在同文件第 7 行为 1476 个整数。开头两个六元组 `2 -1 1 1 1 2`、`2 -1 1 5 1 2`，尾组 `3 -1 3 200 1 3`。六列规则未全部确认，`-1` 必须保留。不能按"等级、数量"两列覆盖。
- `[part type]` 在 `etc/randomoption/partselection.etc:3` 有 7308 个 token，字符串按反引号整体计数，可观察为 2436 组三元组。首组 `1 cl coat 10000`，`1 mt coat 0` 也实际存在。中间字符串含空格，按空白切列会算错。前整数含 1 到更高取值，不能凭一例确认全部是等级。
- `[choose option group]` 在 `etc/randomoption/optiongroupselection.etc:3` 有 168840 个 token。首个十二元组 `2 -1 cl coat 1 1 3 303 303 304 0 0 300`，第二组开头对应 `2 -1 cl coat 1 5`。`[modified option selection]` 第 7 行也是 168840 个 token。两块用途名称不同，不能因开头相同就认定可共用编辑。
- `[option group]` 在 `etc/randomoption/optiongrouping.etc:3` 的第一个块有 45 个整数，首值 `1`，后跟 22 对候选 ID、整数权重，开头 `1 10000 2 10000`。按首值定位组，不按"第几个同名标签"定位。
- 组 `303` 在 `etc/randomoption/optiongrouping.etc:579` 有九整数 `303 74 10000 75 10000 76 10000 77 7000`。组 `304` 第 583 行则有 23 个整数。上游十二元组实际引用了 303、304。末尾 300 的含义未确认，不因为形似组号就保证能在分组文件找到。
- `[option value ratio]` 在 `etc/randomoption/optionnumbering.etc:3` 有 12 个混合浮点与整数 token，首组三值 `0.10000000149011612 0.30000001192092896 25`，末组 `0.800000011920929 1 50000`。可观察为范围样式加权值，但未确认分母与插值，不把小数统一转百分比。

## 具体词条效果

以下均为 `etc/randomoption/options/randomoptions_8_poison.etc` 的 `[dungeon]`、`[option] 8`、`[level] 1` 上下文，不是全文件所有同名标签。

- `[cooltime]` 在第 11 行是两个整数 `10000 19000`。`[attack success]` 第 13 行是 `1 1`。它们在 `[if]` 内，需保留 `[/if]`。
- `[target]` 在第 19 行为四 token `enemy -1 enemy -1`。它在 `[then]` 内，是成对端点形状，不能删成单个 enemy。
- `[duration]` 第 21 行为 `4000 6000`，`[probability]` 第 23 行为 `1 5`。名称提示时长与概率，但时间单位和概率基数未独立确认。
- `[active status]` 第 25 行为六 token `poison 1 501 poison 3 605`。到 `[level] 5` 的第 49 行变为 `poison 5 505 poison 7 625`。可观察状态名固定、四个整数随级别改变。状态等级和伤害列的对应需要继续验证，不能把所有数字都当中毒伤害。
- 简单词条 `etc/randomoption/randomoptions.etc:3` 的 `[dungeon]`、`[option] 1`、`[level] 1` 下 `[physical critical hit]` 为 `3 100`，第 95 行另有 `[pvp]`。同一标签的两个整数也不能自动按 min、max 解释。
- `etc/randomoption/optiontext.etc:18` 将 `8` 对应到中毒说明引用，含 `%d%%`、`%d秒`、每 `0.5秒` 伤害等文本。这能确认显示意图，不能单独证明 active status 各列的运行时算法。修改文字要改 `.str` 中的原有键，保留占位符数量和类型。

## 重置配置与修改配方

- `[choose part]` 在 `etc/randomoption/regenerationrandomoption.etc:13` 为编号 `3`、本地化引用和五个字符串 `club lswd katana ssword beamswd`。第 58 行编号 `12` 包含 `amulet wrist ring support magic stone`。这些字符串与物品 group name 关联，不是文件夹名。
- `[adjust quantity ratio]` 在重置文件第 63 行为 `101`、本地化引用，再跟三个整数 `10 80 10`。`[regeneration price]` 第 68 行是以 `80 1 5 0 75 10 0 100 ...` 开头的长整数序列，完整记录格式未确认，不能当单一价格数组覆盖。

1. 先记录装备 group name 和目标等级、品质条件。沿上游选择表找到组号，再在组表定位首整数，最后通过 `.lst` 解词条 ID。
2. 修改已有组内某候选权重时保持 ID、整数对和组头。没有概率归一化证据时只能做相对权重调整并标明待实机统计，不能宣称得到固定掉率。
3. 修改效果时按模式、option ID、level、if 或 then 定位。保留双端点数量与 token 类型。未解释的六列或十二列选择规则不能安全批量重写。
4. 保留 CRLF、TAB、`#PVF_File\r\n` 和全部字符串拼写。新路径、枚举和文本键不能由 output 新增来扩展归档。Markdown 空格不保留源文件分隔。
5. 核对分组引用、长表 token 数、整数与浮点类型和未改模式。需要真实重建与提取，客户端分别检查抽取、重置、属性显示及效果。`--verify` 不验证修改输出。

本页确认了组表与词条文件的引用，但没有确认全部筛选列、随机端点插值和概率分母。未知列不能凭标签名补解释。

# 职业武器修改手册

## 定位与样本

先在 `equipment/equipment.lst:2` 按物品 ID 查路径。实测 `27733` 对应 `character/swordman/weapon/katana/kat_hightechq.equ`。磁盘文件为 `equipment/character/swordman/weapon/katana/kat_hightechq.equ`，共 91 行。另读了 `equipment/character/gunner/weapon/revolver/n_rev_coltdiamond.equ` 的 91 行，以核对双职业与技能引用。

## 属性与适用范围

- `[usable job]` 在太刀 `equipment/character/swordman/weapon/katana/kat_hightechq.equ:15` 含两个字符串 `[swordman] [demonic swordman]`。左轮 `equipment/character/gunner/weapon/revolver/n_rev_coltdiamond.equ:15` 则为 `[gunner] [at gunner]`。职业枚举有空格，不能按空白切成多 token。
- `[grade]` 为整数 `62`，`[minimum level]` 为整数 `60`，见 `equipment/character/swordman/weapon/katana/kat_hightechq.equ:9` 和第 21 行。两者实测不同，不能把 grade 当穿戴等级一起改。
- `[rarity]` 在太刀第 11 行为整数 `2`。本页只确认编号，不自定其品质名称与完整枚举。
- `[equipment type]` 在 `equipment/character/swordman/weapon/katana/kat_hightechq.equ:51` 是字符串 `[weapon]` 加整数 `22`。`[sub type]` 第 77 行为单整数 `1`，`[item group name]` 第 85 行为 `katana`。左轮也是 `[weapon] 22`，但 sub type 是 `0`，组名为 `revolver`。第二整数 22 不能当作武器种类。
- `[physical attack]` 在太刀第 23 行为 `39`，`[magical attack]` 第 25 行为 `59`。`[equipment physical attack]` 第 39 行却为两个整数 `517 498`，`[equipment magical attack]` 第 41 行为 `571 550`。单值与装备面板双值属于不同字段，不能互换。
- `[separate attack]` 在 `equipment/character/swordman/weapon/katana/kat_hightechq.equ:43` 为 `270 182`。双值呈降序，不应擅自标成最小值、最大值或交换顺序。品质浮动与面板换算未确认。
- `[attack speed]` 为 `80`，`[cast speed]` 为 `40`，`[physical critical hit]` 为 `2`，见太刀第 27、29、45 行。整数形状已确认，显示倍率和百分比单位未确认。
- `[price]`、`[repair price]`、`[value]` 分别为 `86800`、`72912`、`69440`，见 `equipment/character/swordman/weapon/katana/kat_hightechq.equ:33` 到第 38 行。售价、维修和价值是独立输入，完整公式未确认。
- `[durability]` 为 `35`，`[weight]` 为 `2800`，见太刀第 81 到 84 行。不能仅凭常见 UI 值断言 weight 以克为单位。
- 左轮 `[skill levelup]` 在 `equipment/character/gunner/weapon/revolver/n_rev_coltdiamond.equ:39` 有两组三元组 `[gunner] 30 1` 与 `[at gunner] 30 1`。按各职业技能表查 ID `30`，不要把同号自动当同一全局技能。
- 左轮 `[elemental property]` 在 `equipment/character/gunner/weapon/revolver/n_rev_coltdiamond.equ:89` 是字符串 `[light element]`。这是字符串值，不能改成 `.atk` 中的无值标签形状。

## 重复动画段

太刀 `equipment/character/swordman/weapon/katana/kat_hightechq.equ:53` 起的 `[animation job]` 是 `[swordman]`，第 65 行起另一个是 `[demonic swordman]`。各段的 `[variation]` 均为 `13 4`。各段各有两次 `[layer variation]`，依次为 `2790 katanac` 和 `650 katanab`，并各自跟随 `[equipment ani script]`。前段使用 `equipment/character/swordman.lay`，后段使用 `equipment/character/dsswordman.lay`。改外观时按职业段和层名定位，不全文替换所有同名标签。

太刀第 13 行和第 89 行都出现 `[icon mark]`，帧号分别是 `64` 与 `31`。文件没有证明后者覆盖前者，保留两次出现及顺序。

## 修改步骤与验证

1. 由装备索引确定 ID 和实际文件。先选改穿戴、属性、技能还是外观。只修改对应块。
2. 改基础攻击时保留双值数量和顺序。未确认双值语义时不能安全重算两列。改技能时保留职业、技能 ID、等级增量的三元组。
3. 改外观只复用原归档已有路径、层名和字符串。职业允许列表与动画段要一起检查，不只补一个职业名字。
4. 保留 CRLF、TAB、`#PVF_File\r\n`、原整数和浮点类型。中文改 `equipment/equipment.kor.str` 的既有键，内联显示文字不参与编译。本文空格不是源文件分隔。
5. 核对双数值、三元组、重复动画段和未改字段。真实重建并重新提取，再检查两个职业的穿戴、面板、技能和动作。`--verify` 不验证修改后的 output。

## 未知项

本页未确认品质编号、双值算法、重量和速度单位、`[Force Result Item Rule]` 的左轮参数含义。不能据目录名推导所有职业的 sub type 枚举。

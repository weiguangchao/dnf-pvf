# 职业与角色定义修改手册

## 入口与边界

修改基础职业时，先读 `character/character.lst:2`。实测有 11 组整数与路径，例如 `0` 配 `Swordman/Swordman.chr`，`9` 配 `Swordman/DemonicSwordman.chr`。路径相对 `character`。输出磁盘对应 `character/swordman/swordman.chr`。职业编号不等于转职编号。

本页以该 592 行 `.chr` 和 `character/characteretc/swordman.etc` 为证据。技能编号还要查 `skill/skilllist.lst:2` 和 `skill/swordmanskill.lst:2`，装备编号查 `equipment/equipment.lst`。

## 已观察字段

- `[job]` 后是一个反引号枚举。`character/swordman/swordman.chr:3` 为 `[swordman]`。这是职业标识，不是可翻译名称。
- `[growtype name]` 后有六个本地化引用。`character/swordman/swordman.chr:5` 到第 11 行依次含 `growtype_name_75` 到 `growtype_name_95` 及 `growtype_name_171`。中文显示依次为鬼剑士、剑魂、鬼泣、狂战士、阿修罗、征服者。它们的顺序需与既有转职结构一起保留，不能把六个名字直接当六个职业 ID。
- `[width]` 有两个整数 `40 10`，见 `character/swordman/swordman.chr:13`。两列轴向含义未确认。
- `[initial value]` 是后续基础值的上下文。其 `[HP MAX]` 为单个浮点 `180.0`，`[MP MAX]` 为 `140.0`，见 `character/swordman/swordman.chr:15` 到第 20 行。`[physical attack]` 为 `7.5`，`[magical attack]` 为 `4.5`。这些不是文件内所有同名字段的统一值。
- 初始块的 `[move speed]` 为 `850.0`，`[attack speed]` 为 `850.0`，`[cast speed]` 为 `700.0`，见 `character/swordman/swordman.chr:37` 到第 42 行。实测为浮点数。客户端显示换算和时间单位未确认，不应直接写成百分比。
- `[growtype 1]` 内 `[HP MAX]` 为 `45.0`，`[growtype 2]` 内为 `50.0`，见 `character/swordman/swordman.chr:55` 和第 77 行。名称提示这些可能是成长系数，逐级叠加规则仍需实机确认。修改时必须指定所在 growtype。
- `[skill]` 是带结束标签的整数序列。初始块 `character/swordman/swordman.chr:51` 有 16 个整数，形如 `181 2 182 2`。`[growtype 2]` 下第 97 行另有 16 个整数，首组 `27 1`。按职业技能表解析为技能 ID 与等级是有依据的推断，不能按全局技能 ID 解释。
- `[module damage rate]` 为四个浮点数。`[growtype 2]` 内 `character/swordman/swordman.chr:101` 是 `0.699999988079071 1.0 1.100000023841858 0.699999988079071`。四列与伤害模块的对应未确认。
- `[awakening 1]` 与 `[awakening 2]` 在每个转职段内再次出现。剑魂段的 `[awakening skill]` 在 `character/swordman/swordman.chr:127` 为 `91 1`，第 153 行的二次觉醒块为空。不能用全文替换填充所有空块。
- `.etc` 的 `[equipment index]` 在 `character/characteretc/swordman.etc:3` 是字符串 `defaultEquipment` 加 11 个整数，包含 `-1 39400 -1 40600`。`-1` 是现有占位值，其具体部位须结合外观层次确认。
- `.etc` 的 `[key value string]` 需要连同块内首个键定位。`character/characteretc/swordman.etc:35` 的 `growTypeEquipmentFileName` 后有空串、整数与路径，含 `character/swordman/growtype/weaponmaster.equ`。第 11 行同标签却是 `christmas2007Sound`，两者不能混改。
- `.etc` 的 `[key value index]` 同样靠键区分。`character/characteretc/swordman.etc:39` 的 `weaponSubTypeIndex` 有 `27900 0 27000 1 ... 5 28200` 共 13 个整数。形状像默认值加索引映射，但不能把它重排成固定三列。

## 修改步骤

1. 记录职业索引、growtype 段和觉醒段。改基础属性只动 `[initial value]` 下的目标浮点数。改转职成长只动对应 `[growtype N]` 中的同名字段。
2. 改赠送技能时，先在该职业 `.lst` 解析 ID，再保留 ID 与等级的成组关系和 `[/skill]`。改装备关联时先解析装备索引，保留 `-1` 和空串。
3. 改职业名称时修改对应 `.str` 的原有键值。`<0::key` 后的显示文字不会成为编译输入。保留 module 与 key。
4. 保存时保留 `#PVF_File\r\n`、CRLF、TAB 和原 token 类型。本文展示的空格不是可直接覆盖源文件的分隔符。
5. 比较修改前后所在块的 token 数量与类型。执行真实重建并重新提取核对，再在客户端验证基础属性、转职与觉醒。`--verify` 只验证原归档往返，不能证明修改已生效。

## 未知项

本页确认了数值形状和块位置，没有确认客户端成长公式、四列模块系数或装备槽编号。没有运行时证据时只改已定位的现有数值，不扩展枚举和路径字符串。

# 技能学习与加点修改手册

## 入口

单技能学习字段在 `skill/swordman/tripleslash.skl`。职业技能 ID 由 `skill/swordmanskill.lst:2` 解析，三段斩为 `8`。自动加点入口为 `skill/autoskill.lst`，样本为 `skill/autoskill/swordmanautoskill.skl`。技能树界面另在 `clientonly/skilltree/swordman_sp.co` 与 `clientonly/skilltree/swordman_tp.co`，不是 `.skl` 的替代。

## 学习成本与限制

- `[purchase cost]` 在 `skill/swordman/tripleslash.skl:15` 为一个整数 `15`，有结束标签。结合学习用途推断为购买该技能等级的点数成本，具体 SP 或其他点种要核对技能分类，不能改成金额文本。
- `[required level]` 在 `skill/swordman/tripleslash.skl:19` 为 `15`。`[required level range]` 第 21 行为 `2`。名称提示首级门槛与后续等级间隔，是否按公式逐级增加需运行时确认。
- `[maximum level]` 第 27 行为 `70`，`[growtype maximum level]` 第 29 行为六整数 `50 50 50 50 50 50`，见 `skill/swordman/tripleslash.skl`。只改最大等级不能证明玩家可学至该级，还需核对职业限制、等级表和点数。
- `[skill fitness growtype]` 在 `skill/swordman/tripleslash.skl:31` 有 `0 1 2 3 4` 五个整数。它是独立允许列表形状，不能用六元素上限数组覆盖。
- `[sp table]` 在 `etc/sptable.etc:3` 有 400 个整数，可按 200 组键值阅读。前四组 `1 0 2 30 3 30 4 30`，第 11 组 `11 60`，末组 `200 570`。键递增支持等级与点数关系，数值为本级发放还是累计总量未确认。

## 自动加点与界面

- `[job]` 在 `skill/autoskill/swordmanautoskill.skl:3` 为字符串 `swordman`。这里没有方括号，不能照搬技能树的 `[swordman]`。
- `[growtype]` 在 `skill/autoskill/swordmanautoskill.skl:5` 为字符串 `0`，后续第 11、17、23、29 行分别为字符串 `1` 到 `4`。保留字符串类型，不能因为内容是数字就改整数。
- `[AutoSkill]` 大小写固定。第一个块 `skill/autoskill/swordmanautoskill.skl:7` 的开头是 `1 5 1 46 1 169 1 181 2 182 2 184 1 0 2 5 1 ...`。可观察到等级样式头部、技能与等级配对及 `0` 分隔的重复模式。完整记录语法未从样本独立确认，不能把所有 `0` 都当技能等级修改。
- growtype `1` 的 `[AutoSkill]` 在 `skill/autoskill/swordmanautoskill.skl:13` 开头为 `15 5 1 46 5 169 1`。它不从整数 `1` 开始。不能按固定相同行偏移拷贝各转职数据。
- `[character job]` 在 `clientonly/skilltree/swordman_sp.co:3` 为两个字符串 `[swordman] none`。SP 第一个 `[skill info]` 块的 `[index]` 为 `5`，`[icon pos]` 为 `141 0`，见第 5 到 11 行。后一个块的 index 是 `46`，位置 `235 0`。同名标签必须按所属 `[skill info]` 定位。
- TP 样本 `clientonly/skilltree/swordman_tp.co:7` 的首个 index 是 `161`，位置为 `0 0`。SP、TP 文件中的 index 都需查职业 `.lst`，不能把画面位置当作学习门槛。

## 修改配方

1. 修改学习门槛时同时记录单技能的 cost、required level、range 和两类上限。保持各字段原 token 数，不因改上限自动扩充等级表。
2. 修改点数表时保留 200 组键值和键的顺序。先确认实际生效模式，不能用 PVP 的同类表替换普通表。
3. 调整界面位置只动目标技能块的两个整数。调整自动加点前先证明该记录边界和技能等级关系，未确认语法时不能安全编辑长序列。
4. 保留 CRLF、TAB、原字符串类型和 `#PVF_File\r\n`。Markdown 空格不是源文件分隔。
5. 分别核对学习按钮、升级成本、各转职上限、自动加点结果和 SP、TP 界面。重建后重新提取，不能用 `--verify` 代替修改验证。

## 未知项

点数累计规则、自动加点长序列完整语法、图标坐标单位未确认。界面树可见不证明角色实际能学，需逐一验证条件。

## 按等级调整 SP 点数

`etc/sptable.etc` 有显式等级键 `1` 至 `200`。调整某等级的 SP 时，按等级键查找对应值。该值是否表示每级发放量，以及角色已有点数是否重算，仍需实机核对。

按目标等级键修改对应值，保留 200 对与键顺序。只修改需求指定的等级和点数，不连带修改自动加点、技能上限或 QP 商店。

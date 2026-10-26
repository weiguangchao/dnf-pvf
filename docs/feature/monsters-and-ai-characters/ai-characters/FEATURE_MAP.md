# AI 角色与人偶功能索引

职业 AI 角色、人偶及专用 AI 参数。

## 功能范围

- 按职业组织的 AI 角色与人偶。
- AI 操作参数、样例和绝望之塔相关角色配置。

## 分类依据

已观察到各职业 AI 分组、operatingvalue 参数、样例分组以及 towerofdespair_apc 条目。

## 定位与样本

从 `output/aicharacter/aicharacter.lst` 按 AI 角色 ID 查找。本文读取了 `output/aicharacter/swordman/15kuran/15kuran.aic` 和同目录 AI。职业技能 ID 应到该职业技能列表核对，装备和物品 ID 应到各自列表核对。

## 参数项与作用

下列字段的拼写、值形状和位置已经从样本读取。除明确写出代码证据的项目外，游戏作用由标签名和相邻数据推断，尚未经过实机验证。

- `[minimum info]`。角色最小身份信息块。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:3` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 ``<17::ai_character_name_608`15岁的库兰`> 0 0 0 1 17 0 0 11 0 0 0 `no creature` 0 0 0``。到下一个段落标签前共有 16 个制表符分隔值。
  首项是模块 17 名称引用，后续为整数、字符串混合序列。职业、等级、成长类型等位置未完整确认，不能按猜测修改第 N 列。

- `[additional character status]`。附加角色属性数列，作用由名称推断。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:6` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值节选为 `0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0`。到下一个段落标签前共有 37 个制表符分隔值。
  样本为 37 个整数。没有列名，暂不列出固定 HP 或力量列。

- `[character status rate]`。角色属性倍率数列，作用由名称推断。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:10` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值节选为 `1 1 1 1 1 1 1 1.5 1 1.5 1 1 1 1 1 1`。到下一个段落标签前共有 41 个制表符分隔值。
  样本混合整数 1 与浮点 1.5。列映射未知，不能把每一个 1 都替换成 1.5。

- `[quick skill]`。快捷技能配置序列。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:14` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `5 1 46 1 65 6 169 1`。到下一个段落标签前共有 8 个制表符分隔值。
  样本为八个整数，呈技能 ID 与等级交替的形状。应结合职业技能列表确认这些 ID 和等级。

- `[skill]`。角色已配置技能序列。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:18` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `181 2 182 2 184 1 173 1 179 5 177 2`。到下一个段落标签前共有 12 个制表符分隔值。
  样本为十二个整数，呈六组技能 ID 与等级。新增技能还要检查 AI 冷却判断和按键脚本是否会使用。

- `[quick item]`。快捷物品配置序列。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:22` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `6004 99 6001 99 6012 96 6005 97 6007 98`。到下一个段落标签前共有 10 个制表符分隔值。
  原始说明 `output/aicharacter/doc/how to edit key.rtf` 的快捷物品章节明确规定为物品编号与数量配对，与当前样本形状一致。数组顺序对应物品快捷栏，不是技能栏。

- `[equipment]`。AI 角色装备序列。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:26` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值节选为 `27500 2 0 10890 4 0 14881 2 0 12890 2 0 18887 3 0 16880`。到下一个段落标签前共有 45 个制表符分隔值。
  45 个整数呈三元组形状，首列可到装备列表核对。后两列的强化与附加属性等解释未确认。

- `[think term]`。思考周期参数，由名称推断。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:30` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `500`。到下一个段落标签前共有 1 个制表符分隔值。
  单整数 500。时间单位未确认。

- `[keep distance with target]`。与目标保持距离的参数，由名称推断。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:34` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `30`。到下一个段落标签前共有 1 个制表符分隔值。
  单整数 30。不要当作物理米数。

- `[ai pattern]`。角色 AI 文件路径序列。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:50` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `Event.ai` `DestinationSelect.ai` `Action.ai` `MoveMethod.ai` ``。到下一个段落标签前共有 4 个制表符分隔值。
  样本顺序是 Event、DestinationSelect、Action、MoveMethod。应保留各位置职责，不要只凭文件名互换。

- `[key stream]`。角色动作按键流的路径和空位。
  证据为 `output/aicharacter/swordman/15kuran/15kuran.aic:54` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值节选为 ``` `` `triple attack.key` `` `combo.key` `` `a.key` `` `s.key` `` `d.key` `` `f.key` `` `g.key` `` `h.key` ```。到下一个段落标签前共有 36 个制表符分隔值。
  原始 AIC 说明允许省略键名或使用空键名，此时按文件名去掉路径和扩展名生成键名。槽位按声明顺序从 0 编号，Action 与 Event 的返回值会选择该槽位。保留空键名与路径的对应关系。

## 修改步骤

1. 通过 AI 角色列表和职业技能列表定位目标角色及目标技能，不靠显示名称唯一匹配。
2. 优先修改已确认结构的技能等级或单整数命名参数，保留最低身份信息和无列名属性矩阵。
3. 同时核对 AI 的技能条件、按键流和装备引用。回包后实机测试出现、索敌、攻击、物品及死亡处理。

## 未确认与验证

装备三元组后两列的具体字段、最低身份字段布局和属性倍率列尚未解出。角色标签或目录名也不能独立证明最低身份块中的职业枚举。

回包前后应比较实际目标条目的反编译结果。回包成功只证明编码成功，实机检查仍需覆盖本页所述功能。通用编码与回包限制见总索引。

## 原始 APC 说明与可操作规则

以下规则另有原始设计说明支持。来源为 `output/aicharacter/doc/how to edit aic.rtf` 的 Key 设置章节、`output/aicharacter/doc/how to edit key.rtf` 的 input 和快捷物品章节，以及 `output/aicharacter/ai_tool_info.txt`。这些是历史说明，不保证当前客户端保留全部旧功能。

- `[key stream]` 可写名称加路径，也可省略名称。以 `.key` 结尾的字符串被当作文件路径，因此显式名称不能以 `.key` 结尾。只写文件名时，原始说明规定从 AIC 所在目录的 `key` 子目录查找。
- Key 索引从 0 开始。Action.ai 和 Event.ai 的 `[return]` 数字或键名选择相应按键脚本。改 AIC 列表顺序会改变既有 AI 返回值的含义，不能随意排序。
- `[quick item]` 按物品编号、数量配对，按声明顺序分配物品快捷栏。`.key` 中的字符串 `1` 至 `6` 才是使用对应物品栏的按键，AIC Key 索引与物品栏编号不是同一个编号空间。
- `output/aicharacter/swordman/15kuran/key/a.key:3` 的 `[input]` 有四值 `` `a` 30 `time` 100 ``。原始说明明确，按键后的整数是按住的毫秒数，`time` 后的整数是转入下一次 input 的等待毫秒数。该单位证据只适用于这里的 Key 语法，不能扩展为其他格式所有 time 字段。
- `combo attack` 是特殊按键，其后的数值按原始说明表示普通攻击连击次数，不能当作按住时长。`pass` 允许立即前进，`random` 接成功数值与基数，`enemy distance` 使用带符号距离条件；具体语法先对照现有 Key 样本。
- 原始 AIC 说明的 `[party member]` 以成员索引和 APC 索引配对，固定成员从 1 开始，0 是自己，自动成员可用负索引。只有目标文件确实具有这些字段且当前引擎支持时才可据此修改。
- 原始工具说明指出，保存的装备品质值在当时的 AI 创建流程中可能被随机品质替代。因此修改 AIC 装备记录不能直接承诺固定品质生效。
- `output/aicharacter/doc/apc knowhow & attention.rtf` 明确警告 AI 字符串资源的重复键可能导致 APC 创建异常。改名应先查完整键是否重复，而不是只检查显示名不同。

### 编辑一个已有 AI 的快捷技能行为

1. 从职业技能列表确认目标技能已有 ID，核对 AIC 的 quick skill 与 skill 配置。
2. 找到调用该快捷技能的已有 `.key`，确认它已列在 key stream，并记录它当前的零基索引。
3. 在实际 Action 或 Event 条件分支中选择该索引。不要把 DestinationSelect 的移动策略返回号当作 Key 索引。
4. 若调整按键间隔，只改已确认的 input 按住或 time 等待整数，保持过渡条件和空键不变。
5. 回包后检查技能、按键脚本、索引和条件分支，实机观察释放成功、冷却未好、无目标和资源不足时的行为。

# 怪物行为、动作与攻击功能索引

怪物 AI、动作编排、攻击信息和表现资源。

## 功能范围

- 怪物行为及动作配置。
- 攻击判定、动画和粒子资源。

## 分类依据

怪物目录中同时存在 AI、动作、攻击、动画与粒子类型条目，按资源职责归为行为与表现。

## 定位与样本

先读怪物定义中的动作和攻击路径。本文对照了 `output/monster/goblin/bombkagel.mob`、`output/monster/goblin/ai/destinationselect.ai`、`output/monster/goblin/action_goblin/appendage.act` 与 `output/monster/goblin/attackinfo/attack1.atk`。动作、AI、攻击判定使用不同标签大小写，不能混用。

## 参数项与作用

下列字段的拼写、值形状和位置已经从样本读取。除明确写出代码证据的项目外，游戏作用由标签名和相邻数据推断，尚未经过实机验证。

- `[sight]`。视野相关的单整数参数。
  证据为 `output/monster/goblin/bombkagel.mob:35` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `300`。到下一个段落标签前共有 1 个制表符分隔值。
  样本为 300。空间单位及是否还受其他视野规则影响未确认。

- `[warlike]`。攻击倾向相关的单整数参数，由名称推断。
  证据为 `output/monster/goblin/bombkagel.mob:39` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `30`。到下一个段落标签前共有 1 个制表符分隔值。
  样本为 30。没有概率分母，不可直接称为 30% 攻击概率。

- `[attack delay]`。攻击间隔相关的单整数参数，由名称推断。
  证据为 `output/monster/goblin/bombkagel.mob:41` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `2500`。到下一个段落标签前共有 1 个制表符分隔值。
  样本为 2500。时间单位未从引擎确认，不能在手册中直接换算成秒。

- `[attack motion]`。攻击动作资源序列。
  证据为 `output/monster/goblin/bombkagel.mob:75` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `Animation_BombKagel/ThrowAfter1Second.ani` ``。到下一个段落标签前共有 1 个制表符分隔值。
  样本是相对于怪物定义的动画路径，顺序可能被 AI 或动作选择索引使用。替换时必须同步检查引用方。

- `[hp]`。AI 判断中的生命值条件。
  证据为 `output/monster/goblin/ai/destinationselect.ai:17` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `%>=` 45.0 ``。到下一个段落标签前共有 2 个制表符分隔值。
  样本为字符串 `%>=` 和浮点 45.0，原始 APC AI 说明明确将 %>= 定义为当前值相对最大值的百分比比较，因此在采用该解释器时为生命值至少 45%。运算符与浮点类型必须保留。

- `[void]`。调用 AI 内建判断函数及其参数。
  证据为 `output/monster/goblin/ai/destinationselect.ai:23` 的第 1 处同名字段。该字段在样本中出现 4 次。
  原始值为 `` `is target in attack area()` 320.0 320.0 250.0 250.0 ``。到下一个段落标签前共有 5 个制表符分隔值。
  首处调用 is target in attack area() 并有四个浮点数。原始 APC AI 说明将四个参数依次定义为前、后、上、下，不能重排。是否适用于目标怪物所用解释器及具体单位仍需确认。

- `[return]`。AI 条件树的结果编号。
  证据为 `output/monster/goblin/ai/destinationselect.ai:11` 的第 1 处同名字段。该字段在样本中出现 7 次。
  原始值为 `2`。到下一个段落标签前共有 1 个制表符分隔值。
  样本有多处 0、2、10。结果映射属于使用该 AI 的引擎逻辑，不能一概解释为攻击技能 ID。

- `[BASE ANI]`。MOTION 块中的基础动画路径。
  证据为 `output/monster/goblin/action_goblin/appendage.act:5` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `../Animation_Kinol/throw.ani` ``。到下一个段落标签前共有 1 个制表符分隔值。
  相对路径保留大小写与父目录关系，不能用对象索引 ID 替代动画路径。

- `[FRAME]`。TRIGGER 块中触发帧的两个整数。
  证据为 `output/monster/goblin/action_goblin/appendage.act:11` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `2 2`。到下一个段落标签前共有 2 个制表符分隔值。
  样本为 2、2。按名称推断是触发帧条件，区间端点规则未确认，须检查动画帧范围。

- `[APPENDAGE]`。BEHAVIOR 内附加状态的参数及子字段入口。
  证据为 `output/monster/goblin/action_goblin/appendage.act:21` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `5000`。到下一个段落标签前共有 1 个制表符分隔值。
  样本首值为 5000，后续包含 physical attack、attack speed、move speed 与各自的 [%]。5000 的具体单位未确认。

- `[weapon damage apply]`。攻击是否应用武器伤害的开关，按名称推断。
  证据为 `output/monster/goblin/attackinfo/attack1.atk:7` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `1`。到下一个段落标签前共有 1 个制表符分隔值。
  样本为整数 1。不要把该值与攻击倍率混为一谈。

- `[push aside]`。命中后的水平推开参数。
  证据为 `output/monster/goblin/attackinfo/attack1.atk:19` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `100`。到下一个段落标签前共有 1 个制表符分隔值。
  样本为整数 100，空间和速度解释需通过引擎确认。

- `[lift up]`。命中后的浮空参数。
  证据为 `output/monster/goblin/attackinfo/attack1.atk:21` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `300`。到下一个段落标签前共有 1 个制表符分隔值。
  样本为整数 300。它不是已确认的浮空持续毫秒。

## 修改步骤

1. 先画出目标怪物的 `.mob`、AI、动作和攻击文件引用关系。只调整目标怪物实际使用的分支。
2. 修改 AI 阈值时保持 think、true、false 与闭合段完整。修改动作时先核对动画帧，再改 FRAME 条件。
3. 回包后比较条件树和所有路径，实机覆盖条件真与假、近距离与远距离、普通受击与浮空。

## 未确认与验证

帧端点包含关系及动作、怪物时延字段的时间单位仍未确认。AI 解释以实际调用文件类型为准，原始 APC 规则的范围见下一节。

回包前后应比较实际目标条目的反编译结果。回包成功只证明编码成功，实机检查仍需覆盖本页所述功能。通用编码与回包限制见总索引。

## 原始 AI 说明补充

已阅读 `output/aicharacter/doc/how to edit ai.rtf` 与 `output/aicharacter/doc/destination select.rtf`。它们描述 APC AI，不应在未确认解释器一致时强行套到所有旧怪物行为文件。

- `Action.ai` 与 `Event.ai` 的返回值选择 AIC 的 key stream 槽位。`DestinationSelect.ai` 返回移动策略编号。`MoveMethod.ai` 另选移动方式，原始 AI 说明列出浮点 `0.0` 为步行、`1.0` 为冲刺。返回值类型及含义不能跨这四类文件统一。
- 对 DestinationSelect，两个说明共同列出 0 为追踪目标、1 为保持距离、2 为逃离目标、3 为绕目标移动、4 为漫游、10 为迂回追踪。当前哥布林样本的 0、2、10 因此有历史设计解释，但仍要核对该怪物的实际调用方式。
- 两份说明对后续编号有冲突。总 AI 说明把 23 写为保持间距聚集、24 写为躲在被动对象后方；专门目的地说明把 23 写为友军靠近时分散、24 写为保持间距聚集、25 写为躲在被动对象后方。不能对 23 以后的枚举给出无版本条件的固定映射。
- 原始 AI 说明将 `[hp]` 解释为当前生命，`%>=` 是相对最大值的百分比比较，普通 `>=` 则比较绝对值。改阈值前要先确认运算符，45.0 在两种运算符下含义不同。
- `is target in attack area()` 的参数按前、后、上、下排列。`get random()` 把随机结果放到 `[last result]`，原始说明对 0.0、100.0 的例子给出 0 至 99。条件的 `<` 与 `<=` 会改变端点包含关系，不能看到阈值 50 就一律称为 50%。
- `is the skill in cooltime()` 判断给定技能是否处于冷却。先由技能 ID 查职业技能定义，保持该函数和 true、false 分支的对应，不要将 true 误读为技能可释放。
- 目的地说明对 `[set bound]` 明确给出前、后、上、下四个视野边界并注明屏幕像素。该单位证据不自动覆盖 .mob width、速度或其他空间参数。
- `output/monster/mob_module_separation_help.txt` 另列出怪物模块拆分限制，并提醒物品、掉落、任务等服务端相关标签不要随意拆分。本页仅指导已有文件局部修改，不据标签同名推定可以在模块之间搬运。

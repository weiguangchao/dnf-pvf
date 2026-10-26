# 怪物基础参数与难度功能索引

普通、精英、首领、召唤怪物和难度修正参数。

## 功能范围

- 不同怪物类别的基础参数表。
- AI 角色难度奖励与特殊战场参数。

## 分类依据

已观察到 common、named、boss、summon、chaos 和 warroom 对应的基础参数条目，以及 monsterapcdifficultybonus。具体列含义尚未逐项解释。

## 定位与样本

本页逐个读取了怪物根目录的七类基础及修正表。普通、命名、首领和召唤四表均有 4,800 个值，但首领、召唤的数值与普通表不同。这里记录的是观测形状，不是完整表结构。

## 参数项与作用

下列字段的拼写、值形状和位置已经从样本读取。除明确写出代码证据的项目外，游戏作用由标签名和相邻数据推断，尚未经过实机验证。

- `commonmonsterbaseparameter.tbl`。按文件名推断为普通怪物的参数序列。
  `output/monster/commonmonsterbaseparameter.tbl:2` 实测共有 4800 个数值，前 16 项为 `1 5 5 5 5 45 45 11 17 11 17 0 0 0 0 0`。
  该文件没有列名，不能根据这个数量直接确定行宽、等级索引起点、属性顺序或难度列。保留现有整数或浮点写法。

- `namedmonsterbaseparameter.tbl`。按文件名推断为命名或精英怪物的参数序列。
  `output/monster/namedmonsterbaseparameter.tbl:2` 实测共有 4800 个数值，前 16 项为 `1 5 5 5 5 45 45 11 17 11 17 0 0 0 0 0`。
  该文件没有列名，不能根据这个数量直接确定行宽、等级索引起点、属性顺序或难度列。保留现有整数或浮点写法。

- `bossmonsterbaseparameter.tbl`。按文件名推断为首领怪物的参数序列。
  `output/monster/bossmonsterbaseparameter.tbl:2` 实测共有 4800 个数值，前 16 项为 `1 5 5 5 5 240 113 11 17 11 17 0 0 0 0 0`。
  该文件没有列名，不能根据这个数量直接确定行宽、等级索引起点、属性顺序或难度列。保留现有整数或浮点写法。

- `summonmonsterbaseparameter.tbl`。按文件名推断为召唤怪物的参数序列。
  `output/monster/summonmonsterbaseparameter.tbl:2` 实测共有 4800 个数值，前 16 项为 `1 10 10 10 10 229 200 52 92 52 92 0 0 0 0 0`。
  该文件没有列名，不能根据这个数量直接确定行宽、等级索引起点、属性顺序或难度列。保留现有整数或浮点写法。

- `chaosmonsterbaseparameter.tbl`。按文件名推断为混沌类别怪物的参数序列。
  `output/monster/chaosmonsterbaseparameter.tbl:2` 实测共有 33 个数值，前 16 项为 `3000 24 226 24 226 4306 2153 414 3000 414 3000 3001 22 343 22 343`。
  该文件没有列名，不能根据这个数量直接确定行宽、等级索引起点、属性顺序或难度列。保留现有整数或浮点写法。

- `warroommonsterbaseparameter.tbl`。按文件名推断为战场类别怪物的参数序列。
  `output/monster/warroommonsterbaseparameter.tbl:2` 实测共有 120 个数值，前 16 项为 `2000 30 254 30 254 4566 4566 2866 4500 2866 4500 1 1 0 0 0`。
  该文件没有列名，不能根据这个数量直接确定行宽、等级索引起点、属性顺序或难度列。保留现有整数或浮点写法。

- `monsterapcdifficultybonus.tbl`。包含无标签前缀和命名块，不能按一条连续的无标签数列定位。
  `output/monster/monsterapcdifficultybonus.tbl:2` 至文件末尾实测共有 16,842 个数值和 31 个标签。第 2 行的前缀有 169 个数值，前 16 项为 `0.0 10.0 20.0 30.0 30.0 0.0 60.0 150.0 200.0 200.0 0.0 40.0 80.0 120.0 120.0 0.0`。前缀的列义尚未确认。
  `[dungeon party balance]` 位于 `output/monster/monsterapcdifficultybonus.tbl:3`，有 270 个数值，按标签推断涉及地下城组队平衡。
  `[easy]`、`[medium]`、`[hard]`、`[ultimate]`、`[hero]` 依次从第 7、11、15、19、23 行开始，各含 2,800 个数值。按标签推断对应难度修正，但具体列序、行宽和等级索引尚未确认。
  `[mesmerization damage balance]` 从 `output/monster/monsterapcdifficultybonus.tbl:27` 开始。其 `[normal]`、`[named]`、`[boss]` 子块各含 400 个数值，样本形状各为 200 对。列义及伤害修正公式尚未确认。
  `[limit slowdown]` 从 `output/monster/monsterapcdifficultybonus.tbl:43` 开始。其 `[named]`、`[boss]` 子块各含 600 个数值，样本形状各为 200 组三元组。按标签推断为减速限制，三列含义及单位尚未确认。
  `[adjust hp gauge]` 位于 `output/monster/monsterapcdifficultybonus.tbl:55`。该父块内的 `[boss]`、`[named]`、`[normal]` 分别为单浮点 `0.800000011920929`、`0.800000011920929`、`1.0`。按标签推断为 HP 条调整，显示公式尚未确认。这三个字段没有各自的结束标签，父块在第 63 行结束。
  修改重复的 `[normal]`、`[named]`、`[boss]` 前，必须先确定父块。不能全文替换同名字段。保留原数值类型、块边界和记录数量。

- `[ability category]`。单体怪物有显式命名的属性修正入口，可用于缩小修改范围。
  证据为 `output/monster/goblin/bombkagel.mob:11` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `[HP MAX]` `*` 75 `[EQUIPMENT_PHYSICAL_ATTACK]` `*` 80 `[EQUIPMENT_PHYSICAL_DEFENSE]` `*` 80 `[EQUIPMENT_MAGICAL_ATTACK]` `*` 80 `[EQUIPMENT_MAGICAL_DEFENSE]` `*` 80 ``。到下一个段落标签前共有 15 个制表符分隔值。
  只改命名属性的数值仍需核对其倍率解释，不要用不明表列代替该入口。

## 修改步骤

1. 先确定目标是单只怪物还是全局类别参数。单只怪物优先检查其显式命名的 `.mob` 参数。
2. 全局表只在已有引擎列定义或可重复对照实验后修改。先保存完整序列和类型，锁定单个位置进行实验。
3. 回包后比较所有未修改位置，实机分别测试普通、精英、首领、召唤及相应难度，确认影响范围。

## 未确认与验证

当前未解出基础参数表及难度修正块的完整列定义，因此本页不提供 HP、攻击、防御的固定列号。4800 既不等于已知等级上限，也不足以证明任意一种矩阵排布。

回包前后应比较实际目标条目的反编译结果。回包成功只证明编码成功，实机检查仍需覆盖本页所述功能。通用编码与回包限制见总索引。

## 单体怪物属性修改范围

从 `monster/monster.lst` 定位单体 `.mob`，再按 `[ability category]` 中的属性名调整血量、攻击和防御。当前 `output/monster/goblin/bombkagel.mob:12` 的 `[HP MAX]` 系数为 `75`。同类怪物可用于核对结构，数值应按目标怪物分别确定。

只调整一只怪物时，保留属性字符串、运算符和其他属性值，先改该怪物的目标系数。最终血量的完整计算公式尚未确认。不能把系数直接解释为最终 HP，或为了修改单体而连带覆盖全局类别表和难度表。

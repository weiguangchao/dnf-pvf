# 消耗品与投掷道具修改手册

## 入口与样本

先在 `stackable/stackable.lst:2` 用物品 ID 查路径，再编辑对应 `.stk`。本页读取 `stackable/ptn_hplow.stk` 的 50 行、`stackable/ptn_blind.stk` 的 44 行、`stackable/throw/boomerang1.stk` 的 51 行。恢复药、异常恢复药和投掷物的效果载荷不同，不能用一种 `[int data]` 模板覆盖全部物品。

## 药剂参数

- HP 药 `[grade]` 为 `10`、`[minimum level]` 为 `6`，见 `stackable/ptn_hplow.stk:15` 和第 29 行。两者不同。`[usable job]` 为 `[all]`，见第 25 行。
- `[stackable type]` 在 `stackable/ptn_hplow.stk:37` 为字符串 `[waste]` 加整数 `4`。失明恢复剂 `stackable/ptn_blind.stk:31` 相同。枚举决定处理类型，不能翻译 waste。
- `[stack limit]` 在 HP 药第 31 行和失明恢复剂第 25 行均为整数 `1000`。这是堆叠上限形状，不是单次恢复次数。
- `[cool time]` HP 药为 `10000`，`[cooltime group]` 为 `0`，见 `stackable/ptn_hplow.stk:43` 到第 46 行。失明恢复剂同冷却值但组为 `10`，见 `stackable/ptn_blind.stk:37` 到第 40 行。名称提示组共享冷却，实际共享规则与时间单位未确认。
- `[hp recovery]` 在 `stackable/ptn_hplow.stk:49` 为四 token `+ 180 1000 myself`，两个字符串包住两个整数。`+` 支持加法恢复解释，`myself` 指向自身。中间 `1000` 的时间或倍率含义未确认，不能把它说成恢复量或百分比。
- `[active status recovery]` 在 `stackable/ptn_blind.stk:43` 为三 token `blind 65 myself`。名称与 `blind` 确认失明处理类型，整数 65 是等级上限还是强度阈值未确认。不能把三 token 改成 HP 药的四 token。
- `[price]` HP 药与失明恢复剂均为 `200`，分别见 `stackable/ptn_hplow.stk:41` 和 `stackable/ptn_blind.stk:35`。价格与效果量独立。

## 投掷物参数

- `[stackable type]` 在 `stackable/throw/boomerang1.stk:37` 为 `[throw] 2`。`[minimum level]` 第 31 行为 `5`，`[cool time]` 第 41 行为 `2000`。不要把类型后的 2 当投掷数量。
- `[int data]` 在 `stackable/throw/boomerang1.stk:45` 为六整数 `50300 0 0 450 0 100`。首值可能是被动对象引用，需查对象索引确认。本页未确认六列，不能安全用第 10 行说明中的 65 点伤害反推任一列。
- `[string data]` 在 `stackable/throw/boomerang1.stk:49` 只有一个路径字符串 `PassiveObject/ThrowItem/Particle/Boomerang.ptl`。不能增加一个新路径字符串来指向新效果，编译依赖原归档字符串表。
- `[creation rate]` 在 `stackable/throw/boomerang1.stk:19` 为 `900`。没有证据支持这是 900% 或固定掉率，不用于猜测掉落配置。

## 修改步骤

1. 改 HP 药效果时只改 `[hp recovery]` 中已确认的恢复量。保持 `+`、目标和另外一列不变。用实机单次使用核对恢复量，先确认没有其他属性影响。
2. 改异常药时先确认状态枚举与 65 的语义。未知阈值不改。改冷却时检查本物品的 group 和其他同组物品，避免只看单件表现。
3. 投掷伤害需要继续追踪对象和粒子调用，未解释 `[int data]` 前不能安全改六列。说明文本不等于执行参数。
4. 保留 CRLF、TAB、`#PVF_File\r\n` 与 token 类型。改中文需改 `stackable/stackable.kor.str` 原有键，内联显示文字不进入编译。本文空格不是源文件分隔。
5. 核对四 token、三 token、六整数及路径数量。需要真实重建与提取，客户端分别测试恢复、状态解除、共享冷却和投掷命中。`--verify` 只验证原归档。

## 未知项

药剂第二整数、异常等级阈值、投掷对象引用和时间单位尚未确认。文件名含 potion 或 throw 不是效果公式的证据。

# 活动条件、通知与奖励修改手册

本页用于维护条件奖励映射、通知文本和职业奖励编目。维护者应分清活动 ID、条件 ID、物品 ID 和通知开关。

## 入口

已读 `event/conditionevent.evt`、`event/conditioneventchkdungeon.evt`、`event/eventnotice.evt`、`event/eventreward/reward.evt`、`event/eventreward/reward_swordman.evt` 和 `event/exchangerandomitemreward.evt`。这些文件使用不同顶层结构。

## 条件与通知参数

- `[id]` 在 `event/conditionevent.evt:3` 后为 2。condition match 第 5 至 7 行含 30 个整数，十组三整数 `1 1 0` 至 `10 10 0`。观察到两列相同和末列 0，不能凭 match 一词确定 AND/OR 规则。
- condition reward 第 9 至 11 行含 50 个整数，十组五整数。首组 `1 690000433 3 0 0`，第 3 组 `3 24 3 0 0`，末组 `10 900 1 0 0`。首列与 condition match 第一列 1 至 10 对齐，次列物品与第三列数量是推断，末两列未知。
- apply level 在 `event/conditioneventchkdungeon.evt:3` 后为 1。unable dungeon 第 5 至 7 行有 120 个整数，开头 `100 11000 11001 11006 11007 62 63 64 65 66 67`。标签支持排除地下城解释，首整数 100 也可能是 ID，不能当列表长度删除。当前实际 token 数为 120。
- 通知 on 块第 3 至 9 行有两个独立 event id `454`、`455`。off 从第 11 行起含多个 event id，部分重复，见 `event/eventnotice.evt:3` 至第 60 行。不能把重复通知编号当成无用数据自动去重。
- 通知 item 块 `event/eventnotice.evt:299` 至第 312 行的 id 为 15，start、ing、end 各一条模块 23 引用 `event_id_15_start`、`event_id_15_ing`、`event_id_15_end`。它们是三种状态的文案，不是活动起止时间。第 314 行起 id 16 是另一块。

## 职业奖励与随机兑换

- `event/eventreward/reward.evt:2` 是十对整数与相对路径的索引，0 对应 `reward_swordman.evt`，99 对应公共职业文件。不是一条有二十列的奖励记录。
- `event/eventreward/reward_swordman.evt:3` 至第 85 行外层 reward。首个 job type 第 5 至 23 行为字符串 `swordman` 与整数 `1 0`。后三个 job type 分别用 `2 0`、`3 0`、`4 0`。两个整数推断为成长类型与其他条件，具体域未知。
- 首个 sub type 为两个字符串 `common equip`。其中 option 为 `upgrade 10`，其内部 equipment item 为 `0 101040047`，见第 7 至 15 行。标签支持强化 10 的解释，首整数 0 含义未确认。
- 同一 sub type 内、option 之外还有第二个 equipment item，五对 `0 2280104 0 2281104 0 2282104 0 2283104 0 2284104`，见第 17 至 19 行。它与 option 内单件装备的上下文不同。不能一次替换所有 equipment item 块。
- 随机兑换外层 event 的 material 内有 exchange rule `0 690000643 1`，见 `event/exchangerandomitemreward.evt:11` 至第 15 行。三列的规则、物品与数量用途属推断。
- random reward item 第 17 至 19 行只有整数 8287，可能引用随机盒或奖励定义，不是概率与物品二元组。send mail 内 inven 为 1，detail 为四个 0 和消息键 `tw_event_full_title`、`tw_event_full_text`，见第 21 至 29 行。

## 修改步骤与未知项

改条件奖励时锁定活动 id 2 内的条件键，保持五整数记录及两末字段。排除地下城先查 dungeon 索引，保留所有原值的 token 位置。通知改文案只改模块 23 对应 key，不把 on/off 当成服务端奖励开关。

职业奖励替换先锁定 job type、sub type 和是否在 option 内。随机兑换需继续查 8287 的实际物品定义，不能把它替换成一组自创奖励表。

运行检查目标条件计数、排除副本、通知三阶段、职业分支和背包满时邮件。条件枚举、两个零字段、服务端活动开启源和随机权重均未由样本完整证明。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

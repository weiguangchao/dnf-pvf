# 决斗任务修改手册

本页用于修改决斗任务资格、晋级条件和任务链。维护者须使用 mission ID，不把 kind 或文件序号当链编号。

## 入口

`pvp_mission/mission.lst:2` 的 101 指向 `daily/daily_mission001.msn`，110 指向 `rankup/rankup_mission001.msn`。已读两份样本，分别为 26 与 29 行。general、pop、repeatable 任务需先确认自己的 condition 枚举。

## 参数与证据

- `[kind]` 在 `pvp_mission/rankup/rankup_mission001.msn:3` 后为 27。daily 样本为 18。完整 kind 枚举未知，不能根据目录自动生成。
- `[grade]` 是 `[rank up]`，daily 为 `[daily]`，见两份样本第 5 行。rank up 的空格必须保留。
- `[rank range]` 为 `9 10`，`[rate range]` 为 `0 101`，见晋级样本第 7 至 10 行。rank 的整数映射及 rate 是否百分制未知。文本"晋升为1段"不能证明 rank 9 就是一段。
- `[prev mission]` 为 -1，`[next mission]` 为 56，见 `pvp_mission/rankup/rankup_mission001.msn:11` 至第 14 行。应从 mission.lst 查 56，不按 filename 001 加一。daily 的 prev、next 均为 -1。
- `[name_text]`、`[cond_text]` 各一条模块 21 引用，晋级为 `110_name` 与 `110_cond`，见第 15 至 19 行。条件文字明确"接下来的5战当中，达成2胜以上"。
- 晋级 `[condition]` 第 21 至 23 行有枚举 `[within]` 与三个整数 `-1 5 2`。文本支持 5 战和 2 胜解释，首整数 -1 的模式范围未知。
- daily condition 为 `[hereafter join] 1 1 -1`，见 `pvp_mission/daily/daily_mission001.msn:21`。文本要求个人战一场。两个 1 分别指模式还是次数需更多枚举证据，不能套 within 的列映射。
- `[difficulty_ratio]` 是整数 1，见晋级样本第 25 行与 daily 第 25 行。未证实它是倍率、权重还是难度等级，保留原类型。
- `[reward item]` 晋级第 27 至 29 行为 `2601139 1`。推断物品与数量二元组。daily 样本没有此标签，不应为了格式统一补空块。

## 修改步骤与未知项

修改晋级胜场先锁定 within 条件，再改 5 或 2 并同步模块 21 文本。修改链时双向检查 prev、next 是否指向已有 mission ID。改奖励前查物品定义，保持二元组。

运行核对资格边界、计数开始时点、五战失败后的状态、晋级发奖与后续任务。rank/rate 的边界包含性、kind 和模式枚举、daily 重置时点都未由样本证明。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

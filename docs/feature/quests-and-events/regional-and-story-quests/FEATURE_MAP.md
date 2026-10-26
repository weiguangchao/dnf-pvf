# 地区任务与剧情编目修改手册

本页用于修改地区剧情任务条件、奖励和章节归属。维护者可沿任务 ID 和显式前置块核对任务链。

## 定位与样本

`n_quest/quest.lst:2` 的 111 对应 `Handonmyre/GrakKarak/epic_10_GrakKarak_shauta_3.qst`。实际导出样本 `n_quest/handonmyre/grakkarak/epic_10_grakkarak_shauta_3.qst` 共 94 行。章节另在 `n_quest/epicquest.lst`，公共奖励参数另在 `n_quest/questparameter.etc`。

## 任务参数与证据

- `[grade]` 是枚举 `[epic]`，`[difficulty]` 是字符串 `W`，`[gold multiple]` 为整数 `150`，见 `n_quest/handonmyre/grakkarak/epic_10_grakkarak_shauta_3.qst:3` 至第 8 行。difficulty 不是地下城 easy 枚举。`n_quest/questparameter.etc:4` 将 `W` 配为 300，计算公式尚未确认。
- `[npc index]` 与 `[complete npc index]` 都为 7，见任务第 9 至 12 行。需到 `npc/npc.lst` 查 NPC，不能把 7 当任务 ID。
- `[job]` 为 `[all]`，`[grow type]` 为 `-1`，`[level]` 为 `10 99`，见第 13 至 18 行。等级区间解释有标签证据，-1 的精确逻辑未实测。
- 十个 `[pre required quest]` 是十个独立闭合块，分别含 `505 515 7645 525 535 1805 545 623 635 4474`，见第 19 至 57 行。不能改成一行十整数并宣称等价。多个块的 AND/OR 关系未知。
- `[quest point]` 是 4。`[type]` 为 `[hunt monster]`，`[sub type]` 为 -1，`[int data]` 为四整数 `7 -1 15 1`，见第 59 至 67 行。条件文本第 86 行要求击败格拉卡的牛头王萨乌塔。地下城 7、怪物 15、数量 1 的对应属推断，第二列 -1 未证实。
- `[reward type]` 为 `[item]`，固定奖励块为六整数 `0 600 22006 1 18407 1`，见第 69 至 73 行。观察到三对，但首对 0 600 的特殊意义未知，不可把 0 当普通物品直接删除。
- `[reward selection int data]` 第 75 至 77 行为空，与固定奖励不同。`[dialog]` 第 91 至 94 行含七整数 `1 0 7 2 1 15 0` 加文本引用，不采用 NPC dialog 的六整数形状。

## 章节与公共数值

- `n_quest/epicquest.lst:3` 至第 15 行是一个 episode 块。episode 数据为 `1 5`，episode_name 为模块 18 的 `ep_name_1`。epic_index 有十个 ID `101 102 103 4301 104 105 106 107 108 4302`。两整数 episode 的第二列用途未知。
- `n_quest/questparameter.etc:7` 的 piece reward table 为三对 `1 6 2 12 3 18`。随后 piece reward 1 内 physical attack 是字符串 `+` 与整数 100，attack speed 是字符串 `%` 与整数 2，见第 11 至 27 行。百分号有实际 token 证据，不能推广到其他 rate 字段。
- 公共 exp reward table 与 gold reward table 各有 200 个整数，见 `n_quest/questparameter.etc:71` 至第 74 行。数组索引如何对应等级与难度未证实，不能局部插入一格导致后续错位。

## 修改步骤与未知项

先定位任务 ID 和章节位置，再选择条件类型。只改猎杀数量时保留四整数形状并同步核对条件 .str。改奖励时分别核对固定与可选块，保留特殊 ID 0。改前置先逐条查任务索引，不按文件名推导 ID。

运行检查接取、目标击杀计数、交付、固定奖励与章节推进。公共奖励公式和多前置逻辑仍未知。不要只改显示文本就认定任务规则已变。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

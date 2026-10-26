# 转职、觉醒与副职业任务修改手册

本页用于修改转职链、觉醒材料和副职业任务。维护者需要区分普通 job、epicjob 和 expertjob 的职业条件。

## 定位

样本为 `n_quest/job/atf_grappler_01.qst`、`n_quest/epicjob/achievement_50_epicjob_1000hand_1.qst` 与 `n_quest/expertjob/lv2_archemist_01.qst`。使用 `n_quest/quest.lst:2` 查实际任务 ID。该索引中 7628 指向觉醒样本，173 指向副职业样本。部分导出 qst 未确认存在索引入口，不能靠文件新增任务。

## 转职样本

- `[grade]` 为 `[common unique]`，difficulty 为 `M`，gold multiple 为 10，见 `n_quest/job/atf_grappler_01.qst:3` 至第 8 行。转职不是由 grade 单独标明。
- `[job change quest] 1` 与 `[grow number] 3` 见第 9 至 12 行。后者推断是目标转职编号，缺少枚举定义，不可按职业显示顺序猜编号。
- `[npc index] 6` 与 `[complete npc index] -1` 见第 13 至 16 行。exposed by npc、first exposed by npc 各为 1，见第 17 至 20 行。-1 是实际哨兵，不能补成 NPC 0。
- `[job]` 为 `[at fighter]`，grow type 为 -1，level 为 `20 99`，见第 21 至 26 行。职业字符串必须保留空格。
- `[collision quest]` 第 27 至 29 行含三个 ID `7887 7890 7893`。条件文本第 58 行明确提示完成后不能接受其他转职任务，支持互斥关系，但完整互斥时点需运行确认。
- `[type] [seeking]` 对应十整数 int data `3037 30 3034 10 3035 10 3036 10 3033 10`，见第 31 至 37 行。条件文本明确需要无色 30 与白、红、蓝、黑各 10，支持五组物品与数量配对。
- 固定奖励为 `4054 1`，可选奖励为空，relation quest 为 `7897`，见第 39 至 50 行。关系字段只有一个整数，不是闭合块。后续任务引用需回查索引。

## 觉醒与副职业差异

- 觉醒 `[job change quest]` 为 `2`，job 仍为 `[at fighter]`，grow type 为 3，level 为 `50 99`，见 `n_quest/epicjob/achievement_50_epicjob_1000hand_1.qst:11` 至第 22 行。不能把转职样本的 grow number 搬来替换 grow type。
- 觉醒 seeking int data 有四对 `3039 10 3040 10 3155 100 3150 100`。固定奖励是 `1089 20 1090 20 0 100`，relation quest 为 7629，见第 27 至 42 行。ID 0 的奖励含义未知。
- 副职业 `[expertjob level]` 为 `2 2`，`[level]` 为 `1 99`，见 `n_quest/expertjob/lv2_archemist_01.qst:11` 至第 16 行。前两个整数推断是副职业类型与等级或等级范围，不能断言两列都是角色等级。
- 副职业 grade 为 `[daily]`，seeking int data 为 `3037 20`，固定奖励为空，可选奖励有六对 `2610001 20` 至 `2610006 20`，见第 21 至 33 行。文本第 42 行确认交 20 个无色小晶块。

## 修改步骤与未知项

先选链中的具体一环，记录 relation quest、collision quest 和现有职业条件。改材料时按物品数量二元组修改并核对文本。不要把六个可选奖励改为固定奖励，除非需求明确且经过实际交付验证。

转职和觉醒完成后还要核对职业状态、技能可用性与互斥链。副职业需核对资格、每日重复及奖励选择。job change quest、grow number、expertjob level 的完整枚举与重置范围尚未证明。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

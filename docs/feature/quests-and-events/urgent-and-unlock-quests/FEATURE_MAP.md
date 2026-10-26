# 紧急、深渊与特殊解锁任务修改手册

本页用于修改紧急通关条件和特殊地区解锁任务。维护者应按 reward type 区分物品奖励与解锁操作。

## 入口

`n_quest/quest.lst:2` 的 270 对应 `urgent/1stBackbone_0_1.qst`，2603 对应 `Hell/achievement_47_Hell_wild_1.qst`。已读这两份 qst 和 `n_quest/requiem/opengate_1.qst`。title、towers 等目录只是进一步检索入口，不能由目录名认定奖励 schema。

## 紧急任务参数

- `[grade]` 是 `[urgent]`，difficulty 为 `U`，gold multiple 为 10，见 `n_quest/urgent/1stbackbone_0_1.qst:3` 至第 8 行。
- npc index 为 73，complete npc index 为 -1，job 为 `[all]`，grow type 为 -1，level 为 `32 35`，见第 9 至 18 行。负数是哨兵，精确回退逻辑未证实。
- `[pre required quest]` 第 19 至 21 行含 4000，需查任务索引。它不等于 int data 的地下城候选编号。
- type 为 `[condition under clear]`，sub type 为 6，int data 为 `25 0`，见第 23 至 29 行。条件文本仅说通关下列地下城。推断 25 是地下城候选，第二列和 subtype 6 的完整枚举未知。
- reward type 为 `[item]`，reward int data 是 `0 1`，可选块为空，见第 31 至 39 行。不能将 0 改为普通奖励 ID 而忽视特殊逻辑。

## 深渊任务与镇魂入口

- `n_quest/hell/achievement_47_hell_wild_1.qst:3` 的 grade 为 `[achievement]`。ignore quest level 4 exp 为 1，npc index 为 45，level 为 `47 99`，见第 5、11、19 行。
- 该深渊任务 type 为 `[hunt enemy]`，sub type 为 -1，int data 有五整数 `44 2 61704 1 1`，见第 23 至 29 行。条件文本第 50 行要求王者级冰雪宫殿领主。文件不能证明这五列与 `[hunt monster]` 四列相同。
- `[reward type]` 明确为 `[hell challenge]`，reward int data 只有 `1`，见第 31 至 35 行。这是解锁候选参数，不是物品数量二元组。relation quest 为 2606，见第 41 行。
- 世界图 `worldmap/lorien.wdm:16` 的 hell quest 是 2610。它与本样本 2603 不同，说明不能把所有深渊任务统一绑定同一个 worldmap。需按目标地区核对。
- `n_quest/requiem/opengate_1.qst:9` 至第 14 行的 npc index 为 127，complete npc index 为 -1，hide npc on clear 为 127。条件文本第 48 行明确说明完成后 NPC 梅米特消失，支持该隐藏字段解释。
- 镇魂 level 为 `81 99`，type 为 `[seeking]`，int data 为 `3263 10`，见第 19 至 29 行。固定 item 奖励是 `0 200`，见第 31 至 35 行。地区开启方式仍需查城镇、NPC 角色和服务器条件，不能把 0 200 断言为解锁编号。

## 修改步骤与未知项

先确定是 urgent 条件、hell challenge 奖励还是镇魂剧情入口。替换地下城之前对照条件类型及对应文本。改深渊奖励保留单整数形状，不能套物品二元组。改镇魂材料时保留 hide npc on clear，除非需求明确改变 NPC 生命周期。

回归检查前置完成、接取范围、通关计数、深渊入口及 NPC 消失。奖励 0 的含义、紧急 subtype 6、hunt enemy 五列和地区开启链尚未完整确认。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

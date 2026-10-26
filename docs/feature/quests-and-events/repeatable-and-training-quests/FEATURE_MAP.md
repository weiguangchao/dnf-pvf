# 日常、重复与教学任务修改手册

本页用于维护重复收集、training 任务候选表和任务点数商店。training 的实际样本文本是材料考验，不应仅按英文名断言新手教学。

## 入口

`n_quest/quest.lst:2` 的 7319 对应 `common/Gent/training_58_Gent_cartel_insignia.qst`，5950 对应 `common/Gent/repeat_62_Gent_collection.qst`。另读 `n_quest/trainingquest.lst`、`n_quest/dailyrandomquest.lst` 和 `etc/questshop.etc`。

## 任务参数

- training 样本 grade 为 `[training]`，difficulty 为 `D`，gold multiple 为 200，见 `n_quest/common/gent/training_58_gent_cartel_insignia.qst:3` 至第 8 行。npc index 为 57，complete npc index 为 -1，level 为 `58 99`。
- training 的 type 为 `[seeking]`，int data 为 `3249 3`，见第 19 至 25 行。条件文本第 44 行明确收集三个卡勒特干部徽章，支持物品与数量解释。固定奖励 `3300 7 4420 1` 是两对，选择奖励为空，见第 27 至 35 行。
- repeat 样本 grade 实际为 `[normaly repeat]`，见 `n_quest/common/gent/repeat_62_gent_collection.qst:3`。拼写 normaly 不可修正。level 为 `62 99`，前置闭合块含 5777，见第 13 至 17 行。
- repeat 的 seeking int data 为 `3267 3`，dungeon info 为三对 `83 -1 84 -1 85 -1`，见第 23 至 29 行。条件文本列三座地下城。第一列为地下城引用是推断，第二列 -1 的难度或通配语义未知。
- repeat 固定奖励 `0 1` 具有特殊 ID 0，可选奖励有六对 `7754 1` 至 `7759 1`，见第 31 至 39 行。不能当作七个必给物品。

## 候选编目与点数商店

- `n_quest/dailyrandomquest.lst:3` 至第 5 行只有空 group。当前样本没有日常随机组参数可编辑，不应编造每日任务条目。
- `[select prob]` 在 `n_quest/trainingquest.lst:3` 至第 5 行为十一整数 `6 -100 0 -3 10 -2 15 -1 25 0 50`。可观察一个前缀与五对，前缀 6 是否计数未证实。不能将所有整数都当权重。
- `[rand value]` 在第 7 至 9 行含 2196 个整数，开头 `41 67 34 0 69 24`。用途和周期未知，不能随机重新生成。
- 同名 `[level]` 块必须按首整数定位。`n_quest/trainingquest.lst:239` 至第 241 行的数据为 `58 7310 7311 7312 7313 7314 7315 7316 7317 7319 7320 7322 7323 7324 4270 4271 4272 4273`，首值是等级候选，后十七个是任务候选 ID。第 291 至 293 行首值为 -100，保留特殊段。
- `etc/questshop.etc:3` 至第 24 行是 quest status 0。name 为"强化 - 力量"，icon 是 `Common/Etc/QPskill.img 1`，quest status info 为 `[physical attack] + 15.0`。中文说明是力量 +15，标签和自然语言不应强行当成同一个战斗公式。
- 该状态的 level info 有十五对，开头 `15 3 20 1`，末尾 `85 2`，quest point 为 20，见 `etc/questshop.etc:18` 至第 23 行。第二列与等级的关系尚未确认。其他 quest status 的同名字段必须在各自闭合块内修改。

## 修改步骤与未知项

改收集量时同步核对 int data 与 .str。替换 training 候选时先在 quest.lst 验证 ID，再仅改目标 level 块的一个候选，保留首整数。不要删除空等级块或 -100 特殊组。

回归检查可接等级、重复接取、奖励选择及点数扣除。每日重置和候选概率算法未知。training 不能自动等同于教程，questshop 也不是普通 NPC 商品表。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

## 任务条件与奖励匹配

任务 grade、完成条件 type、固定奖励和选择奖励分别定位，`[int data]` 随 type 解释。当前 training 样本的 `[seeking]` 接 `3249 3`，且条件文本要求三个徽章，支持该样本的物品与数量解释。

替换收集目标时先查物品索引，再核对任务文本和奖励块。不能把 `[seeking]` 的二元组套到击杀或通关任务。保留当前任务的 grade 和实际类型字符串，只改需求指定的条件或奖励。

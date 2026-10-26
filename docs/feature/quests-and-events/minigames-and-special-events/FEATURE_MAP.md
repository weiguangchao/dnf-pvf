# 小游戏与专题活动修改手册

本页用于调整棋盘、宾果、双队挑战与竞速的既有配置。维护者应按各玩法的实际记录形状维护，不能共用 reward 元组解释。

## 入口

棋盘读 `event/bluemarble/bluemarble.blu`、`event/bluemarble/bluemarblemap.lst` 和 `event/bluemarble/bluemarbletile.lst`。其他样本为 `event/bingoevent.evt`、`event/dualraid/dualraid.info` 和 `event/racingdungeon/racingdungeon.info`。eventcharacter、eventserver 的生效规则未由本页样本证明。

## 棋盘与宾果参数

- 棋盘 player max 为 3，enter level 为 41，enter max level 为 70，enter count 为 10，die count 为 3，见 `event/bluemarble/bluemarble.blu:3` 至第 12 行。次数重置周期未知。
- `[dice value]` 为 `1 6`，dungeon difficulty 为 2，difficulty list 为五对 `3028 1 3042 1 3043 1 3044 1 3045 1`，见第 13 至 19 行。推断首两整数为骰点范围，难度 2 的枚举映射未知。
- super armor time 为 5，buff max value 为 8，equipment upgrade max 为 10，见第 21 至 26 行。时间单位未确认。gold base 与 gold multi 为浮点 `0.10000000149011612`、`0.30000001192092896`，不能当固定金币数。
- reward item 为三对 `8354 3 8354 2 8354 1`，见 `event/bluemarble/bluemarble.blu:31` 至第 33 行。实际闭合标签是 `[/reawrd item]`。boss dungeon list 的闭合实际为 `[/boos dungeon list]`，见第 39 至 41 行。保持原始拼写。
- dungeon list 第 36 行为 126 个整数，呈 42 组三整数，开头 `41 41 3001`。boss 为 93 个整数，unique 为 90 个整数。前两列推断等级边界，第三列疑似地下城 ID，需查 dungeon 索引。
- tile pos 第 52 行有 64 个整数，可分 32 对坐标候选。`event/bluemarble/map/1.bm:4` 有 64 个整数，可分 32 对，开头 `1 1 6 1 3 3046`。第二列既有 3046 也有 -2、-3，不能统一解释为数量。
- `event/bluemarble/bluemarbletile.lst:2` 的 7 指向 `Tile/boss_unique.bt`。该文件 type 为字符串 `boss unique`，enter dungeon 为 1，见 `event/bluemarble/tile/boss_unique.bt:3` 至第 6 行。
- 宾果 use item 是五整数 `690000377` 至 `690000381`，reward 为七整数 `2 1 1 1 3 690000382 1`，见 `event/bingoevent.evt:3` 至第 9 行。board 有 807 个整数，quiz value 有 63 个整数，开头 `31 1 84 2 63`，见第 11 至 17 行。未确认头计数和布局，不可安全重排。

## 双队与竞速参数

- dualraid normal dungeon 为 3049，boss dungeon 为 3050，team count 为 2，user count 为 3，required fatigue 为 10，见 `event/dualraid/dualraid.info:3` 至第 16 行。user count 是每队还是总人数未证实。
- clear bonus rate 为 120，fail bonus rate 为 80，kill rank 有三整数 `120 110 100`，见第 21 至 27 行。未确认百分比单位。clear reward item 为 `10000373 3`，fail 为 `10000373 1`，见第 29 至 32 行。
- basic reward exp 第 34 行为 52 个整数，26 对，开头 `60 136000 61 146513`。enter minimum level 为 60，`[nomral dungeon difficulty]` 实际拼写 nomral，值为 2，见第 37 至 44 行。kill monster exp rate 为三组三数 `60 65 0.800000011920929`、`66 75 1.0`、`76 85 1.149999976158142`，见第 45 至 47 行。
- racing 的 start condition member count 为 3，upper level 为 85，lower 为 10，见 `event/racingdungeon/racingdungeon.info:3` 至第 8 行。reward item index 为四个 10000374，reward item count 为 `5 3 2 1`，见第 9 至 12 行。四档是否名次顺序未实测。
- racing require fatigue 为 4。recommand channel 为 78 个整数，开头 `98 1 99 1 99 11`，见第 13 至 17 行。保留 recommand 拼写，频道编码和元组宽度未知。

## 修改步骤与未知项

替换棋盘一个格子时先用 tile 索引解释类型，再判断该类型的第二整数域。改竞速奖励同时保留两数组四项的对齐。改 dualraid 奖励分别核对成功与失败，不把 rate 当道具数量。

运行检查人数条件、疲劳扣除、棋盘落点与奖励档位。宾果大数组、频道编码和专题活动启动条件没有足够证据，不能安全按猜测重写。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

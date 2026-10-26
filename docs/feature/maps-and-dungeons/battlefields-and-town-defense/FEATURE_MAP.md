# 战场、决斗场与城镇防御修改手册

本页用于维护刷怪战场、城镇防御和决斗城镇入口。维护者可从实际字段区分三套规则，避免按目录名共用元组解释。

## 入口与样本

`dungeon/dungeon.lst:2` 的 2000 对应 `WarRoom/Grenselos20-30.dgn`。已读 `dungeon/warroom/grenselos20-30.dgn`、`dungeon/villageattack/hendon_city_easy.dgn`、`town/fair_pvp.twn` 和 `town/warfare.twn`。twin_raid 的玩法细节不由这些样本推断。

## 战场参数

- `[minimum required level] 20` 与 `[basis level] 30` 见 `dungeon/warroom/grenselos20-30.dgn:13` 至第 16 行。文件名 20-30 不是运行时上下限证据，未见最大等级字段。
- maze 为 size `1 1`、greed `AA`，map specification 为 `0 0 45000`。见 `dungeon/warroom/grenselos20-30.dgn:23` 至第 31 行。start 与 boss 是空块。`[warroom map index] 45000` 在第 45 行。`map/map.lst:2` 将 45000 映射到 `Grenselos/Grenselos20-30.map`。
- `[monster type spawn prob]` 第 47 至 49 行有 28 个整数，七次重复 `70 17 10 3`。每组和 100 是实测，概率百分制及四类顺序尚未确认。
- `[monster type spawn cost]` 后有四整数 `10 20 40 50`，见 `dungeon/warroom/grenselos20-30.dgn:51`。四类的索引顺序需结合客户端确认。
- 四种 spawn index 块分别含 common monster 的 `40001` 至 `40004`、common champion 的 `41001` 至 `41005`、super champion 的 `42001` 至 `42004`、boss 的 `43001` 至 `43003`，见第 53 至 67 行。应查怪物索引确认 ID，不能把数字当数量。
- `[spawn step max] 7` 与七整数 `[spawn step resource pool] 200 350 450 550 600 650 700` 见第 69 至 73 行。组数吻合是观察，资源恢复机制未知。
- `[monster type spawn interval rate]` 是四浮点 `1.0 1.5 2.0 2.5`。base interval 与 random interval 均为整数 `2000`，见第 75 至 80 行。时间单位未确认，不能写成两秒。
- `[max monster] 30`、`[kill count const] 0.00033000000985339284`、`[join cost gold] 20000` 见第 81 至 86 行。gold 为标签明确币种，kill count 的计算公式未知。

## 防御与决斗入口参数

- `dungeon/villageattack/hendon_city_easy.dgn:13` 的最低等级为 1，basis level 为 60，经验浮点为 `0.6399999856948853`。maze 为 `1 1`、`AA`，boss map 为 `-1 -1`，见第 23 至 35 行。负数是原始状态，不应改成 0 0。
- `town/fair_pvp.twn:7` 的 `[only server parsing dungeon what must be cleared]` 为 `2`，与第 5 行普通前置 `-1` 并存。标签说明服务器专用条件，但是否 dungeon ID 仍须查索引与实测。
- 决斗 area 0 使用 `Fair_PVP/Gate_Hendon.map`、矩形 `258 149 271 157`、枚举 `[gate]` 与尾整数 `474 234`。area 1 使用 `Fair_PVP/Hendon_Pub.map`、矩形 `320 167 358 187` 和 `[normal]`，见 `town/fair_pvp.twn:11` 至第 17 行。
- `town/warfare.twn:10` 的 area 0 为 `[safe zone against b]`，第 26 行 area 4 为 `[safe zone against a]`。区域编号与路径 Warfare05、Warfare04 的次序并不相同。`[limit level]` 为 50，见第 36 行。

## 修改步骤与未知项

战场改强度先限定一个 step 或一类 spawn，保留七组资源与四类参数的各自数量。替换 map index 时核对 map specification 与 warroom map index 是否一致。

防御关卡保留无 boss 的哨兵状态。调整安全区须锁定 area 编号和阵营枚举。运行检查进入条件、怪物上限、阶段推进与阵营安全区。文件没有证明服务器活动开启条件、重置规则或刷怪间隔单位。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

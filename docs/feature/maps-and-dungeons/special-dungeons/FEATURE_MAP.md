# 特殊副本与教学关卡修改手册

本页用于修改异界与教学等具有专用字段的地下城。目录名只提供检索线索，运行规则以实际脚本为准。

## 入口与已读样本

`dungeon/dungeon.lst:2` 中 62 对应 `Impossible/GoblinKingdom.dgn`，3506 对应 `GlobalTutorial/GlobalTutorial.dgn`。样本分别为 `dungeon/impossible/goblinkingdom.dgn` 的 83 行与 `dungeon/globaltutorial/globaltutorial.dgn` 的 61 行。ancient、timegate、anton、quest、riskdungeon 等目录需逐文件再分析，不沿用此页全部列义。

## 异界样本参数

- `[minimum required level] 70` 与 `[basis level] 70` 见 `dungeon/impossible/goblinkingdom.dgn:13` 至第 16 行。`[experience increasing point] 1.5` 是浮点，倍率用途属推断。
- `[prohibit practice]` 后为 `1`，见 `dungeon/impossible/goblinkingdom.dgn:21`。标签支持禁止练习模式解释。`[coin limit]` 第 25 行后为 `12`，重置范围未知。
- `[dimension dungeon]` 是两个整数 `1 5`，见 `dungeon/impossible/goblinkingdom.dgn:27`。`[necessary party]` 为一个整数 `1`。不能把 1、5 都写成人数。
- `[evil]` 与 `[evil high level]` 各五整数 `10 40 90 110 110`，`[evil rate]` 为四整数 `30 30 110 120`，见第 31 至 36 行。疑似抗魔相关，但样本不足以证明各难度位置与百分比单位。
- `[monster difficulty bonus]` 第 37 至 39 行含 65 个数值，其中有 `1.100000023841858` 和 `15 4 2.5 2 1`。不能按物理行解释怪物类别，也不能把所有值当整数。
- `[maze info]` 内 `[size] 6 1` 与 ``[greed] `BBFFFFFFFFEE` `` 见第 41 至 46 行。start 为 `0 0`，boss 为 `5 0`。五个 map specification 分别是 `1 0 16101` 至 `5 0 16105`，见第 55 至 73 行。map 0 的指定并未出现，不应擅自补齐。
- `[coin info]` 第 75 至 77 行为四组枚举加二整数，开头 `[easy] -1 0`，其余 `[medium] 8 1`、`[hard] 8 1`、`[ultimate] 8 1`。保留字符串枚举与负数语义未知值。

## 教学样本参数

- `[prohibit practice] 0`、`[minimum required level] 1`、`[basis level] 1` 见 `dungeon/globaltutorial/globaltutorial.dgn:3`、第 15、17 行。与异界取值不同，不证明教学由这三个字段单独启用。
- 教学 maze 的 size 为 `3 1`，greed 为 `BBFFEE`，start 为 `0 0`，boss 为 `2 0`，见 `dungeon/globaltutorial/globaltutorial.dgn:23` 至第 35 行。
- 三个 `[map specification]` 第 37、41、45 行分别为 `0 0 25205`、`1 0 25206`、`2 0 25207`。`map/map.lst:2` 的 25205 对应 `GlobalTutorial/01N.map`，这是明确地图引用证据。
- `[designate dungeon difficulty] 0`、空的 `[special passive object item]` 和浮点经验字段 `0.10000000149011612` 见 `dungeon/globaltutorial/globaltutorial.dgn:49` 至第 56 行。空块应保持。

## 修改步骤与未知项

地图替换优先修改现有 map specification 的第三整数，保留前两坐标及 maze 尺寸。限制修改先记录当前 difficulty 和 coin info 的关系，在实际难度入口分别验证。

本页没有证明 dimension dungeon、evil 或 monster difficulty bonus 的全部列。调整这些字段之前需要同族样本对照和客户端测量。教学触发、剧情脚本和角色初始流程可能在其他系统，不能只凭进入成功判断完成。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

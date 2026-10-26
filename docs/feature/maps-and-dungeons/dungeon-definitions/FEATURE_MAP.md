# 地下城与关卡定义修改手册

本页用于修改既有地下城入口等级和迷宫布局。维护者可把地下城 ID、迷宫坐标和实际 map ID 分开检查。

## 定位与样本

`dungeon/dungeon.lst:2` 中 ID 2 对应 `Act1/LorienInside.dgn`。实际文件 `dungeon/act1/lorieninside.dgn` 共 51 行。地图引用另查 `map/map.lst`，不要把迷宫坐标当地图 ID。

## 参数与证据

- `[background pos]` 后为单整数 `80`，见 `dungeon/act1/lorieninside.dgn:3`。标签暗示背景位置，坐标轴和单位未确认。
- `[entering title]` 是路径 `Title/LorienInside.ani`。`[cutscene image]` 是路径与整数 `Map/CutScene/Lorien.img 0`。`[minimap image]` 只有路径 `Map/MiniMap/Act1.img`，见第 5 至 10 行。三个字段的参数个数不同。
- `[worldmap pattern info]` 在 `dungeon/act1/lorieninside.dgn:11` 后有四 token ``1 2 `WorldMap/SelectdungeonSlot/elvengard.img` 1``。图像引用有路径证据，三个整数的完整用途未知。
- `[minimum required level]` 与 `[basis level]` 均为单整数 `2`，见 `dungeon/act1/lorieninside.dgn:13` 至第 16 行。前者标签指最低等级，后者标签指基准等级。不能只改其中一个就断言怪物等级一起变化。
- `[experience increasing point]` 为浮点 `1.2000000476837158`，见第 17 行。经验系数是推断，不应标成增加 120% 或固定经验数。
- `[champion]` 是五整数 `0 0 0 0 0`，`[pathgate object]` 是十整数 `361` 至 `370`，见第 19 至 22 行。五列是否对应难度未证实。门对象 ID 须查被动对象索引。
- `[maze info]` 从 `dungeon/act1/lorieninside.dgn:23` 开始。`[size]` 为 `3 3`，`[greed]` 是一个含字面 `\r\n` 的字符串 `BBMMAA\r\n BBPPEE\r\n BBGGAA`。观察到三行各六个字母，推断每格两字符。字母含义未知，不可重命名 greed。
- `[start map]` 第 29 至 31 行有四整数 `0 2 0 0`，`[boss map]` 第 33 至 35 行有 `0 1 2 1`。可观察为两对坐标，但是否候选坐标集需实测。不能以全局固定二整数 schema 截断。
- `[special passive object item]` 第 39 至 41 行有十三整数 `0 -1 2 1000 1250 1004 1250 1 -1 0 2 -1 0`。`[event monster]` 第 43 至 45 行为七整数 `1 7000 61726 1 300 80 1`。列语义未知，不能安全改数量或概率。

## 修改步骤与未知项

改门槛时只修改明确的 minimum required level，记录 basis level 是否另有需求。改路线时先画出现有 3×3 网格，核对 greed 字符数、start 和 boss 候选坐标。复用现有布局字符串，避免新增字符串表值。

要指定实际地图，可参照教学文件已有 map specification 的形状，但不可凭本样本臆造新块。运行核查入口、每个出口、首领房和通关条件。世界地图展示、地图怪物和服务端准入可能另有配置，本页不将这些效果归给单一等级字段。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

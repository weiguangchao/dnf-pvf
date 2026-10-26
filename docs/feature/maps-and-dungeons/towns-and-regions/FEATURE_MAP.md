# 城镇与区域修改手册

本页用于维护城镇区域入口和区域小地图映射。维护者可以按 region、town、area 三层键定位重复标签。

## 入口

`region/region.lst`、`town/town.lst` 分别提供区域和城镇编号。`town/town.lst:2` 的 1 指向 `Elvengard.twn`。已读 `town/elvengard.twn`、`region/arad.rgn` 和 `region/minimap/arad.mm` 的城镇 1 样本。

## 参数与证据

- `[towns]` 在 `region/arad.rgn:3` 至第 5 行含五整数 `1 2 3 4 5`。它引用城镇编号。`[name]` 和 `[english name]` 分别引用模块 19 的 `name_0010`、`name_0011`，见第 7 至 11 行。
- `[minimap]` 在 `region/arad.rgn:13` 后为 `MiniMap/arad.mm`，相对于 region。不能改为 town 的 area 路径。
- `[entering title]` 和 `[cutscene image]` 在 `town/elvengard.twn:3` 至第 6 行分别为一个路径与路径加整数 `0`。`[dungeon what must be cleared]` 为 `-1`，见第 7 行。推断 -1 表示无前置，实际服务端行为未验证。
- 三个 `[area]` 块在 `town/elvengard.twn:9`、第 13、17 行。第一块记录 ``0 `Elvengard/Elvengard.map` `[minimap rect]` 372 242 438 268 `[/minimap rect]` `[normal]` ``，共九个 token。带反引号的 minimap rect 是记录内字符串，不是独立标签。
- area 1 的末尾是 `[gate] 474 234`，共十一 token。area 2 末尾是 `[dungeon gate] 1`，共十 token。见 `town/elvengard.twn:14`、第 18 行。不同区域类型的尾参数不同，末整数 1 的关联目标需进一步核查。
- `[limit level]` 在 `town/elvengard.twn:24` 后为单整数 `1`。标签支持城镇等级限制，是否与地下城最低等级共同生效需客户端核对。
- 小地图 `[image]` 内的 `[map]` 和 `[background]` 在 `region/minimap/arad.mm:3` 至第 9 行，各为图像路径加整数 `0`。
- 第一个 `[town]` 在 `region/minimap/arad.mm:11` 至第 65 行，index 为 1。首个 area 第 15 至 37 行，index 为 0，type 为 0。`[real rect]` 为 `10 157 1558 355`，`[project rect]` 为 `462 340 569 372`。推断为真实与投影矩形，端点制和单位未实测。
- 同一 area 中两次 `[npc]` 分别为 `8 1335 173` 和 `1 445 173`，见 `region/minimap/arad.mm:25` 至第 28 行。三个整数中第一列与 NPC 索引一致。地图脚本的 NPC 1 在 `map/elvengard/elvengard.map:68` 的 y 为 186，两个导出值不同，不能假定它们自动同步。
- `[grid map]` 内 `[level] 1` 与 `[image number] 0` 见 `region/minimap/arad.mm:29` 至第 35 行。它不同于后续 world 块内两整数的 level，不能全局同改。

## 修改步骤与未知项

先锁定 town ID 和 area ID。修改区域地图路径时复用归档内现有路径，保留类型尾参数。移动小地图 NPC 时只改相同 town 和 area 内目标 npc 的两坐标候选值，同时核对实际 map 中的 NPC。

入口限制和 minimap 展示是不同配置。检查城镇可进入性、区域切换及投影位置。矩形端点、type 全枚举、gate 尾参数的目标域尚未确认。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

## 城镇与地下城入口检查

按 region、town、worldmap、dungeon、map 逐层核对入口，并检查各层 `.lst`、选图 UI、等级和前置任务。排查已有入口时，依次核对区域包含的 town ID、城镇中的地图路径、选图引用的 dungeon ID 和地下城引用的房间。

当前 `town/elvengard.twn` 的 `[area]` 直接保存 `Elvengard/Elvengard.map` 路径，并非每处都保存 map ID。这个字段以 `map/` 为基准，对应实际条目 `map/elvengard/elvengard.map`。其他字段的路径基准须按各自资源系统核对。进入等级以目标文件现值为准，新增城镇或房间还受回包器不能收入新增磁盘文件的限制。

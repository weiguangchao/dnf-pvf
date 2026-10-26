# 世界地图与关卡地图修改手册

本页用于维护地下城选择入口与祭坛选关图。维护者需要同时核对 wdm、UI 按钮和 stm 的关联 ID。

## 定位

`worldmap/worldmap.lst:2` 的 1 指向 `Lorien.wdm`。样本 `worldmap/lorien.wdm` 共 26 行。祭坛入口另读 `stagemap/stagemap.lst` 和 `stagemap/advancealtar.stm`，不能把 stm 当 wdm。

## 参数与证据

- `[map image]` 在 `worldmap/lorien.wdm:3` 后为 `WorldMap/Lorien.img 0`，路径加帧候选整数。`[ui path]` 为单路径 `WorldMap/UI/Lorien.ui`，见第 5 行。
- `[dungeon]` 第 7 至 9 行有八整数 `1 -1 2 -1 1500 428 1501 4340`。可观察为四对。`worldmap/ui/lorien.ui:26`、第 32、38、44 行按钮末整数分别为 `1 2 1500 1501`，支持配对首列引用地下城编号。第二列 -1、428、4340 用途未确认，不能直接称为前置任务。
- `[name]` 在 `worldmap/lorien.wdm:11` 后为模块 15 的 `name_00700`。文本改动须查 .str。
- `[hell dungeon]` 为 `1`，`[hell quest]` 闭合块中为单整数 `2610`，见 `worldmap/lorien.wdm:14` 至第 18 行。后者按标签推断为任务引用，须到任务索引查。
- `[hell freepass item]` 在 `worldmap/lorien.wdm:20` 至第 22 行为 `666666 1`。标签支持通行道具关系，第二列是否数量需实测。`[item condition]` 第 24 至 26 行为 `3330`，与 freepass 分开保留。
- UI 每个 `[ui controls]` 自成块。`worldmap/ui/lorien.ui:25` 至第 29 行含十 token `[balloon] IDC_WORLDMAP_BUTTON1 478 331 1 WorldMap/selectdungeon02.img 3 1 13 1`，另有 common action 路径 `Action/worldmap_balloon.act`。坐标推断为第 3、4 列，其他控制列未知。
- `[A]`、`[B]` 在 `worldmap/worldmappatterntable.tbl:3`、第 5 行，每组后有 60 个整数。A 开头 `102 359 52 359 102 314`，疑似位置表。缺少独立列说明，不能安全重排。
- `stagemap/advancealtar.stm:5` 至第 41 行是 area 0。`[slot image]` 是图像路径，`[slot type]` 有十整数 `0 5 6 7 2 1 8 9 10 3`。它不是 stage 的四列记录。
- district 1 在 `stagemap/advancealtar.stm:13`，append image 为路径与整数 1。紧随 stage 块第 17 至 19 行有四组四整数 `3511 97 398 0`、`3512 154 444 0`、`3513 225 457 0`、`3514 300 418 1`。推断为地下城 ID、两坐标和状态，但状态 1 含义未知。
- district 2、3 分别从第 21、29 行开始。`[survival]` 第 37 至 39 行只有 `3523`。不要把 survival 套入四整数 stage 记录。

## 修改步骤与未知项

替换一个选关入口时先确认 dungeon ID，再检查 wdm 配对、UI 按钮末列和目标 dgn。只移动按钮时记录完整 UI 控件名，不改地下城编号。祭坛修改必须在目标 district 内选中 stage，不跨区全局替换。

地图选择界面不证明可进入副本。回归需检查按钮位置、提示、深渊切换与实际进入目标。配对第二列、slot type、末状态和 pattern 表映射仍需运行证据。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

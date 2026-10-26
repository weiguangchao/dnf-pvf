# 场景地图与地块修改手册

本页用于调整既有场景引用、NPC 摆放和通行区域。维护者需要区分地图脚本、地块脚本与二进制动画。

## 定位与实物

主要样本 `map/elvengard/elvengard.map` 共 83 行。其相对路径 `Tile/ForestOver.til` 可在同场景下找到 `map/elvengard/tile/forestover.til`。`Animation/far1.ani` 对应 `map/elvengard/animation/far1.ani`，实读为二进制字节，不能用文本编辑器改。

## 参数与上下文

- `[player number]` 在 `map/elvengard/elvengard.map:5` 后接 `2 8`。推断上下限，但不能断言此城镇实际有八人上限。样本同时含 PVP 字段，可能保留历史用途。
- `[pvp start area]` 第 7 行后为十二整数，开头 `668 207 558 240`。`[pvp practice start area]` 第 9 行后为八整数。按四元组分组是形状推断，矩形端点或宽高语义尚未确认。
- `[type]` 是反引号枚举 `[normal]`，见第 11 行。`[tile]` 第 13 至 15 行有七个 `Tile/ForestOver.til` 路径。重复引用可能是重复铺设，不可去重。
- `[far sight scroll]`、`[middle sight scroll]`、`[near sight scroll]` 分别为 `50 90 110`，见第 17 至 22 行。推断视差参数，不能标注百分比或像素。
- `[background animation]` 包含两个 `[ani info]`。第一块 `map/elvengard/elvengard.map:25` 至第 33 行的 filename 是 `Animation/far1.ani`，layer 为 `[distantback]`，order 为 `[below]`。第二块第 35 至 43 行使用 `Animation/mid1.ani` 与 `[middleback]`。同名字段必须按父块选中。
- `[town movable area]` 第 47 至 49 行有 24 个整数，首六个 `-5 192 29 141 2 1`。`[virtual movable area]` 第 51 至 53 行有十二整数，开头 `10 196 1548 142`。观察到六整数与四整数分组候选，连接目标和边界单位未知。
- `[animation]` 第 59 至 61 行有 90 个 token，开头 `Animation/ElvenSgate.ani [normal] 1094 359 0`。可分十八组五 token。位置三整数的轴与单位尚未实测。
- `[passive object]` 第 63 至 65 行为 24 个整数，六组四整数，首组 `5 150 150 0`。第 74 至 76 行再次出现完全相同的块。不要把第二次出现当作重复垃圾删除。
- `[NPC]` 第 67 至 69 行为两组五 token ``8 `[left]` 1335 173 0`` 和 ``1 `[left]` 445 186 0``。第 78 至 80 行再次出现。NPC ID 可到 `npc/npc.lst` 查，方向是字符串枚举。
- `[IMAGE]` 大写出现在 `map/elvengard/tile/forestover.til:3`，接 `Map/01tile03.img` 与 `0`。`[pass type]` 第 6 行有 420 个整数。数值 2 的通行含义、网格尺寸和扫描顺序未知。

## 编辑步骤与未知项

移动 NPC 先记录选中的是第一次还是第二次 NPC 块，再只改目标记录的坐标候选整数。保留 ID、方向和末整数。游戏里检查实际位置以及小地图标记，后者另见 region 配置。

通行改动需要证明 pass type 的网格映射，当前证据不足以安全改写 420 格。二进制 ani 只能复用已有路径或交给匹配格式工具，不能把乱码转存 UTF-8。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

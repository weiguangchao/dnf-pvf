# NPC 定义与交互角色修改手册

本页为修改 NPC 的代理提供身份、交互入口和对话条件的实物证据。维护者应保留角色绑定与重复对话块的边界。

## 入口与已观察结构

从 `npc/npc.lst:2` 查 NPC ID 与文件名。该行含 `9` 和 `Shylock.npc`。实际导出路径为 `npc/shylock.npc`，共 534 行。不要把 NPC ID 9 和商店 ID 7 混为一谈。

## 参数与证据

- `[small face]`、`[big face]`、`[popup face]` 各接路径字符串和一个整数。`npc/shylock.npc:3` 至第 8 行分别使用 `Map/Npc/NpcFace02.img` 与 `7`、`6`、`8`。整数推断为图像帧索引，未验证客户端。
- `[field animation]` 接一个路径。`npc/shylock.npc:9` 后是 `Animation/Npc_gbn.ani`。这是场景动画引用，不是 NPC 定义 ID。
- `[field wav]` 接 `R_NPC_GOBLIND_AMB_LOOP`。`[popup wav]` 接两个字符串 `R_NPC_GOBLIND_TALK`、`R_NPC_GOBLIND_FAREWELL`。见 `npc/shylock.npc:11` 至第 14 行。不要把两个声音合并为一个 token。
- `[role]` 至 `[/role]` 内为反引号字符串 `[item shop]` 和整数 `7`。见 `npc/shylock.npc:15`。`itemshop/itemshop.lst:2` 的 7 对应 `Rare1.shp`，`itemshop/rare1.shp:4` 又写 NPC 9。这个双向关系支持商店绑定解释。
- `[name]`、`[field name]`、`[quest speech]` 分别引用模块 8 的 `name_3965`、`field_name_3970`、`quest_speech_3975`。见 `npc/shylock.npc:23`、第 26、29 行。显示字面量不是改名入口，须查字符串模块。
- 第一个 `[dialog]` 块位于 `npc/shylock.npc:32` 至第 35 行。数据是六个整数 `1 1 99 -1 0 0` 和一条本地化引用。第二块第 37 行起为 `2 1 99 -1 0 0`。第 47 行起为 `4 5 12 -1 0 0`。第 2、3 列推断是等级区间，其余条件列尚未确认。不能只按标签全局替换。
- `[favor_dialog]` 是另一种记录。`npc/shylock.npc:67` 至第 70 行含三个整数 `3 0 0` 和一条文本引用。它不采用普通 dialog 的六整数形状。
- `[speech]` 的 ```2 1 10 `[goblin]` `` 3 4 5 6``` 有九个 token。见 `npc/shylock.npc:19`。各列含义未知，空字符串也是 token。

## 实际修改步骤与未知项

先用 ID 定位 NPC，再从 `[role]` 跟到商店索引和商店 `[NPC]`。换现有商店时同步检查反向 NPC 绑定。只改某段对话时记录块序号、六整数条件和字符串 key。不要移动 favor_dialog 到 dialog。

外观可复用归档中已有动画路径。保存后核对角色窗口、商店内容和目标条件下的对话。声音资源是否存在、普通 dialog 的完整条件枚举以及 speech 列语义尚未验证。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

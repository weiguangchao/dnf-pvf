# 普通商店与 NPC 商品修改手册

本页用于替换普通商店已有商品和检查 NPC 入口。维护者可沿两个索引重建绑定，避免只改一个同名文件。

## 定位与样本

`itemshop/itemshop.lst:2` 是整数 ID 与反引号路径交替的索引。7 指向 `Rare1.shp`，53 指向 `stackableshp28.shp`。实际样本 `itemshop/rare1.shp` 有 12 行，`itemshop/stackableshp28.shp` 有 18 行。

## 参数与记录形状

- `[NPC]` 大写必须保留。`itemshop/rare1.shp:4` 为单整数 `9`，与 `npc/npc.lst:2` 的夏洛克对应。NPC 自身的 `[role]` 用商店 ID 7，见 `npc/shylock.npc:16`。
- `[type]` 是一个反引号枚举。`itemshop/rare1.shp:6` 为 `[etc shop]`，`itemshop/equipmentshop11.shp:6` 为 `[weapon shop]`。不能以目录名替换枚举。
- `[sell item]` 至 `[/sell item]` 是整数流。`itemshop/rare1.shp:8` 共 84 个整数，开头 `1055 1056 1057 1058 -1 -1 24051`。观察到负数占位，未证明固定列宽或每列 UI 含义。这里没有价格元组。
- `itemshop/stackableshop1.shp:8` 有 77 个整数，开头 `2610039 2610040 2610041`。商品 ID 须到 `stackable/stackable.lst` 或 `equipment/equipment.lst` 查定义。不要用索引中的商店 ID 作物品 ID。
- `itemshop/stackableshp28.shp:8` 同时含 `-1` 与 `-2`。`-2` 前后紧邻 `-1 -1 -1 -1 -2 27742 27593`。推断涉及分页或分隔，但未确认，替换商品时保留这些哨兵及位置。
- `[tab name]` 在 `itemshop/stackableshp28.shp:11` 至第 15 行，接两个本地化引用 `tab_name_ss1` 和 `tab_name_ss2`。显示为"兑换1""兑换2"，不证明每页有固定商品数。
- `[message]` 接一条本地化引用。`itemshop/rare1.shp:12` 为模块 5 的 `message_430`。`itemshop/equipmentshop11.shp:7` 至第 9 行的 sell item 则为空块。空店也可能是有效原始配置。

## 替换已有商品

先确认 NPC role 的商店编号。记录目标 sell item 内的 token 偏移及相邻负数。把一个正整数商品 ID 换成归档内已存在的物品 ID，不改占位和总长度。若需新增页或改变栏位布局，先用客户端验证 `-1`、`-2` 的作用，本页证据不足以给出安全扩容公式。

价格、兑换材料和限购不在上述 sell item 流中明确编码。应继续查物品定义和特殊商店规则。游戏中检查 NPC 入口、页签、商品顺序及实际购买扣除。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

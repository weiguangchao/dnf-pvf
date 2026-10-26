# 特殊商店、积分与购买奖励修改手册

本页用于定位秘密商店、NPC 随机兑换和购买奖励。维护者需保留 NPC、等级段和地下城各自的嵌套范围。

## 入口与不同格式

读取 `etc/secretshop.etc`、`etc/mileageshop.etc`、`etc/exchangeitemnpc.etc`、`cashshop/purcahsebonusitem.shp` 和 `nexon/cerashopmileage.txt`。最后一个是原始文本，不是带 PVF 头的脚本。不要为它补 PVF 头或套用脚本编译规则。其重新入包能力尚未验证。`cashshop/sudden_shop_1.shp:9` 的 item 块为空，不能从空文件推断限时商品元组。

## 参数与证据

- `[eplp wait time]` 在 `etc/secretshop.etc:3` 后接 `3`。`[price random]` 后接 `10`，见第 5 行。标签拼写 eplp 不可修正。时间单位和随机价格算法未知。
- `[level section]` 的 `etc/secretshop.etc:12` 有 27 个整数，九组三整数。首两组 `0 1 18`、`1 19 27`，末组 `8 73 200`。推断为段号和等级边界。
- `[dungeon npc]` 在 `etc/secretshop.etc:7` 至第 9 行，714 个整数可分 102 组七整数。首组 `41 1000 10000 10000 10000 10000 10000`。前两列疑似地下城与 NPC ID，后五列语义和概率分母未知。
- 第一个 `[npc]` 在 `etc/secretshop.etc:19` 至第 101 行，NPC 为 `1002`。其中首个 `[level]` 第 21 至 23 行有 194 个整数，开头 `0 2 27046 0 20000 0 1 5`。观察到两整数前缀与 32 组六整数候选条目。各列价格、数量或权重用途尚未证实。
- 同一 NPC 下 `[dungeon]` 第 57 至 59 行有 170 个整数，开头 `1504 2 2651000 0 1000000 0 1 10`。切勿把它当成 level 段。NPC 1003 的块从第 103 行开始，NPC 1004 从第 179 行开始。
- `etc/mileageshop.etc:10` 的 `[coin]` 只有十个 token ``16596 1 5 0 1900 0 `啭樯 5偃` 4 0 -1``。第 14 行 item 有 80 个 token，呈八组十 token。乱码是实际导出显示，不可据此猜币种或重新翻译覆盖。
- 外层 `[exchange item]` 从 `etc/exchangeitemnpc.etc:3` 到第 69 行。NPC 103 的 list 1 中，内层同名 `[exchange item]` 第 9 至 11 行为 `690000687 1`。随机输出块第 13 至 15 行有八组三整数，首组 `2000 690000691 5`。三列推断为权重、物品、数量，八组首列合计 10000，不证明运行概率算法。
- `cashshop/purcahsebonusitem.shp:3` 至第 5 行的首个 bonus 块含十整数 `510494 1 5 100 2 5 150 3 5 200`。第 7 行起是编号 510495 的另一块。首整数后为三组三整数，不能凭数字将其中一列断言为返利百分比。
- `nexon/cerashopmileage.txt:1` 明写 `[default]` 和 `percent`，次行为 `0 20`。第 3、4 行写 `[item] ipg_no percent` 和 `//no ipg percent`，第 5 行是 `0 510525 0`。此处 percent 有表头证据，但计算基数及生效入口未知。

## 修改步骤与未知项

秘密商店先锁定 NPC，再锁定 level 或 dungeon 及首整数键，只替换该块内已存在商品。NPC 兑换先选 npc 和 list，再修改消耗二整数或输出三整数，不触碰外层同名标签。购买奖励按首整数商品号定位 bonus，保留完整十整数。

积分文本的列说明不应推广到 mileageshop 或 bonus。是否服务端读取 nexon 文本尚未证明。回归需分别观察触发、候选商品、扣除与发奖，不能只看商店打开。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

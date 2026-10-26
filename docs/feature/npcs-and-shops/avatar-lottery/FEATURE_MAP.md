# 时装抽取与轮盘修改手册

本页用于检查既有抽取池、职业展示列表和轮盘权重候选值。维护者须保留职业分块与不同列表的记录宽度。

## 入口与样本

按部位读取 `cashshop/hair_avagacha.shp`，共 53 行。宠物格式另见四行的 `cashshop/creatur_avagacha.shp`。轮盘另有 `cashshop/avarulet.shp` 和 `etc/avatar_roulette_jar.etc`，不能将它们当作同一 schema。

## 参数与证据

- `[spending item]` 在 `cashshop/hair_avagacha.shp:3`，其后到 avatar list 之前没有值。样本不能说明消耗道具从何处取得，不能随意补一个整数。
- `[avatar list]` 的 `cashshop/hair_avagacha.shp:6` 有 385 个 token，可分为 77 组五 token。首组 ``525000 `[swordman]` 2677040 3 1000``。观察到编号、职业枚举和整数三列，后三列用途与权重单位尚未确认。
- `[hair avatar ability list]` 的 `cashshop/hair_avagacha.shp:10` 有 1925 个 token，即 385 组五 token。前两组 ``525000 `[swordman]` 1 0 1000`` 与 ``525000 `[swordman]` 1 1 1000``。第一列连接 avatar list 的 525000，第四列变化。不能将 1000 直接解释为百分数。
- `[avatar display]` 在 `cashshop/hair_avagacha.shp:13` 接职业枚举与 `99`。紧随的 `[display avatar list]` 在第 15 至 17 行，396 个整数可分为 99 组四整数。首两组 `2677015 0 0 0`、`2677040 1 0 0`。99 与组数一致，但三个状态列语义未知。
- 同名 display 块在第 19、25、31、37、43、49 行分别属于 `[fighter]`、`[gunner]`、`[mage]`、`[priest]`、`[at gunner]`、`[thief]`。修改时先定位前一个 avatar display 的职业。
- `[Creature list]` 大写 C 必须保留。`cashshop/creatur_avagacha.shp:4` 有 108 个整数，观察到 12 组九整数。首组 `510086 63022 1000 1 1 63023 0 0 9`。宠物 ID 与商品编号关系需查相应索引，不能套五列时装格式。
- `[swordman]` 的 `cashshop/avarulet.shp:4` 共 119 个整数。开头 `520 39169 2770004 39254 39266`。后续职业块也各 119 个整数。未确认内部列宽，不能凭整除猜测轮盘槽含义。
- `[avatar coin info]` 在 `etc/avatar_roulette_jar.etc:3` 至第 5 行含 `202`。随后四个 rate 标签的值依次为 `0 0 200 800`，见第 7 至 14 行。和为 1000 是观测结果，归一化权重是推断，百分比单位未证实。
- `etc/avatar_roulette_jar.etc:16` 的 `[swordman]` 块有 110 个整数，开头九个物品候选 ID 后跟 `0`。职业名 `[at_gunner]` 使用下划线，`[DemonicSwordman]` 保留大写，见第 35、51 行。

## 修改步骤与未知项

换一个已有时装时同时检索 avatar list、ability list 与该职业 display list 的同一编号。保留五 token 与四整数的各自形状。只改目标职业块。轮盘 rate 调整先记录四值与合计，再由客户端验证各档实际出现情况。

未确认的能力枚举、宠物九列、avarulet 的槽结构都不能安全扩容。资源编号不等于装备定义已存在，替换前须查装备索引。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

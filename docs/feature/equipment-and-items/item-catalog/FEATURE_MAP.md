# 物品索引、价格与编号修改手册

## 定位次序与样本

先确认目标为装备还是堆叠物。`equipment/equipment.lst`、`stackable/stackable.lst` 是 ID 到相对路径的入口。`itemname.lst` 是名称到 ID 的另一种顺序。图鉴、价格表和编号说明不能替代实际索引。

本页对两个物品索引和名称索引做了反引号 token 解析，并读取 `equipment/pricetable.tbl`、`stackable/pricetable.tbl`、`etc/itemtypemaster.etc` 和两份图鉴表。输出中的路径例子一律相对 output，索引内部值则按所在目录解析。

## 索引格式与引用

- `equipment/equipment.lst:2` 有 123582 个 token，即 61791 对整数 ID、反引号路径。实测 `27733` 配 `character/swordman/weapon/katana/kat_hightechq.equ`，输出对应 `equipment/character/swordman/weapon/katana/kat_hightechq.equ`。token 总数不能用磁盘文件总数替代。
- `stackable/stackable.lst:2` 有 28870 个 token，即 14435 对。实测 `1110` 配 `ptn_hphighest.stk`，`2600149` 配 `professional/recipe/rcp_ptn_hphighest.stk`，`3626` 配 `monsterCard/mcard_gblbeliever.stk`。磁盘目录使用 `stackable/monstercard`，不能据大小写差异重写归档路径。
- `itemname.lst:2` 有 21390 个 token，即 10695 对，顺序是字符串名称在前、整数 ID 在后。首条名称的可见内容含乱码并指向 `7012`，末条为韩文 `힐스 스커트` 配 `4000`。不能把它当物品索引的整数、路径对解析，也不因名称乱码自动转换全部编码。
- 物品 `[name]` 常为本地化引用。例如 `equipment/character/swordman/weapon/katana/kat_hightechq.equ:3` 是 `<3::name_27733` 加显示文字，`stackable/ptn_hphighest.stk:3` 是 `<13::name_1110` 加显示文字。显示文字不是编译输入，改中文应改相应 `.str` 的原有键。name 键尾数字与物品 ID 相符只是样本现象，不能将所有键名数字作为 ID。
- `equipment/equipmentnumbersection.txt:6` 和第 7 行可见注释数字区间 `1 ~ 65535`、`65536 ~ 75536`。文件并非 `#PVF_File` 脚本，注释中的原文字节不能由 UTF-8 错误解码后的显示反推。`stackable/stackablenumbersection.txt` 只有一行注释。编号说明不是当前空闲 ID 的证明，也不能据它分配新 ID。

## 价格表与类型表

- `[repair cost]` 在 `equipment/pricetable.tbl:5` 为单浮点 `0.07649999856948853`。第 3 行实际标签为 `[绿徽]`，后有三个整数 `200 150 30`。标签字面已观察，但其用途未解释，不能因为看似异常就重命名。
- `[1]` 在 `equipment/pricetable.tbl:7` 有 100 个整数，开头 `10 20 30`、末尾 `1000`。`[30]` 第 65 行也是 100 项，开头 `10000 20000 30000`、末值 `1000000`。标签数字与数组位置各自构成维度，等级和类别映射未确认，不能把标签 30 当物品 ID。
- 堆叠物表 `stackable/pricetable.tbl:3` 的 `[1]` 同样从 `10 20 30` 开始，但文件没有装备表的 repair cost 前置段。不要把整份装备价格表拷给堆叠物。
- 单件物品仍可能显式写 `[price]`、`[repair price]`、`[value]`。太刀 `equipment/character/swordman/weapon/katana/kat_hightechq.equ:33` 到第 38 行分别为 `86800`、`72912`、`69440`。这些字段与全局表的覆盖顺序未确认。改单件价格应先定位现有单件字段，再验证真实交易金额。
- `[master type]` 在 `etc/itemtypemaster.etc:3` 为整数 `10` 加一个显示为乱码的字符串，后续同标签用 `20`、`30` 等。`[material type]` 第 27 行为 `0` 加字符串。整数与名称是两种 token，不能把乱码显示当新枚举名回写。
- `[weapon type]` 在 `etc/itemtypemaster.etc:37` 的形状是职业字符串、三个整数、名称字符串，开头 `[swordman] 10 0 10` 加名称。第 39 行下一组为 `[swordman] 10 1 20`。它不等于 `.equ` 的 `[equipment type] [weapon] 22`，不能交叉替代。

## 图鉴表

- `[base table]` 在 `etc/itemdictionary/(r)baseitemdictionarytable.etc:3` 有 22748 个整数，可按 11374 对观察。开头 `10564 0 12561 1 20238 2`，末对 `106000047 11373`。形状支持物品 ID 与图鉴顺序的关系，修改前应先去装备索引解 ID。
- `[equipRecipe list]` 在 `etc/itemdictionary/(r)recipelistmakeequip.etc:3` 有 11189 个整数。开头 `10113 2647008 0 0 0 1 44 0`，末尾 `109020042 2651315 0 0 1 0 0`。开头像八列而尾部不同，不能把整表机械切成固定八列。装备与配方关联需逐条核对，未知控制位不能安全重排。

## 修改步骤与未知项

1. 由 ID 查原有索引和文件。改价格先改目标单件字段，保留索引路径不动。改本地化时解析 module、key，再改原 `.str` 值并保留原编码。
2. 改类型展示前区分 itemtypemaster 与物品真实 type。名称索引和图鉴显示不等于运行时装备类型。
3. 新建 output 文件会被编译忽略，删除已有文件会从归档移除。不能把编辑索引或新增文件当作成功新增物品。原归档字符串表不接受任意新名称、标签和路径。
4. 保留脚本 `#PVF_File\r\n`、CRLF、TAB 与 token 类型。注释文件与 `.str` 不套脚本格式。Markdown 展示空格不保留原文件分隔。
5. 核对原 ID 仍解析到原文件、索引 token 成对、价格数组长度及未改名称。重建后重新提取，客户端检查搜索、名称、购买、出售、维修与图鉴。`--verify` 不检验修改后的 output。

本页未确认全局价格表与单件字段的优先级、全部类型整数映射、乱码原意和图鉴变长记录语法。不能安全批量清理或翻译这些未知结构。

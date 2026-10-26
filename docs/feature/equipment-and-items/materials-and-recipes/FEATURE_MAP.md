# 材料与制作配方修改手册

## 入口与引用链

先查 `stackable/stackable.lst:2`。实测 `3080` 指向 `material/stone_magic.stk`，`2600149` 指向 `professional/recipe/rcp_ptn_hphighest.stk`，`2650905` 指向 `recipe/nrcp_rev_teranite_up.stk`。本页读取这三个输出文件和产物 `stackable/ptn_hphighest.stk`。配方 ID、材料 ID、产物 ID 分别解析，不能把文件扩展名当最终物品类型。

## 材料字段

- `[name]` 在 `stackable/material/stone_magic.stk:3` 为 `<13::name_3080` 加显示文字魔晶石。它是本地化引用，不能只改显示文字。
- `[grade]` 为 `1`，`[rarity]` 为 `3`，`[minimum level]` 为 `1`，见 `stackable/material/stone_magic.stk:9`、第 13、21 行。等级与品质字段独立。
- `[attach type]` 在 `stackable/material/stone_magic.stk:11` 为 `[trade]`，`[usable job]` 第 17 行为 `[all]`。可交易与职业条件不是配方材料数量。
- `[stackable type]` 在 `stackable/material/stone_magic.stk:27` 为 `[quest] 0`。材料目录下也可能使用 quest 类型。不能按目录名一律改成 material。
- `[icon]` 在 `stackable/material/stone_magic.stk:23` 为路径 `Item/IconMaterial2.img` 加帧 `51`，`[field image]` 第 25 行为路径加帧 `24`。图标与地面显示分别修改。

## 炼金配方

- `[stackable type]` 在 `stackable/professional/recipe/rcp_ptn_hphighest.stk:25` 为 `[recipe] 0`，`[sub type]` 第 27 行为 `0`，`[price]` 第 29 行为 `10000`。不能将价格当制作费直接相加。
- `[int data]` 在该图纸第 33 行有 12 个整数，完整序列为 `2 2610001 2 2610002 2 1 1110 1 1 193 1 2`。首段符合材料数 `2` 后接两组 ID、数量的结构。堆叠物索引将 `2610001` 解析为 `professional/material/mushroom_nourish.stk`，将 `2610002` 解析为 `professional/material/honey_sweet.stk`。
- 同序列含 `1110 1`。`stackable/stackable.lst:2` 将 1110 解析为 `ptn_hphighest.stk`。该产物 `stackable/ptn_hphighest.stk:43` 的 `[hp recovery]` 为 `+ 1080 1000 myself`。这支持配方产物解释，不能因此认定后面的 `1 193 1 2` 全部列义已知。
- `[string data]` 在图纸 `stackable/professional/recipe/rcp_ptn_hphighest.stk:41` 为单字符串 `[craftmanship]`。拼写就是 craftmanship，不改成英语常见拼写 craftsmanship。
- `[bead item]` 在图纸第 37 行为空块。它不是材料遗漏，不因另一种配方有宝珠就补数据。
- `character/expertjob/alchemist.exj:31` 的第一组为 `0 2600149 1110 1`，与该图纸及产物一致。修改副职业可制作目录时也需核对这组关联。

## 装备升级配方

- `[stackable type]` 在 `stackable/recipe/nrcp_rev_teranite_up.stk:32` 为 `[recipe] 1`。它与炼金的第二值不同，`[string data]` 第 42 行为 `[machinary]`，保留原拼写。
- `[int data]` 在 `stackable/recipe/nrcp_rev_teranite_up.stk:38` 有 15 个整数 `5 31096 1 3300 1500 3167 15 2610030 30 3164 1 1 31138 1 0`。前段符合五组材料 ID、数量。装备索引将 `31096` 映射到 `character/gunner/weapon/revolver/rev_teranite.equ`，将 `31138` 映射到 `character/gunner/weapon/revolver/rev_teranite_up.equ`。材料可包含装备，不能只查堆叠物索引。
- `[need material]` 在装备配方第 46 行为 `4414 35`，堆叠物索引指向 `quest/quest_4414.stk`。它位于 `[int data]` 外，不应混入五组材料重算。
- `[minimum itemmaking level]` 在装备配方第 48 行为字符串 `weapon` 加整数 `5`。不同于第 26 行的 `[minimum level] 57`，前者指制作分类等级的解释有名称依据，实际边界仍需实机确认。
- 第 10 行说明称制作会移除附魔并调整强化、增幅。此处只是文本证据，没有给出调整公式，不能承诺数值继承规则。

## 修改步骤与未知项

1. 修改已有材料数量时先解析 ID，并确认它属于 int data 主材料还是独立 need material。保留首段材料计数和后续未知尾部。
2. 修改产物时解析目标装备或堆叠物，核对副职业 `[items]` 目录。新建 output 文件不会自动加入归档，不能把新增文件当新增配方已完成。
3. 保留所有整数类型、结束标签、CRLF、TAB 和 `#PVF_File\r\n`。字符串只能复用原归档已有值。中文改 `.str` 原有键，Markdown 空格不可覆盖原文件。
4. 核对 12 或 15 个整数、材料组数及每个 ID。真实重建后提取，再验证材料扣除、产物数量、制作等级和装备继承。`--verify` 不验证修改输出。

配方尾部的技能、成功率或熟练度列未全部确认。不能凭 `193` 与炼金技能同号就宣称尾部每列已解码。

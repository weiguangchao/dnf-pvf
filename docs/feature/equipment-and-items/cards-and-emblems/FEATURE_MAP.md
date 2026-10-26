# 附魔卡片、宝珠与徽章修改手册

## 入口与样本

堆叠物索引 `stackable/stackable.lst:2` 将 `3626` 映射到 `monsterCard/mcard_gblbeliever.stk`，将 `2500005` 映射到 `emblem/red/brightemblem_redstr.stk`。输出磁盘路径分别为 `stackable/monstercard/mcard_gblbeliever.stk`、`stackable/emblem/red/brightemblem_redstr.stk`。本页还读取附魔配方 `stackable/professional/recipe/rcp_mcard_gblbeliever.stk`、宝珠 `stackable/professional/bead/bead_int.stk` 和孔映射 `etc/chn_equipmentsockettypelist.etc`。

## 卡片与宝珠字段

- 卡片 `[stackable type]` 在 `stackable/monstercard/mcard_gblbeliever.stk:32` 是 `[material expert job] 1`，`[sub type]` 第 34 行是 `1`。它不是可直接使用的 `[enchant waste]` 宝珠类型。
- 卡片 `[string data]` 在第 40 行有两个字符串 `Interface/MonsterCard/MonsterCard_image.img` 与 `[coat]`。后者提示附魔部位限制，不能当图像路径一部分。
- 卡片 `[int data]` 在第 44 行只有两个整数 `8 260`。首值与图片帧有关的解释尚未确认，不能把 260 当附魔数值。
- 卡片 `[enchant]` 第 48 行内 `[magical attack]` 为整数 `4`。配方名称 `stackable/professional/recipe/rcp_mcard_gblbeliever.stk:4` 明写智力 `+4`，支持该卡片上下文中 magical attack 对应智力的解释。不能凭英文名把它当武器面板魔攻。
- 附魔图纸 `[int data]` 在 `stackable/professional/recipe/rcp_mcard_gblbeliever.stk:33` 有 14 个整数 `3 3626 1 3227 5 3166 10 1 2600320 1 1 191 2 2`。前三组材料 ID、数量的解释由卡片 3626 和三个材料计数支持，尾部未全部解释。
- 图纸 `[bead item]` 第 37 行为两个整数 `2610039 3`，`[string data]` 第 41 行为 `[enchant]`。不能把 bead item 的第二整数直接当产物数量，它与 int data 的产物字段不同。
- 宝珠 `stackable/professional/bead/bead_int.stk:35` 的 `[stackable type]` 为 `[enchant waste] 0`，`[expert type]` 第 37 行为 `[enchanter]`，`[monster card id]` 第 39 行为 `610000012`。该文件名 int 与显示名魂之挽歌力不能作为属性证据，应追踪关联卡片。
- 宝珠 `[need material]` 在 `stackable/professional/bead/bead_int.stk:27` 为 `10000204 85`，`[stack limit]` 第 25 行为 `1000`，`[price]` 第 29 行为 `3000000`。独立材料需求不能忽略。该宝珠自身没有 `[enchant]` 数值块，不照卡片补一个。

## 徽章与孔类型

- `[stackable type]` 在 `stackable/emblem/red/brightemblem_redstr.stk:32` 为 `[avatar emblem] 0`。`[avatar emblem target type]` 第 34 行内为单字符串 `[A socket]`，有结束标签。名称颜色不是实际孔匹配枚举。
- 徽章 `[enchant]` 在 `stackable/emblem/red/brightemblem_redstr.stk:42` 内 `[physical attack]` 为 `8`。第 4 行名称含力量，支持该样本的力量解释。标签在 enchant 内，不能改到装备文件顶层同名字段。
- 徽章 `[stack limit]` 第 38 行为 `1`，`[usable period]` 第 40 行为 `3`。期限单位未确认，不直接写成三天。
- 徽章 `[icon mark]` 在第 18 和第 28 行各出现一次，帧分别为 `63` 与 `23`。保留两次出现和顺序。
- 孔映射 `etc/chn_equipmentsockettypelist.etc:29` 的 `[equipment type]` 为 `[waist]`，其 `[socket info]` 为两个 `[A socket]`。第 47 行的 `[ring]` 也是两个 A 孔。第 53 行辅助装备和第 59 行魔法石各为一个 `[S socket]`。按部位块定位，不全文替换孔枚举。
- 实测孔映射的戒指块以 `[/socket]` 结束，见 `etc/chn_equipmentsockettypelist.etc:51`。其他块多以 `[/socket info]` 结束。不能在无解析证据时顺手修正这个差异。

## 修改步骤与未知项

1. 改卡片属性只动 `[enchant]` 内的目标整数，并同步核对图纸显示。宝珠则先追踪 monster card id，不用文件名猜效果。
2. 改徽章属性时保留孔枚举和 enchant 上下文。改孔适配时确认所有目标部位，保留单孔或双孔数量。
3. 保留 CRLF、TAB、`#PVF_File\r\n` 和原 token 类型。中文改 `.str` 既有键。内联显示不是编译输入，本文空格不是源文件分隔。
4. 核对材料计数、卡片引用、孔类型及重复标签。重建后提取，并在客户端测试附魔部位限制、材料扣除、徽章插入和属性增加。`--verify` 不验证修改输出。

卡片 int data、bead item 第二列、期限单位和孔映射异常结束标签的客户端解析规则未确认。没有这些证据时不能安全重排数据。

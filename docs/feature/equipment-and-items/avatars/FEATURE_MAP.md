# 时装与外观修改手册

## 定位入口

装备索引 `equipment/equipment.lst:2` 将 `101500528` 映射到 `character/swordman/avatar/coat/101500528.equ`。本页读取其 62 行，并读取 `equipment/character/swordman.lay`、`etc/compoundavatar.etc` 与 `etc/compoundavatar_swordman.etc`。时装属性、动作层次和合成结果是不同入口，改一个文件不会自动同步另两个。

## 时装字段

- `[equipment type]` 在 `equipment/character/swordman/avatar/coat/101500528.equ:25` 为 `[coat avatar] 0`。这是时装上衣枚举，与普通防具的 `[coat]` 不同。
- `[usable job]` 在时装第 15 行含 `[swordman]` 和 `[demonic swordman]`。`[minimum level]` 第 21 行为 `1`，`[attach type]` 第 19 行为 `[trade]`。允许职业不等于已有完整动画。
- `[enable dye]` 在时装第 9 行为两个整数 `1 0`。名称提示染色开关或通道，第二列语义未确认，不能删成单布尔。
- `[grade]` 第 11 行为 `2`，`[part set index]` 第 13 行也为 `2`，见 `equipment/character/swordman/avatar/coat/101500528.equ`。数值相同不代表同一字段。`etc/equipmentpartset.etc:3` 的套装编号 2 指向 `character/partset/upperset.equ`，可核对这条关联。
- `[avatar type select]` 在时装第 27 行有 22 个 token。前 20 个为整数，开头 `7 0 0 600 0 30`，尾部 `2600 2`，最后两个为字符串 `[C socket] [C socket]`。此块混有数值与孔枚举，不能全部按属性值解释，也不能把 600 等直接写成秒。
- `[avatar select ability]` 在 `equipment/character/swordman/avatar/coat/101500528.equ:31` 有 276 个 token，按样本形状可分 69 组四元组。首组 `[SKILL_LEVEL] [swordman] 39 1`，第二组 `[SKILL_LEVEL] [swordman] 41 1`。末组 `[SKILL_LEVEL] [demonic swordman] 117 1`。它是可选技能列表形状，先查职业 `.lst` 再改 ID，不能把所有候选当同时生效。
- `[avatar func filter]` 在时装第 59 行为单整数 `0`。筛选规则未确认，不因数值为零就删除。

## 职业动画与层次

- 时装 `equipment/character/swordman/avatar/coat/101500528.equ:35` 起是 `[animation job] [swordman]`，第 47 行起为 `[demonic swordman]`。两段 `[variation]` 都为 `66 3`。每段有两次 `[layer variation]`，分别是 `1800 coat_a` 与 `2300 coat_c`。各自后随 `[equipment ani script]`，分别使用 `equipment/character/swordman.lay` 和 `equipment/character/dsswordman.lay`。修改层时必须指明职业段与层名。
- `.lay` 的 `[LAYER]` 在 `equipment/character/swordman.lay:3` 为 `0`。`[waiting motion]` 第 5 行为 `%s/Stay.ani`，`[move motion]` 第 7 行为 `%s/Move.ani`。`%s` 是原有路径占位形状，替换机制未从样本确认，不能直接填中文目录。
- `.lay` 的 `[attack motion]` 在 `equipment/character/swordman.lay:43` 是三个字符串 `%s/Attack1.ani`、`%s/Attack2.ani`、`%s/Attack3.ani`。`[etc motion]` 第 47 行是另一个长列表，包含 `%s/TripleSlash1.ani` 等。列表顺序可能被动作索引使用，未确认前不重排。

## 合成配置

- `etc/compoundavatar.etc:2` 是整数与配置路径的无标签列表，`1` 配 `CompoundAvatar_swordman.etc`。在磁盘对应 `etc/compoundavatar_swordman.etc`。不要把这个 1 当作角色索引中的鬼剑士编号 0。
- `[character type]` 在 `etc/compoundavatar_swordman.etc:3` 为 `[swordman]`。`[grade]` 第 5 行为 `1`，`[upper grade]` 第 11 行为 `2`，分别与后续不同表关联。
- `[rare rate]` 第 7 行有八组字符串、整数，`hat 100` 到 `shoes 100`。`[upper rare rate]` 第 13 行八组值均为 `1000`。概率分母未确认，不能把 100 和 1000 解释成百分之百和千分之百。
- `[coat avatar]` 在 `etc/compoundavatar_swordman.etc:33` 开头为 `1 601500028 1000 9 601500000 1000 ...`。该表不是从头到尾纯 ID、权重对，保留开头控制整数。
- `[ancient bind cube]` 第 49 行内部的 `[coat rare avatar]` 在 `etc/compoundavatar_swordman.etc:67` 为 ID、整数对，首组 `40681 1000`，末组 `40891 400`，共 12 对。此处形状不同于普通 coat avatar 长表，不混改。

## 修改步骤与未知项

1. 改可选技能先解析职业和技能 ID，保留四 token 分组。改孔类型先核对实际 socket 枚举，不改未知选择数组列。
2. 改外观先核对两个职业段。只复用原归档已有 variation、层名与路径，不能靠新增 output 文件加入新资源。
3. 改合成时按普通、upper、ancient 块定位。未知普通长表语法不能安全重排，权重也不能按固定百分比分母重算。
4. 保留 CRLF、TAB、`#PVF_File\r\n`、原 token 类型和字母大小写。中文改 `.str` 既有键，本文空格不是源文件分隔。
5. 核对 22 token、69 组技能、两个动画段与 12 对稀有候选。重建并提取后，客户端检查穿戴、选技能、染色和合成。`--verify` 不验证修改 output。

尚未确认选择数组各整数列、variation 两列、层号单位和合成概率基数。二进制 ANI 未解析时不能用文本修改。

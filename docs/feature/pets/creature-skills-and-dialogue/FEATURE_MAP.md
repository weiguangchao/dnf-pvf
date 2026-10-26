# 宠物技能、动作与台词修改手册

供调整已有宠物施技和对白的代理使用。已读取银猪 `.cre`、攻击文件和完整 234 行对白，木偶的 185 行多技能定义，以及一个 `.skl` 和一个表现 `.act`。路径均相对 `output`。技能参数、命中规则和文字各有不同归属。

## 旧式技能字段

`creature/silverpig/silverpig.cre` 的下列字段在文件顶层，只各出现一次。

- 第 12 行 `[skill recovery time] 6000` 和第 14 行 `[over skill recovery time] 30000` 各接一个整数。名称提示普通与终结技能恢复时间，毫秒单位未从此文件证实。
- 第 34 行 `[learn overskill level] 26`、第 36 行 `[skill MP] 0`、第 38 行 `[over skill MP] 150` 都是单整数。终结技能解锁与消耗是按名称推断的语义。`MP` 大写不能套用木偶的 `[skill mp]`。
- 第 46 行 `[skill motion]` 为 `Animation/skill.ani`，第 48 行 `[over skill motion]` 为 `Animation/over_skill.ani`。第 58、60 行是对应的 `[skill over effect]`、`[over skill over effect]`，用于表现的推断有路径支持，不能用动画替代命中参数。
- 第 74 至 76 行 `[attack info]` 列表有两个路径，依次为 `AttackInfo/skill.atk` 与 `../../PassiveObject/Creature/SilverPig/AttackInfo/jump_attack.atk`。前者对应 `creature/silverpig/attackinfo/skill.atk`。后者跨入被动对象，修改终结攻击要另查该文件，不能全局替换第一个 `.atk`。
- 第 78 至 80 行 `[piercing]` 为四整数 `20 1 1000 0`。各列语义未证实，不能解释成四个概率。
- 第 82 至 88 行 `[skill string]` 含四个 module 16 引用，依次为普通名称、说明、终结名称、说明。键为 `silver_pig_skill_0001` 至 `silver_pig_skill_0004`。第 90 和 94 行两个 level-values 块各有四整数 `1 4 1 60`。说明中含 `%d`，但四列与占位符的计算关系未证实。
- 第 98 行 `[int data]` 有八整数 `5 300 800 50 60030 250 0 580`。第 102 行 `[string data]` 有两个粒子路径。它们是位置参数和资源列表，不把 `60030` 擅定为物品或技能 ID。

`creature/silverpig/attackinfo/skill.atk:3` 的 `[damage] 120` 是有值字段。该文件第 15 行 `[damage reaction]` 后是无值枚举 `[down]`。`[attack type]` 后是 `[physic]`，`[elemental property]` 后是 `[no element]`，`[attack direction]` 后是 `[hit horizon]`。第 19 行 `[push aside] 200`、第 21 行 `[lift up] 200` 各接整数。第 33 行 `[no blood] 100 1.0` 是整数和浮点的二元组。距离、伤害缩放和最后二元组单位未知。

## 多技能节点不能按旧式字段批改

`creature/woodendoll/woodendoll.cre:68` 的 `[skill list]` 包含四个 `[skill node]`，节点号分别为 0、1、2、3。节点 0 在第 70 至 96 行。节点 1、2、3 分别起于第 98、126、154 行。

- 节点内 `[skill type]` 接普通字符串 `general skill`，与模板 `creature/creaturesample.cre:109` 的 `` `[active]` `` 不同。
- 节点 0 的 `[skill recovery time] 40000`、`[learn skill level] 1`、`[skill mp] 10` 在第 80 至 85 行各为单整数。其余三个节点各有自己的同名字段，修改时必须先锁定节点号。
- 节点 0 第 92 行 `[skill info]` 引用 `skill/skill1.skl`，该文件第 3 行 `[pre teleport]` 为 `100` 加 `Animation/woodendoll_tele.ani` 和空字符串，第 5 行 `[post teleport]` 为 `0` 加相同动画和空字符串。两者都是整数与两字符串的三元组，首整数含义和单位未证实。
- 节点 0 第 88、90 行的 under/over effect 各为显式空字符串。不能删除空 token，不能因为空就补一个猜测路径。
- 文件最后第 184 行 `[using random skill] 1` 是顶层字段。它不是第四个 skill node 的参数。

`creature/ignis/effect/ignis_skill2_fire.act:3` 的大写 `[MOTION]` 内有 `[BASE ANI]` 单路径，`[SUB ANI]` 有五组路径与两个整数 `0 0`。这是叠加表现例子，结束标签为 `[/SUB ANI]` 和 `[/MOTION]`。不能把这些字段小写成 `.cre` 标签。

## 对白必须定位完整上下文

`creature/script/silverpig.wrd` 的 `[ambient]` 起于第 3 行，`[trigger]` 起于第 70 行。两者各有 `[room list]`、`[main game]`。相同标签在不同上下文代表不同触发位置。

- ambient/room list 第 6 至 8 行有三个 module 16 文本引用。`[in elven gard]` 第 10 行和 `[in alfhlyra]` 第 15 行另有区域条件文本。保留标签的原拼写 `gard`。
- ambient/main game 第 29 行 `[fill point under]` 接整数 `20` 和三个文本引用。整数是阈值候选，具体量表未证实。
- ambient/main game/enemies alive 第 38 行 `[hits over]` 接整数 `20` 与两段文本，第 44 行 `[hits under]` 接 `21` 与两段文本。不要把这些整数当对白条数。
- ambient/main game/enemies destroyed 第 54 行 `[rank over]` 和第 60 行 `[rank under]` 各接字符串 `b` 与两段文本。等级排序和边界是否含等号未知。
- `[pop random]` 全文出现 9 次。trigger/room list 的第一次在第 79 行接 `30` 并包住 `[call the name]`，第二次第 88 行接 `20` 并包住 `[equip]`。trigger/main game 的 `[equip]` 则在第 191 行，被第 189 行的另一个 `[pop random] 20` 包住。不能对 `[equip]` 做无上下文替换，`20` 与 `30` 是否百分率未知。

## 编辑步骤与未知项

先判断宠物使用顶层旧式字段还是 skill-list 节点。只修改目标节点或目标对白条件块。伤害改 `.atk`，表现改 `.ani/.act` 引用，文本改 `creature/creature.kor.str` 中现有键的值。内联 ``<16::key`display`>`` 只编译 module 与 key，display 改动不生效。保留 `%d`、`%%%%` 等原格式占位符。

保留 CRLF、TAB、字面文件头和各 token 类型。本文用空格描述的元组不是可直接覆盖的脚本。只引用原归档字符串表已有值。真实重建并重新提取核对字段，再分别验证普通技能、终结技能和城镇/地下城对白。`--verify` 只验证源归档往返。

本页未证实冷却单位、piercing 四列、int-data 八列、level-values 插值方式及随机触发权重。没有运行时证据时，保留原值。

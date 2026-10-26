# 场景机关与可交互对象修改手册

供修改障碍、可破坏物和陷阱的代理使用。本页读取瓶子、沙栅栏、压力地雷和雨滴对象，并追到地雷的两个动作。路径均相对 `output`。画面资源、碰撞配置与机关行为分别核查。

## 对象入口与基础字段

`passiveobject/passiveobject.lst:2` 的 `8843` 对应 `ActionObject/BreakableObject/bottle.obj`，`8374` 对应 `ActionObject/Trap/MinePressure.obj`。同编目还有 `340` 对应 `MapObject/Trap/MinePressure.obj`。后者属于另一目录，不能因文件名相同替换。

- `passiveobject/actionobject/breakableobject/bottle.obj:3` 的 `[width] 58 20` 是整数二元组。第 5 行 `[floating height] 0` 是单整数。几何轴和单位未确认。
- 第 7 行 `[layer]` 为 `` `[normal]` ``，第 9 行 `[pass type]` 为 `` `[do not pass]` ``，第 11 行 `[piercing power] 0`。阻挡和穿刺的关系是推断，不能把 0 理解成完全无碰撞。
- 第 13 行 `[basic action]` 为 `Action/bottle.act`。`passiveobject/actionobject/breakableobject/action/bottle.act:3` 的 `[MOTION]` 内只有 `[BASE ANI]` 引用 `../Animation/bottle.ani`。该动作没有本样本可见的触发器。
- 对象第 15 行 `[hp max] 2000`、第 17 行 `[hp destroy] 1` 各为单整数。前者可推断为耐久上限，后者的阈值或开关语义未确定。第 19 行名称引用显示布万加冰块，与文件名 bottle 不同，因此应按地图实际引用辨认对象。
- `passiveobject/actionobject/obstacle/sandfence1.obj:3` 宽度为 `100 36`，第 9 行同样是 `` `[do not pass]` ``，但第 11 行直接用 `[basic motion] Animation/SandFence1.ani`，文件没有 hp 字段。不能从 obstacle 目录推断所有障碍可破坏。
- `passiveobject/mapobject/particlefactory/raindrop.obj:3` 的 `[string data]` 只有 `Particle/RainDrop.ptl`，第 7 行 `[int data]` 有三整数 `8000 0 1`。它没有 width、hp 或动作块。三列语义不明，不能把第一项当雨滴数量或毫秒。

## 地雷动作与嵌套触发

`passiveobject/actionobject/trap/minepressure.obj` 共 22 行。第 5 行 `[layer]` 为 `` `[bottom]` ``。第 11 行 `[basic action]` 引用 `Action/MineStay.act`，第 13 至 15 行 `[etc action]` 列表仅含 `Action/MineActive.act`。第 17 行 `[attack info]` 引用 `AttackInfo/MinePressure.atk`。第 19 行 `[destroy particle]` 为 `Particle/MinePressureDestroy.ptl`。

- `passiveobject/actionobject/trap/action/minestay.act:13` 的 `[TRIGGER]` 内用 `[WHICH]`、`[MONSTER]` 指定检查对象。`[CHECKUP]` 内 `[IS INDEX] 56506` 为整数引用候选，`[DISTANCE]` 后是 `[<] 150`。距离单位和 56506 的怪物定义尚未核对。
- 同动作第 31 行 `[CHECKED NO]` 后是 `[>] 0`，再由 `[DO BEHAVIOR] [ME] 0` 选择行为。第 41 行 `[BEHAVIOR]` 内 `[SET ACTION] [CUSTOM] 0 [NOW]` 按名称推断为立即切到自定义动作 0。与 `.obj` 仅有一个 etc action 的结构相容，索引基准未由引擎证实。
- `passiveobject/actionobject/trap/action/mineactive.act:17` 的第一个 `[TRIGGER]` 内 `[FRAME] 1 1`，再次检查 `[IS INDEX] 56506`，再用 `[CHECKUP OBJECT] 0`。不要将它改成第二个 trigger 的 `[ME] 1`。
- 第一个 `[BEHAVIOR]` 第 43 至 55 行是 `[RESTORE] [HP] -20 [%]`，随后 `[SEND MESSAGE] [ATTACK_COMMAND] 4`。`[%]` 是明确观察到的标签，支持相对百分量的推断，但恢复负值的运行时伤害机制未验证。
- 第二个 `[TRIGGER]` 在第 57 行，同样有 `[FRAME] 1 1`，但行为目标是 `[ME] 1`。第二个 `[BEHAVIOR]` 第 67 行含 `[CREATE PASSIVEOBJECT]`，内部 `[INDEX] 8901`、`[PARTICLE FILENAME]` 空字符串、`[LEVEL] 60`、`[POS] 0 0 0`。编目将 8901 映射为 `ActionObject/Common/FlameBomb.obj`。创建块之后是 `[DESTROY]`。
- `passiveobject/actionobject/trap/attackinfo/minepressure.atk:3` 只有 `[damage reaction]` 和 `[none]`，没有伤害值。实际行为还包括动作里的 HP 修改和创建子对象，不能仅改 `.atk` 宣称改好地雷伤害。

## 修改步骤与未确认项

调整耐久先确认目标具有 `[hp max]`。调整触发距离只改 MineStay 的 CHECKUP/DISTANCE 整数。调整爆炸对象先沿 8901 查编目，不把 `.obj` 本身的攻击入口当完整行为。动作中的同名 trigger 必须以出现次序和目标字段定位。

保留字面 `#PVF_File\r\n`、CRLF、TAB、原 token 类型和所有嵌套结束标签。本文元组使用空格展示，不能原样覆盖。新字符串和新路径不能超出源归档字符串表。真实重建并重新提取，再在引用该对象的地图分别验证阻挡、受击破坏、触发范围和生成行为。`--verify` 不验证修改后的 output。

本页未证实碰撞尺寸单位、CUSTOM 索引解释、雨滴三列和地图对象的具体放置点。未追到地图引用时，不保证改动会出现在目标场景。

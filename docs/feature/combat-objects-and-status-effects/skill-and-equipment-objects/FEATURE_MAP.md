# 技能、怪物与装备生成对象修改手册

供修改已有被动对象的代理使用。已读取擒月炎对象与攻击定义，以及装备光束的 `.obj`、`.act`、`.atk`。路径均相对 `output`。维护者要分别定位对象编目、动作时序和伤害定义。

## 先查编号，再查引用

`passiveobject/passiveobject.lst:2` 是整数与路径连续交替的编目。`21014` 对应 `Character/Fighter/GrabExplosion.obj`，`48229` 对应 `EquipmentPassiveObject/power_beam.obj`。实际文件分别为 `passiveobject/character/fighter/grabexplosion.obj` 和 `passiveobject/equipmentpassiveobject/power_beam.obj`。名称相同不证明调用相同，先用生成处的对象编号确认目标。

## 对象字段与路径形态

- `grabexplosion.obj:3` 的 `[floating height] 1` 是单整数。第 5 行 `[layer]` 为字符串 `` `[normal]` ``。高度单位和完整层级枚举未知。
- 第 7 行 `[pass type]` 为 `` `[pass all]` ``。第 9 行 `[piercing power] 1000` 是单整数。穿越与穿刺是按名称推断的语义，1000 不能当作百分比。
- 第 11 行 `[basic motion]` 接 `../../Common/Animation/FireExplosion.ani`。该相对路径跨回公共资源，替换前检查所有共享调用者。
- 第 13 行 `[attack info]` 只有一个路径 `AttackInfo/GrabExplosion.atk`，没有 `[/attack info]`。不要照搬 creature 的带结束标签列表。
- 第 15 至 17 行 `[string data]` 是四个 `.ptl` 路径，按序为 `FireExplosionParticle1.ptl` 至 `FireExplosionParticle4.ptl`，前缀都是 `../../Common/Particle/`。序号的运行时用途未跟踪，不增减项。
- 第 19 行 `[name]` 接 module 9 的 `name_4135`，显示为擒月炎的爆炸。显示文字不等于伤害定义。
- `power_beam.obj:3` 的 `[width]` 为两个整数 `0 0`，第 7 行 `[piercing power]` 为 `99999`。零宽度不证明没有伤害判定。
- 光束第 9 行 `[basic action]` 引用 `Action/power_beam.act`，第 11 行 `[attack info]` 引用 `attackinfo/power_beam.atk`。这里走动作入口，不是 `[basic motion]`。

## 动作内的时序

`passiveobject/equipmentpassiveobject/action/power_beam.act` 共 27 行。`[MOTION]` 第 3 至 11 行内，`[BASE ANI]` 引用 `../Animation/power_beam_0.ani`，`[SOUND]` 为字符串 `PATRIS_BOW_LIGHTNING` 和整数 `0`，并有独立结束标签。

第 13 至 21 行是 `[TRIGGER]`。其中 `[FRAME] 3 3` 是两个整数，按名称推断是帧区间，端点是否含等号未知。`[DO BEHAVIOR]` 后的 `[ME] 0` 指向行为候选。第 23 至 27 行唯一 `[BEHAVIOR]` 内是无参数 `[DESTROY]`。修改消失时机应定位这组 trigger 和 behavior，不把 `[FRAME]` 当持续毫秒。

## 攻击定义及重复标签

- `passiveobject/equipmentpassiveobject/attackinfo/power_beam.atk:3` 的 `[damage] 1000` 与第 5 行 `[damage bonus] 10` 各为单整数。缩放和叠加方式未证实。
- 第 7 行 `[attack type]` 后是无值 `[magic]`。第 11 行 `[weapon damage apply] 1` 与第 13 行 `[attack enemy] 1` 是单整数。
- 第 15 行 `[elemental property]` 后是 `[light element]`。第 19 行 `[damage reaction]` 后再次出现无值 `[damage]`。只改第一个有值 damage，不全局替换。
- 第 23 行标签实际拼作 `[knuck back]`，值 `0`。第 25、27 行 `[push aside] 200`、`[lift up] 50`。保留原拼写，距离单位未证实。
- 第 39 行 `[no blood] 10 1.0` 为整数与浮点二元组。第 41 行 `[active status]` 是字符串 `` `[lightning]` `` 加四整数 `100 5 10000 100`。四列各自含义未明，不能同时称为概率、等级、毫秒和伤害。
- `passiveobject/character/fighter/attackinfo/grabexplosion.atk` 共 30 行，含 `[magic]`、`[fire element]`、`[weapon damage apply] 1`，但没有有值 `[damage]`。这说明伤害可依赖调用处，不能为补齐模板而新增 damage。

## 实用修改流程

先用对象 ID 找 `.obj`，再沿现有动作和攻击路径定位修改点。伤害改有值攻击参数，时序改动作 trigger，表现改动画或粒子引用。共享资源的修改需记录可能影响的其他对象。

保留 `#PVF_File\r\n`、CRLF、TAB 与原 token 类型。本文空格元组不能直接覆盖脚本。编译只用源归档字符串表，不新造标签、字符串或路径。真实重建后重新提取对象及依赖，并用原生成技能或装备验证命中和消失。`--verify` 只查源归档往返，不验证修改。

未知项包括状态四列、穿刺尺度、武器伤害公式和生成端注入参数。遇到无伤害字段的对象先追调用者，不猜补字段。

# 投掷物与爆炸对象修改手册

供调整已有炸弹和地雷对象的代理使用。已读取 Bomb、BombMine4、FlyBomb、CurseBombSub1 及 Bomb 和 BombMine 攻击文件。路径均相对 `output`。投掷入口、生成对象与命中表现需要分别追踪。

## 编目存在共享路径

`passiveobject/passiveobject.lst:2` 的 50100、50101、50102、50103、50104 全部指向 `ThrowItem/Bomb.obj`。修改该文件可能影响五个对象 ID，实际差别可能由调用者提供，后者尚未核查。编号 50004 对应 `ThrowItem/BombMine4.obj`。当前没有名为 `passiveobject/throwitem/bombmine.obj` 的文件，不要按名称新建。

## 飞行对象参数

- `passiveobject/throwitem/bomb.obj:3` 的 `[width] 1 1` 为整数二元组，第 5 行 `[floating height] 1` 为单整数。轴与单位不明。
- 第 7 行 `[layer]` 为 `` `[normal]` ``，第 9 行 `[pass type]` 为 `` `[pass all]` ``，第 11 行 `[piercing power] 5000`。穿透尺度未知，5000 不可直接解释为概率。
- 第 13 行 `[basic motion]` 为 `Animation/BombFly.ani`，第 15 至 17 行 `[etc motion]` 列表只有 `Animation/BombLand.ani`。两者按名称提示飞行与落地表现，实际切换条件不在此文件。
- 第 19 行 `[attack info]` 为单路径 `AttackInfo/Bomb.atk`。第 21 行 `[name]` 引用 module 9 的 `name_6400`，显示爆弹、轰爆弹。共用名称不是两个独立参数组。
- `passiveobject/throwitem/flybomb.obj:11` 的 `[piercing power] -100` 证明该字段存在负值。第 15 行 `[destroy particle]` 为 `Particle/FlyBombPiece.ptl`。第 19 至 21 行 `[int data]` 有两整数 `50590 0`，未证实第一列是子对象 ID，不要按正值范围校正。
- `passiveobject/throwitem/cursebombsub1.obj:13` 的 `[etc motion]` 有四个路径，公共目录前缀为 `../Common/Animation/`，依次为 `CurseBombSub1.ani` 至 `CurseBombSub4.ani`。第 17 行 `[string data]` 是两个命中粒子路径。二者条数不同，不能假定逐列一一配对。

## 攻击字段及无伤害样本

`passiveobject/throwitem/attackinfo/bomb.atk` 全部 34 行中，第 3 行 `[damage] 60` 是有值伤害。第 15 行 `[damage reaction]` 后第 17 行无值 `[damage]` 是枚举位置，不能同改。

- 第 5 行 `[attack type]` 后是 `[physic]`，第 9 行 `[attack enemy] 1` 是单整数。
- 第 11 行 `[elemental property]` 后是 `[no element]`。第 25 行 `[attack direction]` 后是 `[hit horizon]`。保留枚举的独立标签格式。
- 第 19 行 `[push aside] 50`、第 21 行 `[lift up] 50` 各为单整数。击退与浮空的解释来自名称，单位未知。
- 第 23 行 `[hit wav]` 是字符串 `R_BOMB_HIT`。第 29 行 `[hit info]` 后为 `[blow]`。
- 第 33 行 `[no blood] 150 1.0` 是整数与浮点二元组。没有证据将这两列解释为出血概率和倍率。

`passiveobject/throwitem/bombmine4.obj:7` 的 `[layer]` 为 `` `[bottom]` ``，第 11 行 `[piercing power] 0`，第 13 行基本动作为 `Animation/BombMineReady.ani`，第 15 行列表是 `Animation/BombMineActive.ani`。第 19 行引用 `AttackInfo/BombMine.atk`，但该攻击文件全部 5 行只含 `[damage reaction] [none]`。对象第 23 至 25 行 `[int data] 40002 1035` 是整数对。编目中 40002 恰对应 `Common/FireExplosion.obj`，这支持子对象引用的推断，第二列 1035 的意义和调用方式仍未知。不能把 BombMine.atk 里不存在的 damage 凭空补上。

## 修改步骤

先确认投掷物使用的对象 ID。记录同路径的其他 ID，再调整已有有值伤害或现有资源引用。需要改爆炸时追实际生成对象，不把飞行图像当伤害。对 int-data 的第二列缺乏证据时保留原值。

保存原文件头 `#PVF_File\r\n`、CRLF、TAB 和 token 类型。本文空格元组不是覆盖模板。只使用源归档已有字符串、标签和路径。需要真实重建并重新提取对象和攻击定义，再分别验证飞行、落地、爆炸和多个共用 ID。`--verify` 仅查源归档往返。

投掷物品到对象的上游映射、落地切换机制、穿刺尺度和地雷 int-data 的实际读取方式尚未核查。

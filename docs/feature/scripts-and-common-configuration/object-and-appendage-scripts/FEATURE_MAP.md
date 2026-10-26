# 对象与附加状态脚本功能索引

被动对象和附加状态的 Squirrel 实现分组。

## 功能范围

- 被动对象脚本。
- 附加状态脚本及其与角色脚本的边界。

## 分类依据

sqr 下独立区分 passiveobject 与 appendage，功能对象定义和附加状态定义仍分别归入战斗对象分类。

## 定位与样本

被动对象脚本先从职业加载入口的 pushPassiveObj 反查，附加状态脚本则核对实际添加它的代码。本文读了 `output/sqr/passiveobject/character/priest/po_devilstrike_attack1.nut` 和 `output/sqr/appendage/character/ap_atmage_bodyeffect.nut`。

## 参数项与作用

下列字段的拼写、值形状和位置已经从样本读取。除明确写出代码证据的项目外，游戏作用由标签名和相邻数据推断，尚未经过实机验证。

- `setCustomData_po_DevilStrike1`。接收创建对象时的自定义数据。
  证据为 `output/sqr/passiveobject/character/priest/po_devilstrike_attack1.nut:4`，源代码为 ``function setCustomData_po_DevilStrike1(obj,reciveData)``。
  本函数从 reciveData 读取一个 Dword，再传给当前攻击信息。发送端字段顺序必须一致。

- `local rate = reciveData.readDword()`。读取伤害修正参数。
  证据为 `output/sqr/passiveobject/character/priest/po_devilstrike_attack1.nut:6`，源代码为 ``local rate = reciveData.readDword(); // 공격력(%)``。
  证据是该值直接传入 sq_SetCurrentAttackBonusRate，具体缩放分母应查引擎 API，不因变量名 rate 就认定是百分数。

- `sq_SetCurrentAttackBonusRate(pAttack, rate)`。修改当前攻击信息的 bonus rate。
  证据为 `output/sqr/passiveobject/character/priest/po_devilstrike_attack1.nut:9`，源代码为 ``sq_SetCurrentAttackBonusRate(pAttack, rate);``。
  不要误改固定攻击力字段，调用目标是当前攻击对象而不是角色面板。

- `if(bEnd)`。动画结束时进入销毁分支。
  证据为 `output/sqr/passiveobject/character/priest/po_devilstrike_attack1.nut:34`，源代码为 ``if(bEnd) {``。
  实际销毁还受 isMyControl 判断限制。移除该条件可能导致多端重复发送。

- `appendage.sq_AddFunctionName("onStart"`。注册附加状态的启动回调。
  证据为 `output/sqr/appendage/character/ap_atmage_bodyeffect.nut:9`，源代码为 ``appendage.sq_AddFunctionName("onStart", "onStart_appendage_atmage_bodyeffect")``。
  回调字符串必须与函数声明一致；该文件还注册 proc、prepareDraw、onEnd、drawAppend 与 isEnd。

- `APPENDAGE_INDEX_STATE <- 0`。状态存储使用向量位置 0。
  证据为 `output/sqr/appendage/character/ap_atmage_bodyeffect.nut:2`，源代码为 ``APPENDAGE_INDEX_STATE <- 0``。
  APPENDAGE_INDEX_ISEND 为位置 1，onStart 连续 push_vector 两次初始化。改索引需同步所有读写。

- `local startT = 150`。默认透明度插值的起始值。
  证据为 `output/sqr/appendage/character/ap_atmage_bodyeffect.nut:90`，源代码为 ``local startT = 150;``。
  证据是 startT 与 endT 经 sq_GetUniformVelocity 后传给 sq_ALPHA。它虽然名为 startT，却不是已证实的起始时间。

- `local endT = 250`。默认透明度插值的目标值。
  证据为 `output/sqr/appendage/character/ap_atmage_bodyeffect.nut:91`，源代码为 ``local endT = 250;``。
  特定技能与 state 分支会覆盖该默认值，不能只改默认值就认为所有技能改变。

- `local effectT = 500`。透明度插值的时长参数。
  证据为 `output/sqr/appendage/character/ap_atmage_bodyeffect.nut:92`，源代码为 ``local effectT = 500;``。
  值传入 sq_GetUniformVelocity，时间单位依赖引擎，未在仓库确认。

- `local rgb = sq_RGB(0, 90, 255)`。构造默认效果颜色。
  证据为 `output/sqr/appendage/character/ap_atmage_bodyeffect.nut:94`，源代码为 ``local rgb = sq_RGB(0, 90, 255);``。
  三个实参为颜色构造函数输入；技能分支可能改成白色。改色要核对实际命中的分支。

## 修改步骤

1. 先把创建端写入的数据与对象读取端逐项配对，确认对象绑定 ID。
2. 编辑回调或效果时同时检查注册、向量初始化、分支覆盖及生命周期清理。
3. 回包并实机检查命中、动画结束、父对象消失、技能取消以及其他客户端观察结果。

## 未确认与验证

不得根据 startT 的变量名把它解释成时间。本页语义来自实际数据流。Dword 的有符号解释、API 时间单位及伤害倍率分母仍需引擎证据。

回包前后应比较实际目标条目的反编译结果。回包成功只证明编码成功，实机检查仍需覆盖本页所述功能。通用编码与回包限制见总索引。

# 脚本加载与状态注册功能索引

Squirrel 脚本入口、公共定义和职业状态加载。

## 功能范围

- 脚本加载入口及公共枚举和函数。
- 职业状态加载与角色脚本分组。

## 分类依据

已读取 loadstate 中的 sq_RunScript 调用，另可见 init_character、dnf_enum_header、common 和角色加载条目。

## 定位与样本

这些 `.nut` 是原样导出的 Squirrel 源码，不带 #PVF_File。源文件注释含非 UTF-8 字节，编辑时应识别并保留原始编码，不能套用反编译脚本的 UTF-8 保存方式。先从 `output/sqr/loadstate.nut` 追踪加载链。

## 参数项与作用

下列字段的拼写、值形状和位置已经从样本读取。除明确写出代码证据的项目外，游戏作用由标签名和相邻数据推断，尚未经过实机验证。

- `sq_RunScript("dnf_enum_header.nut")`。先加载枚举定义。
  证据为 `output/sqr/loadstate.nut:3`，源代码为 ``sq_RunScript("dnf_enum_header.nut");``。
  这是加载调用的代码证据，路径属于 sqr 运行环境，不是系统绝对路径。

- `sq_RunScript("common.nut")`。加载公共回调。
  证据为 `output/sqr/loadstate.nut:4`，源代码为 ``sq_RunScript("common.nut"); //``。
  本文件有顺序，新增调用前必须确认依赖定义已加载。

- `//sq_RunScript("Character/common_load_state.nut")`。该加载语句已注释。
  证据为 `output/sqr/loadstate.nut:12`，源代码为 ``//sq_RunScript("Character/common_load_state.nut"); // 공통스킬 nut파일 로딩``。
  文件存在不等于当前会加载。不能把注释行算作生效入口。

- `CNAvenger.pushState("Character/Priest/Spincutter.nut"`。注册一个职业状态脚本。
  证据为 `output/sqr/character/avenger_load_state.nut:7`，源代码为 ``CNAvenger.pushState("Character/Priest/Spincutter.nut", "spincutter", STATE_SPINCUTTER, SKILL_SPINCUTTER);``。
  样本实参依次为脚本路径、函数后缀 spincutter、STATE_SPINCUTTER、SKILL_SPINCUTTER。各枚举数值要到头文件核对。

- `CNAvenger.pushState("Character/Priest/DashAttack.nut"`。样本也注册了不对应技能的动作状态。
  证据为 `output/sqr/character/avenger_load_state.nut:14`，源代码为 ``CNAvenger.pushState("Character/Priest/DashAttack.nut", "DashAttack", STATE_DASH_ATTACK, -1);``。
  第四参数为 -1，证明不能把全部注册都强制写成有效技能 ID。

- `CNAvenger.pushPassiveObj("PassiveObject/Character/Priest/po_devilstrike_attack1.nut"`。把被动对象脚本绑定到对象 ID 24104。
  证据为 `output/sqr/character/avenger_load_state.nut:31`，源代码为 ``CNAvenger.pushPassiveObj("PassiveObject/Character/Priest/po_devilstrike_attack1.nut", 24104); // 24104	`Character/Priest/DevilStrike1.obj`	// 어벤저 - 데빌스트라이커 공격1``。
  修改对象 ID 要同时核对 passiveobject 列表和调用该对象的代码。

- `obj.sq_JumpUpStartFrame(1)`。为职业初始化跳起动画起始帧。
  证据为 `output/sqr/init_character.nut:11`，源代码为 ``obj.sq_JumpUpStartFrame(1);``。
  同块还设置下降和落地帧。帧数必须与该职业动画匹配。

## 修改步骤

1. 确认目标脚本在未注释的加载链中，并解析相关 STATE、SKILL 和对象 ID。
2. 只在现有源文件中修改已定位的注册或参数，保留原字节编码。新文件不会由当前打包器收入封包。
3. 静态核对函数后缀和回调命名，回包后实机检查职业创建、技能施放和状态结束。

## 未确认与验证

本地没有 Squirrel 编译器或游戏引擎执行环境，不能仅靠语法外观保证引擎 API 正确。原样文件中的新字符串不受 ScriptText 字符串表检查，但新资源路径仍必须在封包或客户端中存在。

回包前后应比较实际目标条目的反编译结果。回包成功只证明编码成功，实机检查仍需覆盖本页所述功能。通用编码与回包限制见总索引。

# 独立 pet 系统修改手册

供维护旧 pet 定义的代理使用。已读取 `pet/pet.lst`、`pet/falcon/falcon.pet` 全部 30 行和 `pet/falcon/attackinfo/tackle.atk` 全部 34 行。路径均相对 `output`。本系统只有本次编目中的 Falcon 样本，不能套用 creature 的成长字段。

## 编目与资源

`pet/pet.lst:2` 只有一对 `1` 与 `Falcon/Falcon.pet`。实际提取文件为小写 `pet/falcon/falcon.pet`。ID 1 属于 pet 编目，不是 `creature/creature.lst` 的 ID 1。`.pet` 没有本样本可见的经验表、artifact slot 或 evolution 块。

## 定义参数

- `.pet:3` 的 `[width]` 接两个整数 `16 8`。它保留双值，轴与单位未知。
- 第 5 行 `[floating height] 80` 与第 13 行 `[gravity] 0` 各为单整数。按名称可推断为悬浮和重力参数，不能确认 80 为像素。
- 第 7 行 `[layer]` 接字符串 `` `[normal]` ``。第 11 行 `[direction correct] 1` 是单整数，朝向修正是推断。
- 第 9 行 `[recovery time] 5000` 是单整数。这里没有 `[skill recovery time]`，不能改写成 creature 标签。恢复时间的单位未知。
- 第 15 行 `[basic motion]` 接 `Animation/Rest.ani`。第 17 至 19 行 `[etc motion]` 是带结束标签的单路径列表 `Animation/Tackle.ani`。分别对应 `pet/falcon/animation/rest.ani` 和 `pet/falcon/animation/tackle.ani`。
- 第 21 至 23 行 `[attack info]` 是单路径列表 `AttackInfo/Tackle.atk`，对应现有 `pet/falcon/attackinfo/tackle.atk`。
- 第 25 至 27 行 `[int data]` 是四整数 `700 -80 500 100`。负数是有效观察值，四列的含义未明，不能全转为无符号数或根据浮空高度猜位移。
- 第 29 行 `[name]` 接 module 10 的 `name_6505` 引用。显示文本在当前提取中为 `笝錍`，不能仅据此认定正确中文名。`pet/pet.kor.str:12` 同样为 `name_6505>笝錍`。改名应先核对原编码，不修改内联显示段来冒充生效。

## 攻击参数与重复标签

- `pet/falcon/attackinfo/tackle.atk:3` 的 `[damage]` 接整数 `100`。第 17 行再次出现无值 `[damage]`，它位于 `[damage reaction]` 后，属于反应枚举位置。两个同名标签不能全局数值替换。
- 第 5 行 `[attack type]` 后是无值 `[physic]`。第 9 行 `[attack enemy] 1` 是单整数，不能把它当攻击力。
- 第 11 行 `[elemental property]` 后是 `[no element]`。第 23 行 `[attack direction]` 后是 `[hit horizon]`。这些枚举保留原拼写和无值形态。
- 第 19 行 `[push aside] 100` 和第 21 行 `[lift up] 30` 各为单整数。击退和浮空含义是名称推断，单位未知。
- 第 27 行 `[hit wav]` 接字符串 `FALCON_HIT`。第 29 行 `[hit info]` 后是 `[blow]`。声音键与命中类型不等价。
- 第 33 行 `[no blood]` 接二元组 `100 1.0`。首项为整数，次项为浮点，不能断定两项都是概率或持续时间。

## 修改与核查

从 pet 编目定位现有条目，记录目标是定义、攻击还是表现。改基础攻击力只改 `.atk` 第一个有值 `[damage]`。改恢复只改 `.pet` 的 `[recovery time]`。改动作先核对路径实际存在并属于原字符串表，保留列表结束标签。

保持 `#PVF_File\r\n`、CRLF 和 TAB，保留整数、浮点与字符串原 token 类型。本文空格样例不是直接覆盖文件。实际重建后重新提取这两个文件并比较，再在旧 pet 的真实入口验证。`--verify` 不验证修改后的 output。

本页未找到运行时创建 pet 的调用点。是否仍能通过当前客户端正常进入旧系统尚不明。未确认的四列 int-data 和 `[no blood]` 二元组不提供安全改值方案。

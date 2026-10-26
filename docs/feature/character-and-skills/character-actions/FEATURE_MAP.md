# 角色动作与攻击判定修改手册

## 入口与格式边界

角色攻击样本是 `character/swordman/attackinfo/ashenfork.atk`。公共动作样本是 `character/common/action/booster_particle.act`。前者为 25 行脚本，后者为 11 行脚本。它们分别说明攻击参数和动画组合，不代表整个动作系统只有这些字段。

`character/common/animation/booster_particle_0.ani` 实测为 266 字节二进制。头 16 字节为 `06 00 01 00 33 00 00 00 43 68 61 72 61 63 74 65`，没有 `#PVF_File`。其中可见 `Character/Common/FallingEffect/falling_particle.img` 字节串。不能把该 `.ani` 当文本覆盖，也不能凭可见路径推导帧结构。

## 攻击脚本字段

- `[attack type]` 后是无值的 `[physic]`，见 `character/swordman/attackinfo/ashenfork.atk:3` 到第 5 行。这是标签选择，不是反引号字符串，也没有数字枚举。
- `[weapon damage apply]` 后有整数 `1`，见 `character/swordman/attackinfo/ashenfork.atk:7`。名称提示是否应用武器伤害。`0` 的行为和其他合法值未从本样本确认。
- `[attack enemy]` 后有整数 `1`，见 `character/swordman/attackinfo/ashenfork.atk:9`。名称提示敌对目标控制，不能推断它能覆盖友军和中立目标的所有规则。
- `[elemental property]` 后是无值 `[no element]`，见 `character/swordman/attackinfo/ashenfork.atk:11`。改属性前必须从同类真实 `.atk` 找到已有标签，不能写中文或自造枚举。
- `[damage reaction]` 后是无值 `[down]`，见 `character/swordman/attackinfo/ashenfork.atk:15`。名称提示倒地反应，不等于攻击方向。
- `[push aside]` 后有整数 `270`，`[lift up]` 后有整数 `180`，见 `character/swordman/attackinfo/ashenfork.atk:19` 到第 22 行。名称提示横向推开和抬升，距离或速度单位未确认。
- `[attack direction]` 后是 `[hit down]`，见 `character/swordman/attackinfo/ashenfork.atk:23`。它与 `[damage reaction]` 是两个独立选择，不要全文替换所有含 down 的标签。

## 动作组合字段

- `[MOTION]` 和 `[/MOTION]` 包住动作块，见 `character/common/action/booster_particle.act:3` 到第 11 行。大小写属于原标签。
- `[BASE ANI]` 后为单个反引号路径 `../Animation/booster_particle_0.ani`，见 `character/common/action/booster_particle.act:5`。按相对路径解析，对应上述二进制文件。
- `[SUB ANI]` 后有七组三 token，每组为路径与两个整数，见 `character/common/action/booster_particle.act:7` 到第 9 行。第一组是 `../Animation/booster_particle_1.ani 0 1`，末组是 `../Animation/booster_particle_7.ani 0 7`。第二列均为 0，第三列递增。不能据此认定它们是帧号或层号。

## 修改步骤

1. 先确定技能或角色实际调用的 `.atk` 和 `.act`。文件存在不等于当前技能使用它。本样本没有提供调用入口，不能声称修改必然影响某一招。
2. 只调整已定位攻击脚本的单个整数。以 `push aside` 为例，保留整数 token 和所在攻击文件，不改 `lift up`。
3. 动画路径只能复用原归档已有字符串。保留 `.act` 的相对路径、三 token 分组和大小写。二进制 `.ani` 的布局未解释，不能安全文本编辑。
4. 保存脚本的 CRLF、TAB 与 `#PVF_File\r\n`。Markdown 中的空格不是文件分隔符。
5. 核对修改块的 token 类型和子动画条目数。重建并提取检查，再实机检查击倒、推开、浮空及动画组合。`--verify` 不能验证修改后的动作。

## 未知项

未确认整数的物理单位、布尔合法域、动作三元组列义和 ANI 二进制协议。未确认攻击脚本是否还受技能级别数据覆盖。需先取得调用链证据再扩大改动。

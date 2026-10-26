# 套装与称号修改手册

## 入口与关联

装备中的 `[part set index]` 指向 `etc/equipmentpartset.etc` 的编号块。样本时装 `equipment/character/swordman/avatar/coat/101500528.equ:13` 为 `2`，对应 `etc/equipmentpartset.etc:3` 下的 `character/partset/upperset.equ`。路径相对 equipment，输出文件为 `equipment/character/partset/upperset.equ`。

本页还读了 `equipment/character/partset/2choroset1.equ`、`equipment/character/partset/bluefootprint.equ`、`equipment/character/common/title/event_adult_girl.equ`、`etc/titlebook.etc` 的开头奖励段与 `equipment/character/swordman/growtype/weaponmaster.equ`。套装能力、称号物品、称号簿和转职外观分别定位。

## 套装参数

- `[equipment part set]` 在 `etc/equipmentpartset.etc:27` 的块以整数 `10`、路径 `character/partset/2choroset1.equ` 开头，后接本地化名称和部位字符串、两个整数。该块含 `[amulet]`、`[wrist]`、`[ring]`、`[coat]` 等九个部位。不要把部位后 `0 0` 擅自改成装备 ID。
- `[set name]` 在 `equipment/character/partset/upperset.equ:3` 为普通字符串 `高级装扮套装`，但 `equipment/character/partset/2choroset1.equ:3` 是本地化引用。两类字符串 token 不可互换。新名称还受原归档字符串表限制。
- `[piece set ability]` 在 `equipment/character/partset/upperset.equ:5`、第 17、29 行分别以整数 `3`、`5`、`8` 开头，并各有结束标签。名称支持件数门槛解释，实际是否累计叠加还需客户端确认。
- 三件块 `[physical attack]`、`[physical defense]`、`[magical attack]`、`[magical defense]` 均为整数 `10`，见 `equipment/character/partset/upperset.equ:7` 到第 14 行。八件块第 31 到 38 行再次出现这些字段，改三件不能全文替换八件。
- 五件块 `[HP MAX]`、`[MP MAX]` 各为 `100`，`[inventory limit]` 为 `6000`，`[MP regen speed]` 为 `5`，见 `equipment/character/partset/upperset.equ:19` 到第 26 行。重量与恢复单位未确认。
- 八件块 `[room list move speed rate]` 为浮点 `0.10000000149011612`，见 `equipment/character/partset/upperset.equ:45`。该 rate 与前面整数速度值形状不同，不能统一乘除 100。
- 勇者套装 `equipment/character/partset/2choroset1.equ:6`、第 17、28 行的块头是 `2`、`4`、`6`，而说明键名含 partset3、partset6、partset9。实际整数与键名数字不同，不能按键名修正门槛。
- 勇者套装首块 `[skill data up]` 在 `equipment/character/partset/2choroset1.equ:8` 以七 token `[swordman] 8 [dungeon type] [cooltime] 0 + -1200` 开头。后续组改 `[level]` 列 `0`、`1`、`2`，末尾 `% 20`。第 13 行说明对应三段斩冷却 `-1.2秒` 与攻击力 `+20%%`。这是该样本冷却数值按千分之一秒展示的证据，不推广到所有 time 字段。
- `equipment/character/partset/bluefootprint.equ:3` 只有 `[piece set ability] 8` 和内部 `[additional effect index] 2`。效果继续引用其他配置，不在本文件展开，不能凭文件名猜具体效果。

## 称号与称号簿

- `[equipment type]` 在 `equipment/character/common/title/event_adult_girl.equ:39` 为 `[title name] 1`。`[custom animation]` 第 35 行为 `TitleAnimation/event_adult_girl.ani` 字符串列表，不能把称号当普通时装上衣。
- 该称号 `[usable period]` 第 31 行为 `90`。期限单位没有文件声明，不能直接写九十天。
- 第一个 `[if]` 在 `equipment/character/common/title/event_adult_girl.equ:57` 内为 `[cooltime] 40000` 与 `[attack success] 1`。对应 `[then]` 第 65 行内含 `[target] myself -1`、`[duration] 20000`、`[probability] 2`，随后四次 `[stat]`，各为属性名、`+`、`20`。第 10 行说明写攻击或施放技能时有 `2%%` 几率、持续 20 秒，这为本文件 probability 与 duration 的展示单位提供依据。
- 第二个 `[if]` 在称号第 83 行，条件改为 `[casting] 1`。第 91 行开始的 `[then]` 另有一套相同数值。改攻击触发和改施法触发必须分别定位。是否共享冷却未确认。
- `[default reward]` 在 `etc/titlebook.etc:3` 内 `[hp max]` 与 `[mp max]` 均为字符串 `+` 加整数 `200`。这里标签小写，不是装备顶层 `[HP MAX]`。
- `[section]` 在 `etc/titlebook.etc:23` 为 `general`，其第一个 `[reward type]` 第 30 行内 `[hp max]` 为 `+ 150`、`[mp max]` 为 `+ 100`，第 54 行的第二个 reward type 又是 `+ 200`、`+ 150`。按 section、section icon 和 reward type 定位奖励，不能全文替换 hp max。
- `[title collection info]` 在 `etc/titlebook.etc:11`、第 15、19 行分别以 `general 70`、`specific 140`、`despair 100` 开头，含 `-1` 等不同长短记录。完整语法未确认，不能当固定两列称号列表编辑。

## 转职外观与修改步骤

`equipment/character/swordman/growtype/weaponmaster.equ:11` 的类型是 `[coat avatar] 0`，第 17 行 `[spectrum]` 为五整数 `255 255 255 150 200`，第 19 行 `[layer variation]` 为 `50 weaponmaster`。这份文件是有外观结构的转职装备，不能把 growtype 目录当作角色成长数值表。五列 spectrum 的完整含义未确认。

1. 从物品 part set index 追到套装路径，再按块头实际整数改目标件数组。保留其他件数块。
2. 改技能套装时查职业技能索引和数据列。改称号触发时明确攻击还是施法，保留 if、then 边界。
3. 改称号簿只动已定位奖励。未解释的收集长序列与外观 spectrum 不能安全重排。
4. 保留 CRLF、TAB、`#PVF_File\r\n` 与原类型。中文本地化值改 `.str` 原有键，普通字符串只能复用已有值。Markdown 空格不可覆盖源文件。
5. 核对套装门槛、重复奖励块、两组触发和引用 ID。需要真实重建、提取与客户端件数、触发、称号簿验证。`--verify` 不验证修改输出。

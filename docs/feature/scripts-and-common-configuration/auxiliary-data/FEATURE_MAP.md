# 技能与界面辅助数据功能索引

技能、界面辅助数据及公共占位条目。

## 功能范围

- 按职业区分的技能辅助数据。
- 界面辅助数据、测试数据和占位条目。

## 分类依据

data 下可见 skill 与 ui，另有 extern、test 和根目录占位条目。辅助数据的运行时用途尚未逐项确认。

## 定位与样本

辅助数据不是统一的任意列数组。本文读取的 `.sd` 带 #PVF_File，内部按 int、float、string 分开存放名称和值。`output/dummy.etc` 则只有文件头，没有可修改参数。

## 参数项与作用

下列字段的拼写、值形状和位置已经从样本读取。除明确写出代码证据的项目外，游戏作用由标签名和相邻数据推断，尚未经过实机验证。

- `[int]`。以字符串键和整数值交替保存的技能辅助参数。
  证据为 `output/data/skill/swordman.sd:3` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值节选为 `` `damh start frame` 3 `swa area offset` 146 `swa after delay` 500 `vs hit x offset` 121 `vs hit z offset` 80 `upper slash start frame` 3 `gss release delay` 500 `gss after delay` 500 ``。到下一个段落标签前共有 94 个制表符分隔值。
  样本 94 个值构成 47 个键值对。例如 damh start frame 为 3，swa area offset 为 146，swa after delay 为 500。缩写对应技能与时间单位未确认。

- `[float]`。以字符串键和浮点值交替保存的技能辅助参数。
  证据为 `output/data/skill/swordman.sd:7` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `saw eye init size` 0.5 `saw eye add size` 0.20000000298023224 `br typhoon start size` 0.44999998807907104 `br typhoon end size` 1.2999999523162842 ``。到下一个段落标签前共有 8 个制表符分隔值。
  样本四组键值，saw eye init size 为 0.5，saw eye add size 约 0.2。保留浮点 token 类型，不要按显示小数重排。

- `[string]`。字符串参数段。
  证据为 `output/data/skill/swordman.sd:11` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `空段落或后面直接进入子段落`。到下一个段落标签前共有 0 个制表符分隔值。
  本样本为空。空段不是允许新增任意键的证明，当前编译器仍要求键名已在源字符串表中。

- `[int]`。选项界面的整数辅助数据。
  证据为 `output/data/ui/option.sd:3` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值节选为 `` `menu window size x` 12 `menu window size y` 20 `set window size x` 18 `set window size y` 28 `key window size x` 22 `key window size y` 23 `menu window pos x` 243 `menu window pos y` 122 ``。到下一个段落标签前共有 128 个制表符分隔值。
  样本有 64 对键值。menu window pos x 为 243，pos y 为 122，size x 为 12、size y 为 20。尺寸数值与位置尺度不同，不能统一假设为像素。

- `[float]`。跨功能浮点修正参数。
  证据为 `output/data/extern.sd:3` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `pvp deathmatch attack power rate` 1.7999999523162842 `skill level data revision const` 0.8999999761581421 ``。到下一个段落标签前共有 4 个制表符分隔值。
  pvp deathmatch attack power rate 约 1.8，skill level data revision const 约 0.9。作用由键名推断，调用范围应先搜索使用方。

- `[int]`。按键名区分的死亡竞赛场景开关。
  证据为 `output/data/extern.sd:7` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `pvp deathmatch single play 50019` 0 `pvp deathmatch single play 50018` 1 ``。到下一个段落标签前共有 4 个制表符分隔值。
  两个键分别包含 50019 与 50018，值为 0 和 1。场景 ID 与开关含义需结合地图调用核对。

## 修改步骤

1. 按完整键名定位，先区分 int、float、string 段，不要只按相同的数字搜索替换。
2. 只改已有键对应的值，保留键值交替结构、类型和顺序。修改界面尺寸前检查其量纲与布局关联。
3. 回包后反编译目标 `.sd`，再测试对应技能、选项窗口或指定死亡竞赛场景。

## 未确认与验证

多数缩写键没有调用方说明。手册只给出可定位键和观测值，未知缩写、坐标系及尺寸单位不作扩展解释。dummy 不是放入新配置的通用入口。

回包前后应比较实际目标条目的反编译结果。回包成功只证明编码成功，实机检查仍需覆盖本页所述功能。通用编码与回包限制见总索引。

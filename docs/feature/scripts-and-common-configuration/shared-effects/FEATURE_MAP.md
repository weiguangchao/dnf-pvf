# 公共特效与表情资源功能索引

命中、状态、公共效果和角色表情表现。

## 功能范围

- 公共效果、命中特效和状态表现。
- 角色表情、情绪动作与公共移动表现。

## 分类依据

common 下可见 commoneffect、hiteffect、activestatus、emoticon、emotionexpression 和 transports。

## 定位与样本

本文读取了状态粒子 `output/common/activestatus/particle/badeffectparticle.ptl`。命中特效样本 `output/common/hiteffect/animation/age12/knocklarge.ani` 实测为 140 字节，文件头为 `03 00 01 00 1f 00 00 00 43 6f 6d 6d 6f 6e 2f 48`，不是 #PVF_File 文本。

## 参数项与作用

下列字段的拼写、值形状和位置已经从样本读取。除明确写出代码证据的项目外，游戏作用由标签名和相邻数据推断，尚未经过实机验证。

- `[creation pos]`。粒子创建位置参数。
  证据为 `output/common/activestatus/particle/badeffectparticle.ptl:3` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `355 320 20`。到下一个段落标签前共有 3 个制表符分隔值。
  三个整数 355、320、20，按字段名推断为空间坐标，坐标系、锚点及单位未确认。

- `[changing term]`。粒子属性变化周期参数。
  证据为 `output/common/activestatus/particle/badeffectparticle.ptl:5` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `1000`。到下一个段落标签前共有 1 个制表符分隔值。
  单整数 1000，时间单位未确认。

- `[changing type]`。属性变化方式枚举。
  证据为 `output/common/activestatus/particle/badeffectparticle.ptl:7` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `[keep last value]` ``。到下一个段落标签前共有 1 个制表符分隔值。
  样本是 `[keep last value]`，替换枚举必须是源字符串表已有名称并被该字段支持。

- `[life time]`。粒子存活时长参数。
  证据为 `output/common/activestatus/particle/badeffectparticle.ptl:11` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `1200`。到下一个段落标签前共有 1 个制表符分隔值。
  单整数 1200，不应未经确认就标注为毫秒。

- `[transparent value]`。透明度相关的两个整数。
  证据为 `output/common/activestatus/particle/badeffectparticle.ptl:13` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `100 60`。到下一个段落标签前共有 2 个制表符分隔值。
  样本为 100、60，起止或范围语义和量程尚未确认。

- `[creation frequency]`。粒子生成频率参数。
  证据为 `output/common/activestatus/particle/badeffectparticle.ptl:15` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `4.0`。到下一个段落标签前共有 1 个制表符分隔值。
  样本为浮点 4.0，不能直接解释为每秒 4 个，也不要写成整数以免改变 token 类型。

- `[create area size]`。创建区域大小参数。
  证据为 `output/common/activestatus/particle/badeffectparticle.ptl:17` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `50 20 30`。到下一个段落标签前共有 3 个制表符分隔值。
  三个整数 50、20、30，按名称推断为三轴尺寸，轴向与单位未确认。

- `[object]`。粒子所用动画路径与附加整数。
  证据为 `output/common/activestatus/particle/badeffectparticle.ptl:23` 的第 1 处同名字段。该字段在样本中出现 1 次。
  原始值为 `` `../Animation/BadEffect1.ani` -1 `../Animation/BadEffect2.ani` -1 `../Animation/BadEffect3.ani` -1 ``。到下一个段落标签前共有 6 个制表符分隔值。
  样本为三组相对动画路径和 -1。-1 的具体含义未确认，须保留占位。

## 修改步骤

1. 先识别文件头。文本粒子配置可按命名字段修改，二进制动画不经格式解析器不得用文本编辑器修改。
2. 修改粒子数值时保留浮点类型、坐标数量和动画占位。替换资源前检查相对路径是否实际存在。
3. 回包后检查粒子生命周期、密度、遮挡和资源加载；动画样本需另用支持其二进制格式的工具检查。

## 未确认与验证

当前仓库不解码该 `.ani` 的帧结构。不能因为目录叫 animation 就编造 [FRAME]、[IMAGE] 或帧延迟文本字段。表情和移动表现也必须先按实际文件头识别格式。

回包前后应比较实际目标条目的反编译结果。回包成功只证明编码成功，实机检查仍需覆盖本页所述功能。通用编码与回包限制见总索引。

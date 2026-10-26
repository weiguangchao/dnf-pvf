# 剧情与活动对象修改手册

供维护已有过场步骤和活动对象的代理使用。已读取 `passiveobject/cinematicobject/dimensiongatedungeonmovie/cosmofiendroom4.obj` 全部 219 行，以及 `passiveobject/event/bluemarble/fireexplosion.obj`。路径均相对 `output`。过场步骤是表现时序，活动对象仍可能依赖外部行为。

## 定位入口与重复步骤

过场样本含 22 个 `[movie unit]`，每块有独立 `[/movie unit]`。本次 `passiveobject/passiveobject.lst` 中没有找到该样本路径，因此未证实它的调用 ID。先在过场调用处确认入口，不能按文件名推造编目。

活动编目中 `39003` 对应 `Event/BlueMarble/FireExplosion.obj`。这与编目 `40002` 的 `Common/FireExplosion.obj` 不是同一条目。

## 过场顶层与步骤参数

- 过场第 3 行 `[passive object type]` 为字符串 `` `[cinematic object]` ``，第 5 行 `[passive object sub type]` 为 `` `[object pattern]` ``。它们是字符串枚举，不是嵌套块起点。
- 第 7 至 9 行 `[int data]` 有两整数 `0 57031`。第 15 行 down-arrow 同时用 57031，支持怪物关联的推断，但不能据此解释第一个 0。
- 第一个 movie-unit 在第 11 至 17 行。`[type] show down arrow` 后 `[down arrow data]` 是字符串 `monster` 与四整数 `57031 0 0 0`。第一个整数可能是怪物 ID，后三列的偏移或选择语义未证实。
- 第二个 unit 第 19 至 27 行的 type 为 `notice`，`[time] 3000` 是单整数，`[notice]` 是空字符串加整数 `0`。保留空字符串，不将 0 当文本条数。时间单位未证实。
- 第三个 unit 第 29 至 33 行只有 type `clear down arrow`，没有 time。不能为了统一结构补时间。
- 第四个 unit 第 35 至 45 行的 type 为 `show screenshot`。`[ani path]` 为 `PassiveObject/CinematicObject/DimensiongateDungeonMovie/Animation/cosmofiendRoom4_1.ani`，`[ani title]` 是普通反引号字符串，当前可见部分含问号。`[screenshot data] 4000 120 250` 为整数三元组，时间与坐标的列解释尚未证实。
- 第五个 unit 第 47 至 59 行 type 为 `motion`，含 `[time] 4000`、`[speech]` 字符串、`[notice]` 空字符串加 0，以及 `[motion type] attack 2` 的字符串与整数二元组。不能把 motion-type 的 2 直接当动画帧。
- 第十个 unit 第 95 至 105 行 type 为 `move`，含 `[time] 4000` 和 `[move pos] 481 261 0`。按名称推断为三维目标位置，但坐标系、单位和移动插值未知。
- 第七、第十一、第十六、第十九个 unit 分别在第 67、107、155、183 行，也使用 `show screenshot`。这些截图的 data 为 `3000 120 250`，与第四个的首值不同。修改一张图必须以 unit 起始行和 ani-path 共同定位，不全局替换 screenshot-data。

以下为第四个步骤的节选。空格只用于阅读，不代表原 TAB 和 CRLF。

```text
[movie unit]
[type]
`show screenshot`
[ani path]
`PassiveObject/CinematicObject/DimensiongateDungeonMovie/Animation/cosmofiendRoom4_1.ani`
[ani title]
`病毒之因?特的瘟疫?`
[screenshot data]
4000 120 250
[/movie unit]
```

## 活动对象可能没有内置动作

`passiveobject/event/bluemarble/fireexplosion.obj` 全部 8 行只有 `[width] 0 0`、`[pass type]` 字符串 `` `[pass all]` ``、`[piercing power] 1000`。没有 basic-motion、basic-action 或 attack-info。不能用文件名推断这里有可修改的火伤字段。需要继续追活动生成逻辑或调用者提供的数据。

## 编辑步骤与限制

先找实际调用入口，再按第几个 movie-unit 和 type 定位步骤。保持 22 块的原顺序和各块闭合。仅替换已知现有路径或原数字。直写的 speech、ani-title 字符串受源归档字符串表限制，不能随意输入新文案。内联本地化显示段的修改也不能替代 `.str` 值更新。

保存原字面头 `#PVF_File\r\n`、CRLF、TAB 和原 token 类型。不要直接粘贴节选覆盖源文件。真实重建并重新提取，再完整播放过场检查箭头、截图清除、对白和移动衔接。`--verify` 只验证源归档脚本往返。

本页未确定过场调用 ID、int-data 两列、截图三列、坐标单位或现有问号是否来自上游乱码。缺少编码依据时保留原文字，不自行还原所谓正确台词。

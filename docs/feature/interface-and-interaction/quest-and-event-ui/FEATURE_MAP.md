# 任务、活动与教学界面修改手册

供调整任务窗口、活动提示与教程表现的代理使用。已读取任务商店、活动通知、教程 UI、教程动作、指南 UI，并分析活动按钮配置的 60 个 info 块。路径均相对 `output`。文案和教程显示不决定实际任务奖励或活动资格。

## 任务窗口与活动提示

- `ui/quest/questshop.ui` 共 26 行。window 的 `[type] popup`、`[horizontal distance] 543`、`[vertical distance] 188`、`[tile type] 5`、`[size] 19 23`、`[alpha] 255` 都是顶层字段。距离、尺寸与透明度尺度尚未在客户端确认。
- 第 17 行 `[title accesorry type] 10` 保留原拼写。第 19 行 title-string 引用 module 20 的 `quest_shop_title`，显示任务商店。`[controls]` 第 22 至 24 行为空。不能因窗口名就补一份任务条目列表。
- `ui/event/starterserver/noticepartyplay.ui` 共 19 行，三个 ui-controls。board-image `300` 候选位置 `1 1`，图集 `Interface/WindowCommon.img` 和整数串 `11 230 40 213 214 215 216 217 218 219 220 221`。
- 两个 text `301`、`302` 分别在第 8、15 行引用 `starter_notice_03_01`、`starter_notice_03_02`，显示组队提高经验和任务道具掉落。二者各有 `[parent]` 字符串 `300`。这只是通知内容，没有加成数值字段，改文字不改变加成。

## 活动按钮按 info/id 定位

`ui/event/informationbuttoninfo.evn` 共 628 行，60 个 `[info]` 与对应结束标签。

- 第一块第 3 至 12 行 `[id] 0`、`[imageStartIndex] 1` 各接单整数。大小写 `imageStartIndex` 是原标签。不能改成 image start index。
- 第 9 行 `[tooltip]` 接字符串 `enable` 和 module 20 引用 `info_tooltip_enable_000`。第二块 id 1 的图块起点为 4、第三块 id 2 为 7。图块连续不意味着 id 全连续，下一块 id 已为 4。
- 第 58 至 64 行 id 6 的 imageStartIndex 为 19，但没有 tooltip。保留缺省结构，不给每块强加提示。
- 第 256 行另一个 tooltip 接 `disable` 和 `info_tooltip_enable_045` 的空显示引用。enable/disable 是字符串模式，键名中的 enable 不保证模式是 enable。
- ID 的调用来源、图块一组多少帧以及 enable/disable 的条件不在这些字段中。修改应以 info 的 id 定位，不按第几行批量递增编号。

## 教程控件与共享动作

`ui/tutorial/tutorial.ui` 共 211 行，38 个 ui-controls 和 29 个 `[common action]`。

- 第 4 行 image `IDC_IMAGE_0` 后为 `236 26 1`、`Interface2/Tutorial.img`、`1 0`。其 common-action 第 5 行引用 `Action/Interpolation.act`。第 10 行 `IDC_IMAGE_1` 有同样动作。共享动作修改可能影响所有 29 个挂载处中的相关控件，应逐个查实际路径。
- 第 68、74、80 行技能效果 image 使用 `LINEARDODGE` 字符串与图块索引 18，common-action 为 `Action/SkillEffect.act`，不是 Interpolation。
- 第 92 行 animation `IDC_ANI_SKILL` 用 `UI/Tutorial/skill.ani` 和尾整数 0。第 96 行 `IDC_ANI_MINIMAP` 用 `UI/Tutorial/minimap.ani`。第 100、104 行背包和快捷栏提示又共用 skill.ani，不能仅按动画文件名判定提示对象。
- 第 108 行 text `IDC_TEXT` 后有 13 整数 `160 224 0 9 0 485 1 1 1 0 221 197 147`，没有内联具体文本。零值是运行时填文候选，未证实其绑定规则。
- 第 114 行 button `IDC_BUTTON_EXIT` 后为 `730 108 1`、图集与 `4 37 38 39 40`。保持 ID，避免只移动图像而遗漏退出点击区。

`ui/tutorial/action/interpolation.act` 共 51 行。第 3 行 TRIGGER 内 `[ON TIMING] [SET VISIBLE] 0 0`，随后 DO-BEHAVIOR/MY-CONTROL 0。第 15 行 BEHAVIOR 内 PLAY-SOUND `TUTORIAL`，再 RESET/CONTROL。此后两个 INTERPOLATION 分别控制 ALPHA 与 MOVEMENT。

- ALPHA 块第 27 行 `[DURATION] 500`，第 29 行 `[FIRST ARG] 128.0 -1.0`、第 31 行 `[SECOND ARG] 255.0 -1.0`，均为浮点二元组。透明度过渡是名称推断，-1.0 的哨兵意义和时间单位未知。
- MOVEMENT 块第 39 行 DURATION 也是 500，第 41 行 FIRST-ARG 为整数对 `-1 -1`，SECOND-ARG 后是无值标签 `[0]` 和 `[10]`，不是普通数字 token。不能为统一格式转成 `0 10`。

`ui/guide/guide.ui:24` 的 basic-edit-box `IDC_EDIT_SEARCH` 带 `279 20 0 2 30 132`。第 28 行 tab-group `IDC_TABGROUP` 含内容与 Lv相关两个标题，尾整数 `1 60`。第 34、38 行两个 tree 的 ID 为 `IDC_TREE`、`IDC_LIST`，候选位置相同 `0 48`，整数尾为 `0 5 183 327 221 197 141`。重叠是原结构，不擅自分开。

## 修改与检查

先选实际窗口和控件 ID，活动按钮先选 info 的整数 id。文字改 `ui/ui.kor.str` 的现有键值，内联 display 不参与编译。教程时序修改先记录共享动作的引用范围，再只改目标插值块，保留两块各自 token 类型。

保留 `#PVF_File\r\n`、CRLF、TAB 和原反引号。本文空格样例不是覆盖文本。新标签、字符串和路径受源归档字符串表限制。需要真实重建并重新提取，再检查通知父子位置、活动按钮启用和禁用提示、教程显隐及退出。`--verify` 不验证修改结果。

尚未知晓活动触发条件、空 controls 的运行时填充、插值哨兵、时间单位和任务规则。不要把表现改动报告为玩法改动。

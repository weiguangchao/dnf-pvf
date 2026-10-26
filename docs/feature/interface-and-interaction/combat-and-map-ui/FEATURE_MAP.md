# 战斗、地图与结算界面修改手册

供调整 HUD、地图面板、载入提示和结算表现的代理使用。已读取五个 `.ui` 和一个结算 `.act`，并检查结算动画文件头。路径均相对 `output`。这些描述不直接改变地下城开放条件或结算奖励。

## HUD 控件按字符串 ID 定位

`ui/hud/hud.ui` 全部 49 行含 12 个 `[ui controls]`，无外层 window。

- 第 4 行 `[highlight button]` `myinfo_button` 的尾参数为 `283 52 1`、图集 `interface2/HUD/HUD.img`、`5 5 6 7 93 98`。第 8、12、16、20 行的 inventory/quest/skill/auction 按钮各有自己的五索引组。5 与后面五项数量相符，但各状态意义未证实。
- 第 24 行 `[button]` `exp_toggle_button` 后为 `65 76 1`、同图集、`4 30 31 32 30`。重复索引 30 是观察到的原值，不去重。
- 第 36、40 行 `skill1_button` 与 `skill2_button` 都位于候选位置 `519 51`，但尾图块组不同。重叠可能由客户端切换显示，未经运行证实，不为消除重叠擅改其一。
- 第 44 行 `[image]` `aura_gauge_lineardodge` 含候选位置 `-2 -30`、整数 `3`、图集、字符串 `LINEARDODGE` 与 `set virtual size`，再接 `1 85`。保留两个可选字符串，不能把所有 image 定为固定列数。
- 第 48 行 `[animation]` `newly_skill` 后为 `360 40 1`、`UI/HUD/Animation/hud_new.ani`、`1 0`。动画尾列与其他 UI 中单个 0 的形式不同，保留原形。

## 小地图窗口和图块

`ui/dungeonminimap/dungeonminimap.ui` 共 43 行。第 7 行水平对齐 `right`，第 9 行距离 `-13`，第 11 行垂直对齐 `top`，第 13 行距离 `25`。它没有 size 字段，不能强制补世界地图的 size。

- 第 15 行 `[tile type] 10`、第 17 行 `[alpha] 150` 各为单整数。透明度是名称推断，取值尺度未由客户端证实。
- 第 23 行 `[title bar] 1 -1 39 -1` 是四整数。-1 的哨兵意义未知，不能把它们改成 0。
- 第 25 行 `[draggable] 1` 和第 27 行 `[close button] 0` 是单整数，按名称提示可拖动和无关闭按钮。
- 第 29 行 `[imagepack]` 为 `Interface2\Minimap\Dungeon\minimap.img`，原字符串用反斜杠。第 31 行 `[starting frame] 27`、第 33 行 `[tile offset] 8`、第 35 行 `[tile width] 18`、第 37 行 `[tile height] 18` 各为单整数。可推断控制小地图图块，不把宽高当真实地图格子尺寸。
- `ui/worldminimap/worldminimap.ui:17` 另有 `[size] 10 8`，第 23 行 `[title string start] 33`。第 46 行按钮 `IDC_SCALE_MINIMAP_UP` 为候选位置 `4 3`，图块 `4 179 181 182 182`。第 50 行 DOWN 按钮为 `17 3`、`4 180 183 184 184`。只修改表现不能证明缩放倍率改变。

## 载入、入场提示与结算

- `ui/dungeonloading/dungeonloading.ui` 共 9 行。第 4 行 image `IDC_DUNGEONLOADING_TOPBOTTOM_BANNER` 用 `WorldMap/selectdungeon02.img` 和尾整数 `3 79 1 0`。第 8 行 text `IDC_DUNGEONLOADING_TIP_TEXT` 后有 13 个整数 `20 580 0 9 316 760 1 1 1 0 255 255 0`，316 为文本索引候选。中间各列不全明，不能替换成任意字符串。
- `ui/selectdungeon/enterconditionwindow.ui` 共 42 行，三个 image 与三个 text 共用候选位置。text ID `1`、`3`、`5` 分别引用 `dungeon_enter_condition_00`、`01`、`02`。提示文字描述难度和评级，但文件没有实际门槛数值字段。改文字不解除难度限制。
- `ui/result/result_admission0.act:3` 的 `[MOTION]` 内 `[BASE ANI]` 是 `result_admission01.ani`。`[SUB ANI]` 有五组路径与两个整数 `0 1` 至 `0 5`。各组路径包括 `result_admission02.ani`、`result_admission03_0.ani`、`result_admission04.ani`、`result_admission05.ani`、`result_admission06_1.ani`。这是一组叠加表现，整数列的层级或偏移意义未证实。
- `ui/result/result_admission01.ani` 是 196 字节二进制，头字节为 `06 00 01 00 25 00 00 00`，没有 `#PVF_File` 文本头。未分析二进制结构，不能用文本编辑器安全改帧或图片索引。

## 修改与验证

按控件字符串 ID 定位改动，保持图块列表原长度和顺序。移动一个 HUD 按钮后检查 tooltips 和客户端点击区。小地图只改已定位的布局或图块参数，地下城规则去实际规则文件查。文案应修改 `ui/ui.kor.str` 的现有键值，内联显示段不生效。

保留 `#PVF_File\r\n`、CRLF、TAB 和原 token 类型。本文空格样例不是覆盖模板。路径和 ID 受源字符串表限制。需要真实重建并重新提取，再验证 HUD 点击、两类小地图、载入和完整结算动画。`--verify` 不能替代修改验证。

尚未确认布局单位、控件尾列完整定义、小地图缩放实现或结算分数关联。二进制动画只保留和引用，不能据名称猜改。

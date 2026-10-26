# 商城与装备服务界面修改手册

供调整商城选色、增幅选择和随机属性面板的代理使用。已读取 `ui/cashshop/selectavatarcolorwindow.ui`、`ui/amplify/amplifyselectwindow.ui` 和 `ui/randomoption/randomoptiontotal.ui`。路径均相对 `output`。这些字段不能证明价格、增幅收益或随机词条规则改变。

## 商城选色入口

选色文件共 70 行。window 内 `[type] popup`，对齐 `left/top`，水平和垂直距离各 `300`。`[tile type] 7`，`[size] 0 0`。零尺寸并不证明窗口不可见，窗口单位与自动布局规则未知。

- 第 22 行 board-image 的 ID 为字符串 `0`，接 `-11 -11 2`、图集 `interface2/cs_shop/cs_shop.img`、字符串 `draw by loop` 与整数串 `11 13 6 129 130 131 132 133 134 135 136 137`。资源后的 11 与九个图块之间还含两整数，不把它按按钮帧数解析。
- 第 26 行第二个 board-image ID `6`，整数串为 `11 13 4 146 147 148 149 150 151 152 153 154`。重复类型但图块和尺寸候选不同，按 ID 定位。
- 第 34 行 text `3` 引用 `avatar_color_ui_01`，第 39 行 text `5` 引用价格标签 `avatar_color_ui_02`，第 48 行 text `7` 引用恢复原状标签 `avatar_color_ui_03`。标签不编码商品售价。
- 第 53 行 button `8` 后为 `148 -9 1`、同图集、`4 160 161 162 163`。第 57 行 page-button `9` 只有四整数 `78 54 0 0`，没有图集，不统一补图块。
- 第 61 行 control `1000` 带六整数 `-10 -10 0 2 0 0`。第 64 至 66 行 ui-path 将 `UI/CashShop/SelectAvatarColorPass.ui` 挂到 `1000`。具体色项需继续沿该子文件核对，不能只改父窗口声称改好颜色列表。

## 增幅选择的 ID 不等于实际属性

`ui/amplify/amplifyselectwindow.ui` 共 71 行，16 个 ui-controls。

- 第 4、8、12、16 行四个背景 image 位置候选为 `12 6`、`12 48`、`12 90`、`12 132`，共用 `interface/production.img` 和尾整数 `2 0 1`。
- 第 20、24、28、32 行四个图标 image 的图集为 `interface2/ItemToolWindow/windows4/ItemTool_window4.img`，尾整数分别 `2 100 1`、`2 102 1`、`2 101 1`、`2 103 1`。不能认为中间编号顺序对应同样排列的数值属性。
- 第 36、40 行 button `apply` 和 `cancel` 候选位置为 `9 185`、`67 185`，同用 `interface/WindowCommon.img` 和 `4 12 13 14 15`。不同动作依赖 ID 绑定候选，换图块不交换功能。
- 第 54 行 text ID `physical_defense_text` 实际引用 `amplify_physical_defense`，显示异次元体力。第 59、64、69 行分别显示精神、力量、智力。名字里的 defense/attack 不能直接解释为实际提升防御/攻击。
- 第 55 行文本尾十整数 `9 0 65 0 0 0 0 255 0 240`，力量那行末三整数为 `250 0 240`。末三列为颜色候选，未证实 65 是像素宽度。保留不相关列。

## 随机属性窗口的页与子文件

`ui/randomoption/randomoptiontotal.ui` 共 67 行。第 17 行 size 为 `19 17`，第 19 行 alpha 为 `255`，第 21 行 title-string 引用 `randomOptionUnseal_00`。

第 29 至 33 行 tab-group `1000` 有三标题，解除封印、合成、变换，尾整数 `1 57`。三个 control ID `11000`、`12000`、`13000` 分别经 parent-tab 绑定父 ID `1000` 的页 0、1、2。第 53、57、61 行 ui-path 分别挂载 `UI/RandomOption/RandomOptionUnsealPass.ui`、`UI/RandomOption/RandomOptionRegenerationPass.ui`、`UI/RandomOption/RandomOptionChangePass.ui`。标题键原拼写包含 `reandomOptionRegeneration_03`，不纠正为新键。

## 二进制强化表现的边界

`ui/equipmentupgrade/eventequipmentupgradeidle.ani` 实测为 148 字节二进制，头八字节 `04 00 01 00 2c 00 00 00`，无 `#PVF_File` 文本头。本页未解析其格式，不能安全按文本改动画。该目录中的动画不提供可确认的强化成功率字段。

## 操作与验证

先锁定服务窗口和父页。布局修改保持控件 ID、parent-tab 和 ui-path 的绑定，只改已定位数值。新文案应改 `ui/ui.kor.str` 现有键的值，内联 display 不参与编译。实际费用与结果逻辑需另查对应服务规则。

保留 CRLF、TAB、`#PVF_File\r\n` 和原 token 类型，本文空格元组不可直接覆盖。编译受源归档字符串表限制，不新造路径或控件 ID。真实重建并重新提取，再验证三随机属性页、选色分页和增幅选择的显示及点击。`--verify` 只查源归档往返。

未知项包括完整控件列、商城子页面颜色数据、增幅事件绑定和服务端消耗规则。没有这些证据，不以 UI 数值推导价格或成功率。

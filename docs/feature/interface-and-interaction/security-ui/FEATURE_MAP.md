# 安全提示与限制界面修改手册

供修改安全告知、期限道具提示和身份限制面板的代理使用。已读取四个 `.ui`，并检查 goblinpad 动画文件头。路径均相对 `output`。本页修改的是提示与布局，不能开通安全服务或解除账号限制。

## 安全警告窗口

`ui/security/securitywarningwindow.ui` 全部 68 行。window 内 type 为 `popup`，水平/垂直对齐为 `center/middle`，两个 distance 均为 `0`。tile-type 为 `0`，size 为整数对 `19 14`，alpha 为 `255`。这些单位和尺度未由客户端确认。

- 第 21 行 title-string 引用 module 20 的 `SecurityWarringWindow_00`。键实际拼成 Warring，不改为新键。标题显示保安警告通知。
- 第 27 行 basic-button ID 是字符串 `0`，后为三整数 `87 156 1`、取消文本引用 `SecurityWarringWindow_01`、尾整数 `0`。不要将 ID 字符串转为整数 token。
- 第 32 行 image `1` 后为 `16 11 1`、`Interface/SecurityCard/securityWarning.img`、`4 0 1 1 255`。尾部四值的状态或透明度含义未全部解析，不能当四个帧号逐项改。
- 第 36 行 text `2` 引用 `SecurityWarringWindow_02`，文本含三个以字面 `\n` 分隔的句段。尾十整数为 `9 0 160 0 0 0 0 255 146 0`。保留换行转义，末三列为颜色候选。
- 第 45 行 text `4` 引用 `SecurityWarringWindow_03`，说明二级密码保护。第 50 行 custom-button `5` 引用 `SecurityWarringWindow_04`，后有两整数 `1 103`。103 的事件或样式含义未证实，不把它当网址或服务编号。
- 第 59、63 行 control `101`、`102` 后分别为 `152 110 0 2 28 28` 与 `182 110 0 2 28 28`。按位置推断为两个挂载区域，绑定内容未证实。

## 空窗口和限制提示不可过度解释

- `ui/shutdown/servicehourswindow.ui` 共 15 行。只有 window、type popup、tile-type 1、size `0 0` 和空 controls 块。文件没有关服时间或游戏时长数值。不能在这里安全新增限时规则。
- `ui/simpleid/simpleidmylimitpopup.ui` 共 9 行。text ID 为 `notice text`，后有 13 整数 `10 20 0 9 13036 250 1 0 0 0 255 255 255`。13036 为文本索引候选，不是账号上限。
- 同文件第 8 行 text-button `cancel button` 后为 `105 55 1`、`Interface/WindowCommon.img`、`5 12 13 14 15 13033`。尾整数 13033 是文本索引候选，不能把五个尾值全部当按钮动画帧。

## 期限道具窗口包含独立变量块

`ui/timelimiteditemsinfowindow/timelimiteditemsinfowindow.ui` 全部 41 行。

- 第 13 行 size 为 `19 21`，第 15 行 title-string 引用 `time_limited_items_info_window_00`。第 18 行 title-accesorry-type 为 `20`。
- 第 23 行 tab-group ID `100` 后为 `0 20 1`、一个优惠标题引用、尾整数 `1 60`。一个标题对应整数 1 是观察到的形态，不能用 60 推导天数。
- 第 27 至 29 行 `[variable]` 内容是字符串 `[int]`、字符串 `102`、整数 `1 5`。这不是 UI control。变量值、范围或绑定的列意义未知，不能把 5 当期限五天。
- 第 32 行 tree `201` 后为 `0 48 0 5 219 204 255 255 255`。第 36 行 text `101` 后为 `3 260 0 9 31076 219 1 0 0 1 255 255 255`。31076 为文本索引候选，期限实际数据未出现在此描述中。

## goblinpad 是未解析二进制表现

`ui/security/goblinpad/01_bunker_eff.ani` 实测 324 字节，头八字节为 `0b 00 01 00 1e 00 00 00`，没有 `#PVF_File` 文本头。未分析二进制格式，不能按文本编辑数字键、验证流程或动画帧。目录名只能说明资源分组，不能证明认证逻辑在这里。

## 编辑与验证

先确定需要改变的提示和控件 ID。布局改原数值，文字改 `ui/ui.kor.str` 中现有键值。`ui/ui.kor.str:399` 存在 `SecurityWarringWindow_00>保安警告通知`。内联显示段不参与编译。数字文本索引应先追客户端文本映射，不随意换成 module 20 引用。

保留 `#PVF_File\r\n`、CRLF、TAB、反引号、字面 `\n` 和原 token 类型。本文空格样例不是可覆盖文件。原字符串表不允许任意新键、新路径或新 ID。真实重建并重新提取后，应验证提示出现、关闭、文字换行和期限列表。`--verify` 只查源归档往返。

尚未知晓各提示的真实触发条件、限制规则、variable 四列语义和安全服务事件绑定。未解析二进制不得尝试修改认证行为。

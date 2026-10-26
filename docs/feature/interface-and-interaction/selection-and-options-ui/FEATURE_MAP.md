# 登录选择、选项与公共界面修改手册

供调整角色选择表现、声音选项和主菜单的代理使用。已读取选择特效 UI、角色选择上层描述、声音面板和 `mainhudmenu.co`。路径均相对 `output`。角色数量、服务器路由和真实音量设置由其他运行逻辑控制。

## 选择画面的分层与控件

`ui/selectserver/effect/selectservereffect.ui` 全部 13 行包含三个 animation 控件。三个 ID 分别为 `IDC_ANIMATION_SELECT_CHARACTER_EFFECT_BASE1`、`IDC_ANIMATION_SELECT_CHARACTER_EFFECT_BASE2`、`IDC_ANIMATION_SELECT_CHARACTER_EFFECT`。每个后接三整数 `343 2 1`、一个路径字符串、尾整数 `0`。路径分别为 `UI/SelectCharacter/Animation/SelectCharacterEffect_back1.ani`、`SelectCharacterEffect_back2.ani`、`SelectCharacterEffect.ani`，后两项与第一项同目录。selectserver 的文件引用 selectcharacter 动画是实际观察，不按目录名纠正路径。

`ui/selectcharacter/selectcharacterover.ui` 全部 329 行包含 82 个 ui-controls。

- 第 4、8、12 行 text ID `1000`、`1001`、`1002` 都带同一 13 整数串 `100 80 0 9 0 120 1 1 0 1 209 185 148`。重复位置可能由客户端按角色槽布局移动，未验证，不据此把所有控件平移到不同槽位。
- 第 284 行 image `1102` 后是 `0 0 1`、`Interface2/SelectCharacter/SelectCharacter.img`、`2 5 0`。第 288 至 320 行后续 ID 重复同形。2 与后两整数相关，但图片状态意义未确认。
- 第 324 行 animation `1120` 后是 `0 0 1`、`UI/SelectCharacter/Animation/SelectCharacter_drag.ani`、`0`。第 328 行 text `1121` 的数值串含 `21355`，这是文本索引候选，不是角色 ID。
- 另有 `selectcharacterover_starterserver.ui` 与 `selectcharacterover_eventserver.ui` 等实际目录条目。本页未分析它们，普通文件的改动不能保证覆盖特殊服务器。

## 声音选项参数

`ui/optionwindow/optionsound.ui` 全部 32 行，七个 ui-controls。

- 第 4 行 board-image `1002` 后为 `-6 0 1`、`Interface/WindowCommon.img`、整数串 `11 216 209 213 214 215 216 217 218 219 220 221`。11 后两值为尺寸候选，其余九值为边框图块候选，未由客户端确认。
- 第 8、13、18 行 text ID 为 `200`、`201`、`205`。分别引用 `optionwindow_65`、`optionwindow_66`、`optionwindow_75`，显示音效、背景音乐、环境音效。每个引用后有十整数 `9 0 150 0 0 0 0 221 197 147`。
- 第 23 行 slide `202` 后有八整数 `0 32 0 4 0 195 100 80`。第 27、31 行 slide `203`、`204` 只将第二个整数改成 `70`、`108`。位置与标签对应支持音量滑条的推断，100 和 80 的范围、初值或步长角色未证实。不能凭这两个数承诺最大音量或默认音量。

## 主菜单是分组内的 info 数组

`clientonly/mainhudmenu.co` 共 75 行，在 `[add menu info]` 内有 35 个重复 `[info]`。每项形态是整数菜单号、字符串命令名、四整数图块候选。

- 第 6 行为 `1000 MYINFO_WINDOW 2 3 4 5`，第 8 行为 `1001 INVENTORY_WINDOW 6 7 8 9`，字符串均有反引号。菜单号不是 UI 控件 ID 字符串。
- 第 16 行命令确实是 `MERNCENARY_WINDOW`，保留原拼写。第 26 行邮件命令为 `2003 MAIL_WINDOW 42 43 44 45`。
- 第 28 行 `2004` 后是显式空字符串和四个 0。这与其他空槽同形，不删除空命令 token，也不凭空填新命令。
- 第 62、64 行分别为 `5000 GAMEOPTION_WINDOW 78 79 80 81` 与 `5001 HOTKEY_WINDOW 82 83 84 85`。第 68 行 `5003 SELECT_CHARACTER_WINDOW 86 87 88 89`，第 74 行 `5006 EXIT_GAME 98 99 100 101`。只使用已存在命令名，不改命令去猜另一个窗口。

## 修改与检查

选择画面先确认普通、starterserver 或 eventserver 的实际入口。按控件 ID 修改现有布局候选或资源引用，不新增角色槽。声音面板只改已定位显示字段，实际音量范围未知时保留滑条尾列。主菜单按整数菜单号修改，不把空槽转换为新功能。

文案应改 `ui/ui.kor.str` 对应原键，内联 display 不参与编译。保存 `#PVF_File\r\n`、CRLF、TAB、空字符串与原 token 类型。本文空格样例不能覆盖脚本。编译受源归档字符串表限制，不新增路径或命令名。真实重建并重新提取后，检查角色槽、三种声音标签和菜单点击。`--verify` 不能证明修改生效。

尚未确认重复角色控件的运行时布局、声音数值的绑定、菜单尾四列状态顺序或服务器选择规则。本页未分析载入进度资源，不把公共 UI 当网络配置。

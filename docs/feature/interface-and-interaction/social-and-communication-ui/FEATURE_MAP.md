# 社交、邮件与聊天界面修改手册

供修改组队、邮件、聊天和表情界面的代理使用。已读取组队创建、邮件撰写、聊天窗口与一个 `.emo` 及表情编目。路径均相对 `output`。这些 UI 不定义组队人数上限、邮费或聊天权限。

## 组队创建控件

`ui/party/partycreate.ui` 共 49 行，有 12 个 `[ui controls]`。使用可读字符串 ID，不是全为数字。

- 第 4 行 text `title` 后有 13 整数 `1 11 0 9 21944 64 0 1 1 0 221 197 141`。21944 是文本索引候选，末三列是颜色候选，各自的实际消费逻辑未证实。
- 第 8、12、16、20 行 text 的 ID 为 `region`、`dungeon`、`difficulty`、`limit number`，文本索引候选依次为 `19057`、`19058`、`21943`、`21949`。不要把 difficulty 的数值串解释为副本难度参数。
- 第 24 行 basic-button `confirm` 后是五整数 `76 95 0 1 100003`。第 28 行 cancel 为 `133 95 0 1 21401`。两者 ID 是客户端绑定候选，不改名。
- 第 32 行 basic-combo-box `limit combo box` 后为 `194 73 1`、字符串 `without edit`、整数 `1 44`。第 36 行 difficulty-combo-box 尾部是 `1 100`，这不是 100 级难度。
- 第 48 行 `title combo box` 使用字符串 `edit and list` 和整数 `1 160`。可编辑选项与其他四个不可编辑下拉框不同，不能统一格式。

## 邮件输入和附件区域

`ui/mail/createmailframe.ui` 全部 137 行含 34 个 ui-controls。

- 第 8 行 basic-edit-box `IDC_EDIT_NAME` 后为六整数 `51 46 0 2 18 128`。第 12 行 `IDC_EDIT_SENDMONEY` 为 `77 280 0 2 20 120`。名称和位置提示收件人与金额框，但 18/20 的长度限制或类型语义未知。不要据此改发信金额上限。
- 第 16 行 button `IDC_BTN_CHECKNAME` 用图集 `Interface/newstyle/windows/Mail/AddingMailControl.img` 和 `4 6 7 8 9`。四索引的状态顺序未证实。
- 第 20、24 行发送和取消是 basic-button，ID 为 `IDC_BTN_SEND` 与 `IDC_BTN_CANCEL`，尾部文本索引候选为 `21113`、`21401`。
- 第 56 至 92 行依次定义 `IDC_AREA0` 至 `IDC_AREA9` 十个 control，每个带 `0 2 28 28`。候选位置形成两行五列，第一行 `33/67/101/135/169` 与 `205`，第二行相同横值与 `237`。这是 UI 布局观察，不保证邮件系统允许十附件。
- 第 100 至 136 行 `IDC_BTN_PASTLIST0` 至 `IDC_BTN_PASTLIST9` 共十个按钮，共用图块 `4 10 11 11 10`，纵值按 16 增长。重复索引 11 是原值，不去重。

## 聊天的父页、选项与子面板

`ui/chat/chatwindow.ui` 全部 311 行有 43 个 ui-controls、12 个 int-option、6 个 parent-tab 和 22 个 parent。

- 第 12 至 19 行 tab-group ID `99` 含六个 module 20 标题引用，依次为普通、队伍、公会、师徒、悄悄话、喇叭。尾部很长的整数串混有页号和颜色候选，未完整解析，不把六标题后所有整数统称 RGB。
- 第 22、26、30、34、38、42 行 filtering-board 的 ID 为 `80` 至 `85`，各带四整数 `0 0 0 0`。过滤行为由客户端如何使用这些 ID 决定，本文件没有明确禁词列表。
- 第 46 行 hyperlinklabel `0` 的形态为候选位置 `14 24 1`、字符串 `left scroll`、整数 `7 330 130 221 197 141 1 1`。其内 int-option `line height 16` 和 `display marginwidth -5` 各自闭合，再经 parent-tab `99 0` 绑定普通页。后五个 hyperlinklabel 分别绑定页 1 至 5。只改普通页不能宣称所有频道布局同步。
- 第 281 行 control `105` 为 `112 295 0 2 178 110`。第 285 至 287 行 ui-path 是三元组 `UI/Chat/ChatEmoticon.ui`、字符串 `105`、整数 `0`，比角色窗口常见二元组多一项。最后一项语义未知，保留。
- 第 296 与 303 行 tooltips `95` 和 `96` 都绑定字符串目标 `91`，但文字分别为决斗场无法使用和使用聊天图案，尾整数串中有 `0/1` 差异。这是条件提示候选，不能删掉一个作为重复项。

## 聊天表情的编目与类型

`chatemoticon/chatemoticon.lst:2` 的 `1` 映射到 `event1.emo`。`chatemoticon/event1.emo` 共 8 行，第 3 行 `[type]` 接字符串 `EVENT` 和整数 `2660539`，第 5 行 `[ani]` 接 `ChatEmoticon/Animation/000_hi.ani`，第 7 行 `[macro]` 接 module 24 的 `emoticon_macro_evt_001`，显示 `evt1`。EVENT 大写是原值。2660539 的事件、道具或权限含义尚未核实，不当作动画编号。

## 修改与检查

按字符串 ID 和父页定位，改位置候选或现有图块引用。附件区域数量、金额输入框和频道提示只描述界面，实际限制应另追规则。文字修改应核对 `ui/ui.kor.str` 或 `chatemoticon/chatemoticon.kor.str` 的原键，保留占位符。后者第 4 行为 `emoticon_macro_evt_001>evt1`，与样本 macro 引用相符。内联 display 不参与编译。

保留字面文件头 `#PVF_File\r\n`、CRLF、TAB、原 token 类型和父子绑定。本文空格样例不能覆盖脚本。不新造源字符串表之外的 ID、路径或宏。需要真实重建并重新提取，再验证组队下拉框、邮件输入与附件、六聊天页和表情入口。`--verify` 不验证 output 修改。

尚未知晓输入框各列、表情 EVENT 整数含义、客户端事件绑定和社交限制的实际实现。

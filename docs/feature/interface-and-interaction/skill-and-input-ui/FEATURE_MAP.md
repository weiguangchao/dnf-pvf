# 技能树与输入设置修改手册

供修改技能显示布局、热键与手柄映射的代理使用。本页核对实际 `.ui` 和 `.co`，区分技能展示、按键默认映射与运行时技能规则。路径均相对 `output`。

## 技能树入口和重复技能块

`clientonly/skillshoptreespindex.co` 共 5 行。第 3 至 5 行 `[skill tree]` 内是 11 组职业字符串与路径字符串，例如 `` `[swordman]` `SkillTree/Swordman_Sp.co` ``。这是字符串对列表，不是技能 ID 表。

`clientonly/skilltree/swordman_sp.co` 共 1407 行，含五个 `[character job]`、163 个 `[skill info]` 和 41 个 `[next skill]`。职业块起始行依次为 3、143、495、821、1105，对应 `[swordman]` 加 `none`、`weaponmaster`、`soulbringer`、`berserker`、`asura`。每块有 `[/character job]`。

- 第一块第 7 行 `[index] 5` 是单整数技能引用候选，第 9 行 `[icon pos] 141 0` 是两个整数布局坐标候选。单位和坐标原点未证实。
- 第一块第 31 行 index 为 `1`，icon-pos 为 `376 67`。weaponmaster 块第 179 行也有 index `1` 和相同位置，但第 183 行另有 `[next skill] 3`。必须按职业分支与 index 共同定位，不能替换全文所有 index 1。
- next-skill 是单整数且可重复出现，名称支持技能连接关系的推断，是否决定学习前置条件未证实。修改图标位置不等于修改技能学习等级或 SP 需求。

## 技能说明 UI 的可变列

`ui/skill/skillshopexplain.ui` 共 46 行，有 9 个 ui-controls 块。

- 第 4 行 `[image]` `22` 后是 `-20 3 1`、`Interface2/UI/SkillShop/Skillshop.img`、`1 3`。ID `22` 是字符串，位置候选为有符号整数，资源尾列是整数。
- 第 20 行 `[text]` `4012` 后接 `16 137 1`、module 20 的 `skill_shop_06` 和十整数 `9 0 150 0 1 1 0 104 213 237`。说明文案与位置列不混为一个文本字段。
- 第 25 行 `[button]` `4000` 用图集与 `4 75 76 77 78`。四个索引的按钮状态含义未逐一证实，保留顺序和数量。
- 第 33 行 `[hyperlinklabel]` `4013` 含整数串 `9 176 0 7 179 260 221 197 141 1 0`。其内两个 int-option 分别是字符串 `line height` 加 `14` 与 `display marginwidth` 加 `-5`。这两块用无反引号 `[/int option]` 结束，不能套宠物 grid 的字符串结束形态。
- 第 45 行 `[basic combo box]` `4002` 后含 `8 152 3`、三个字符串 `left without edit without scroll bar`、两整数 `1 89`。不要把字符串选项转成标签。

## 热键默认配置

`clientonly/hotkeysystem.co` 共 239 行，含 79 个 `[key]`。每条为一个 module 25 的文本引用，接整数功能号、两个分类字符串、整数键码。例如第 3 至 5 行为功能号 `48`、`system`、`left`、`27`。第 73 至 74 行上移条目为 `0 character left 38`，后续左、下、右分别为 `1/37`、`2/40`、`3/39`。方向描述与键码相符支持键码映射的推断，但本页不提供完整键码枚举。

- 第 13 至 14 行装备辞典条目的尾键码为 `-1`。按名称推断为未绑定，不能用 0 替换所有 -1。
- 第 97 至 98 行宠物栏条目为 `17 character left 117`。功能号 17 不是按键值 117，两列不能互换。
- `ui/hotkey/hotkeywindow.ui` 共 154 行，26 个 ui-controls。第 38 行 tab-group `0` 含五标题。第 47、53、59、65、71 行 tree `2/3/12/4/5` 各经 parent-tab 绑定页 0 至 4。界面页分类与 `.co` 的 system/character 等有关联候选，但 left/right 语义未核实。
- 该窗口第 122、127、132 行使用、取消、关闭按钮的 ID 为字符串 `7`、`8`、`9`。第 148 行 ui-path 将 `UI/HotKey/Keyboard.ui` 挂到字符串 ID `13`。不要更名导致客户端找不到控件。

创造者另有 `clientonly/hotkeysystemforcreator.co`，本页未读取内容。修改普通 hotkeysystem 不能保证覆盖创造者，目标为创造者时应先另行核对。

## 手柄按产品分组

`clientonly/joypadmapping.co` 共 39 行，只有一个 `[mapping table]`。`[product name]` 是 `Razer Sabertooth Elite (Controller)`。四个 mapping 块中 `[key]` 为字符串 `rgb` 与整数 `0`、`2`、`3`、`1`，各自 `[mapping to]` 为字符串 `x`、`z`、`space`、`c`。这不是通用手柄全局顺序表，不能只按行号猜 ABXY。目标字符串必须已存在于源字符串表。

## 修改与核查

技能布局按分支和 index 改 icon-pos，输入按功能号改尾键码，手柄按产品名和 rgb 编号改 mapping-to。保留其他条目。修改说明文字应改 `ui/ui.kor.str` 或 `clientonly/clientonly.kor.str` 的原键值，`clientonly/clientonly.kor.str:49` 的 `hotkey_48>打开系统功能表/关闭所有窗口` 与该 key 引用相符。内联显示段不参与编译。

保存 CRLF、TAB、字面 `#PVF_File\r\n` 和原 token 类型。本文空格样例不可原样覆盖。不要新造路径、键名或 ID。真实重建、重新提取，再分别验证技能布局、默认键位、已存用户键位和目标手柄。`--verify` 不验证 output 修改。

尚未知晓全部控件列、技能前置连接的运行含义、键码完整枚举、用户设置覆盖顺序和手柄产品匹配方式。

## 技能图标布局

当前鬼剑士技能树的 `[icon pos]` 包含 `141 0`、`376 67` 等双整数位置。布局坐标应按目标职业分支和客户端核对，不把某一职业的间距推广到所有职业或 UI 缩放。

移动已有技能图标时，先按 `[character job]` 和 `[index]` 锁定块，只改其两个 `[icon pos]` 整数。保留 `[next skill]`、技能学习条件和 SP、TP 文件的独立布局。图标移动后仍需在目标客户端检查重叠、连线与可点击范围。

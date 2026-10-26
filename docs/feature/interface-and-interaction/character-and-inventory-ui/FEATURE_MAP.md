# 角色、背包与仓库界面修改手册

供调整已有角色、宠物背包和金库布局的代理使用。已读取 `ui/characterinfowindow/characterinfowindow.ui`、`ui/inventory/inventory_creature.ui`、其子控件文件和 `ui/cargo/cargoconfirmwindow.ui`。路径均相对 `output`。这些文件描述界面，不直接定义物品容量或金库认证规则。

## 入口、窗口与子面板

角色信息文件共 62 行。第 3 至 62 行为 `[window]`，内含 `[controls]`。第 5 行 `[type] popup`，第 7、9 行对齐为 `left`、`top`，第 11、13 行距离为 `122`、`120`，第 17 行 `[size] 22 28` 是整数对。距离和尺寸单位未从客户端证实，不能按 22×28 像素解释。第 19 行标签确实拼成 `[title accesorry type]`，值 `9`，不要纠正拼写。

- 第 24 行控件类型字符串为 `[tab group]`，ID 字符串为 `999`，其后整数 `0 18 3`。接三个 module 20 标题引用和六整数 `5 40 2 45 75 55`。三项标题与整数 3 相符，尾部六列各自含义未知。
- 第 31、37、43 行三个 `[control]` 的 ID 分别为 `1000`、`1001`、`1004`。每个控件内的 `[parent tab]` 各有父 ID 字符串 `999` 与整数页号 `0`、`1`、`2`。
- 第 48、52、56 行 `[ui path]` 各为子文件路径和目标 ID 字符串二元组。分别为 `UI/CharacterInfoWindow/CharacterInfo.ui 1000`、`UI/CharacterInfoWindow/AvatarCreatureInfo.ui 1001`、`UI/CharacterInfoWindow/MakingItemInfo.ui 1004`。修改子界面前先沿该映射定位，不随意重命名 ID。

## 宠物背包的实际控件形态

`ui/inventory/inventory_creature.ui` 全部 133 行，共 27 个重复 `[ui controls]`，没有外层 window。每块按控件类型解析，不能把所有行按同一固定列数处理。

- 第 4 行为 `` `[control]` `3500` 0 0 0 0 ``，含两个字符串和四整数。第 20 行另一个 control `3100` 为 `0 -149 0 2 28 28`，含六整数。`28 28` 按布局推断为区域尺寸，但两个形态不能互换。
- 第 8 行 `[image]` ID 为字符串 `-1`，后接整数 `-3 43 1`、图集 `Interface/newstyle/windows/Inventory/Inventory.img` 和整数 `1 12`。第 16 行 image `3401` 额外有字符串 `LINEARDODGE`。资源字符串之后的参数不能固定按全整数处理。
- 第 24 行 `[text]` `3300` 后有 13 个整数 `4 135 0 9 1 100 0 1 0 0 104 213 237`。前两列为布局位置的推断，末三列为 RGB 的推断，中间各列未全部确认。第 32 行 text `3302` 的数值 `42005` 是文本索引候选，不能把它当宠物 ID。
- 第 40 行 `[gauge]` `3107` 后是 `47 150 1`、`Interface2/profile/profile.img` 和 `3 10 9 9`。第 44 行 gauge `3108` 的位置为 `47 164 1`，尾部为 `3 10 11 11`。修改血条图块不等于调整宠物数值。
- 第 64 行 `[control group]` ID 为 `3101`。第 67 至 69 行 `[ui path]` 把 `UI/Inventory/inventory_creature_control_group.ui` 挂到 `3101`。该子文件共 17 行，只有四个 ID 为 `-1` 的 control，位置整数对分别为 `7 54`、`205 53`、`205 99`、`205 146`，均带 `0 2 28 28`。`-1` 在这里重复使用，不将它批量替换成唯一 ID。
- 第 76 至 80 行 tab-group `3000` 含三条标题引用，依次为宠物、宠物装备、消耗品，尾部整数 `2 48 0`。后续 `3001`、`3002`、`3003` 三个 control 通过 parent-tab 挂到页 0、1、2。
- 第 104 至 114 行 grid `3106` 内有四个 `[int option]`。其内容分别为字符串 `[grid data]` 加 `7 4`、字符串 `[cell basic data]` 加 `0 0 30 30`、字符串 `[cell margin]` 加 `0`、字符串 `[stick vscroll]` 加 `11 0 0 0`。结束 token 在此写为反引号字符串 `[/int option]`，不是无反引号标签。7 与 4 可推断为格子行列，但不证明服务端容量变为 28。
- 第 121、126、131 行 tooltips 的 ID 是 `3600`、`3601`、`3602`，目标 ID 分别为字符串 `3107`、`3108`、`3110`。保留与目标控件的绑定。

## 金库确认窗口

`ui/cargo/cargoconfirmwindow.ui` 共 45 行。第 17 行 size 为 `13 10`，第 19 行 `[alpha] 255`。第 21 行 title-string 引用 `cargoPassword_09`。第 29 行 text `1` 接 `6 20 1`、本地化文本引用和十整数 `9 10 150 0 0 0 0 221 197 147`。第 34、39 行两个 basic-button 的 ID 为 `2`、`3`，各有三位置候选整数、一个文本引用和尾整数 `0`。这些只是确认和取消的界面，不能证明认证已开通或密码已修改。

## 修改步骤与检查点

先定位窗口、目标控件 ID 和父 tab，再仅改所需位置候选、已有图集索引或子面板引用。移动控件时连同关联 tooltips 检查。改标签文字应修改 `ui/ui.kor.str` 中原键的值，例如第 443 行 `inventory_creature_tab01>宠物` 与第 211 行 `char_tab_01>角色`。内联 module 20 引用的 display 不参与编译。不要把数字文本索引直接当 `.str` 键。

保持原 `#PVF_File\r\n`、CRLF、TAB、空 token、反引号和原 token 类型。本文空格样例不能覆盖脚本。源归档字符串表不允许新造控件 ID 或路径。需要真实重建并重新提取，再检查各 tab、子界面、提示和点击位置。`--verify` 只查源归档往返。

尚未证实窗口单位、完整控件列 schema、客户端对 ID 的事件绑定以及 grid 与实际容量的关系。不要以界面格子数替代库存规则。

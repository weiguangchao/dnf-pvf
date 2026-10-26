# 登录、签到与成长活动修改手册

本页用于修改签到奖励、创建角色礼包和成长道具参数。维护者须将活动数据库键、条件和邮寄配置分别保留。

## 入口与已读文件

已读 `event/attendance.evt`、`event/accountfirstlogin.evt`、`event/accountfirstlogindaily.evt`、`event/createcharactergift.evt`、`event/growthcapsule.evt`、`event/growthweapon.evt` 和 `event/fatiguequantity.evt`。多个文件复用相同签到说明，显示文本不能作为活动真实规则的唯一依据。

## 签到和登录参数

- attendance 的 `[event]` 包含 title、explain、db table 和 fatigue，见 `event/attendance.evt:3` 至第 14 行。db table 为 `event_1202_fatigue_attendance`，fatigue 为单整数 30。说明文本也明确消耗疲劳值 30，支持这个条件量。
- `[reward]` 第 18 至 20 行有 30 个整数，即十五对。首五对 `690000005 3 690000004 3 36 3 690000301 1 690000005 3`。推断为每日物品数量，十五对是否十五天按序领取需运行确认。
- `[reward explain]` 后是普通字符串 `game_server_msg_211`，见 `event/attendance.evt:22`。这不是内联本地化模块引用，需检索对应消息键。
- `[send mail]` 内 inven 为 0，detail 为四整数 `0 0 0 0` 与两字符串 `game_server_msg_210`、单空格字符串，见第 24 至 32 行。空格字符串不能改成空字符串并称等价。
- 首登文件 db table 为 `event_give_title_twn`。其 send mail detail 为 `690000000 1 0 0 tw_cb_launching_title_01 tw_cb_launching_mail_01`，见 `event/accountfirstlogin.evt:11` 至第 21 行。前二整数推断物品和数量，后两整数语义未知。
- 每日首登样本 `event/accountfirstlogindaily.evt:11` 后只有 `event_1306_account_reward`，没有奖励块。fatiguequantity 的 db table 为 `event_1201_fortune_cookie_fatigue`、user type 为 0，见 `event/fatiguequantity.evt:11` 至第 15 行。不能凭复用说明补出签到奖励。

## 创建角色和成长参数

- `event/createcharactergift.evt:3` 至第 19 行外层 create character gift，内层 apply job 为普通字符串 `common`。item 是单整数 690000293，不是物品数量对。
- `[new account event start time]` 和 end time 分别为字符串 `2013-06-27 06:00:00`、`2030-07-25 06:00:00`，见第 9 至 12 行。时区及两端包含性未知。新日期字符串还受源字符串表限制，不能任意输入。
- `[create title] tw_newbie_title`、`[create text] tw_newbie_content` 为两个消息键，见第 13 至 16 行，不是可直接覆盖的邮件正文。
- `event/growthcapsule.evt:3` 至第 8 行有 gage percent 10、max gage exp 200000、capsule id 8480。percent 和 exp 名称有字段证据，但经验结转公式及百分数基数未知。
- `event/growthweapon.evt:3` 至第 12 行有 gift growth weapon box 690000003、growth material item 690000002、材料 max 110、event bubble max 10、event sand max 10。后两项具体玩法含义未知，不能当消耗数量。
- `[growth equipment reward list]` 在 `event/growthweapon.evt:13` 后有 56 个整数，开头 `601000000 601000001 601010000 601010001`。职业与等级映射未提供，不能随意按两列重新配对。

## 修改步骤与未知项

签到换奖先记录十五对中的位置和物品数量。邮寄改动另核对 inven、detail 和消息键。成长道具替换须查 stackable 或 equipment 索引，保持单整数和整数流的差异。

回归检查疲劳门槛、每日领取、重复登录防重发、创建角色条件和邮寄结果。db table 的持久化状态由服务器决定，改键可能重置领取记录，本页不能安全建议改名。

## 保存与验证边界

PVF 脚本保留字面头 `#PVF_File\r\n`、CRLF、TAB 和原有 `{1}`/`{3}`、`{6}`/`{8}` 类型。本文中的空格排版不是可覆盖源文件的序列化格式。编译依赖源归档字符串表。只复用已有标记、字符串和路径值。``<module::key`display`>`` 的 display 不参与编译。修改显示文本要定位对应 `.str` 并保留原编码。

交付前逐块比较 token 数量、顺序和引用。完成实际回包后，重新读取目标条目，核对修改值和未改字段。`--verify` 只验证源归档脚本往返，不能证明修改后输出有效。新建 output 文件不会自动入包，删除原有文件会从归档移除。

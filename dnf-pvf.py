#!/usr/bin/env python3
"""解包 DNF 的 PVF 封包（Script.pvf），并把二进制脚本还原成可编辑文本。

格式参考 https://github.com/similing4/pvf/blob/master/chunk.md

封包头部
    uint32 uuid_length
    char   uuid[uuid_length]
    int32  version
    int32  tree_length
    uint32 tree_crc32
    int32  file_count
    byte   tree[tree_length]    加密的目录树
    byte   pack[...]            文件内容，偏移由目录树给出

目录树每条记录
    int32  number
    int32  path_length
    char   path[path_length]    CP949，分隔符是 \\ 或 /
    int32  length
    uint32 crc32
    int32  offset               相对文件包起点

解密
    逐小端 4 字节 w，输出 ror32(w ^ 0x81A79011 ^ crc32, 6)。
    目录树用自己的 tree_crc32，每个文件用自己的 crc32。
    密文长度按 4 字节对齐，解密后截断到真实长度。

脚本格式（文件以 0xB0D0 开头）
    0xB0D0 之后每 5 字节一项，第一字节是类型，后 4 字节是小端 int。
    2 整数 -> "值\\t"
    1,3 整数 -> "{类型=`值`}\\t"
    4 浮点 -> "值\\t"
    5 段落 -> "\\r\\n名字\\r\\n"
    6,8 命令 -> "{类型=`名字`}\\r\\n"
    7 字符串 -> "`名字`\\t"
    9,10 文本链接成对出现 -> "<str序号::名字`文本`>\\r\\n"
    名字取自 stringtable.bin，文本取自 n_string.lst 指向的 .str 文件。

文本按 UTF-8 写出。封包里中文是 CP950 繁体，日文是 Shift-JIS，韩文是 CP949，
逐文件挑解码失败最少的编码。文本里的繁体字默认转成简体（--lang zh-hans），
--lang zh-hant 保留原文。脚本和 .str 都做这个转换，--raw 则两者都不转。
字符串里的反斜杆、反引号、回车、换行写成 \\ \` \r \n，都解不出来的字节写成 \\xNN。

重新打包
    按原封包的目录树顺序读 output 下的文件，写回一个完整封包。
    output 里没动过的文件沿用原封包的字节和密钥，所以原样打包出来的文件和来源一致。
    改过的文本重新编码后追加到文件包末尾。output 里删掉的文件不再写进目录树，
    output 里多出来的文件会被跳过。--lang 要和解包时一致，否则 .str 会被当成改过。

用法
    python3 dnf-pvf.py Script.pvf -o output          # 解包，默认 output
    python3 dnf-pvf.py Script.pvf --list
    python3 dnf-pvf.py Script.pvf --lang zh-hant      # 保留繁体原文
    python3 dnf-pvf.py Script.pvf --raw -o output     # 原样解包，不转文本
    python3 dnf-pvf.py Script.pvf --verify            # 校验文本可无损还原
    python3 dnf-pvf.py Script.pvf --pack              # 打包 output，默认输出 rebuild
    python3 dnf-pvf.py Script.pvf --pack -i out -o rebuild2
"""

import argparse
import os
import struct
import sys
import zlib
from array import array
from collections import namedtuple

KEY = 0x81A79011
MASK = 0xFFFFFFFF

HEADER = struct.Struct("<iiIi")      # version, tree_length, tree_crc32, file_count
ENTRY_HEAD = struct.Struct("<ii")    # number, path_length
ENTRY_TAIL = struct.Struct("<iII")   # length, crc32, offset
INT32 = struct.Struct("<i")

SCRIPT_MAGIC = b"\xb0\xd0"
SCRIPT_HEADER = b"#PVF_File\r\n"
STRING_TABLE = "stringtable.bin"
NSTRING_LIST = "n_string.lst"

# 文本解码。同一封包里会混用多种编码：中文用 CP950(Big5)，日文用 Shift-JIS，
# 韩文用 CP949。逐文件挑一个解码失败最少的，单个条目失败了再试其它。
CODECS = ("cp950", "cp949", "shift_jis", "utf-8")
TEXT_CODEC = "utf-8"          # 写出来的文本用什么编码

# 繁体转简体单字表，数据取自 OpenCC 的 TSCharacters.txt，每个字只取第一个简体写法。
TS_PAIRS = (
    "㑮㑮㑯㑔㑳㑇㑶㐹㒓㒓㓄㓄㓨刾㔋㔋㖮㖮㗲𠵾㗿㗿㘉㘉㘓㘓㘔㘔㘚㘎㛝㛝㜄㚯㜏㛣㜐㜐㜗㜗㜢𡞱㜷㜷㞞㞞㟺㟺㠏㟆㠣𫵷㢗㢗㢝㢝"
    "㥮㤘㦎㦎㦛㦛㦞㦞㨻㨻㩋㩋㩜㨫㩳㧐㩵擜㪎㪎㯤㯤㰙㰙㵗㵗㵾㵾㶆㶆㷍㷍㷿㷿㸇㸇㹽㹽㺏𤠋㺜㺜㻶㻶㿖㿖㿗㿗㿧㿧䀉䀉䀹䀹䁪𥇢"
    "䁻䀥䂎䂎䃮鿎䅐䅐䅳䅳䆉䆉䉑䉑䉙䉙䉬䉬䉲䉲䉶䉶䊭䊭䊷䌶䊺䊺䋃䋃䋔䋔䋙䌺䋚䌻䋦䋦䋹䌿䋻䌾䋼䋼䋿䋿䌈䌈䌋䌋䌖䌖䌝䌝䌟䌟"
    "䌥䌥䌰䌰䍤䍤䍦䍠䍽䍽䎙䎙䎱䎬䓣𬜯䕤䕤䕳䕳䖅䖅䗅䗅䗿䗿䙔䙔䙡䙌䙱䙱䚩䚩䛄䛄䛳䛳䜀䜧䜖䜖䝭䝭䝻䝻䝼䞍䞈䞈䞋䞋䞓䞓䟃䟃"
    "䟆䟆䟐䟐䠆䠆䠱䠱䡐䡐䡩䡩䡵𫟦䢨䢨䤤䤤䥄䥄䥇䦂䥑鿏䥕𬭯䥗䥗䥩䥩䥯䥯䥱䥾䦘䦘䦛䦶䦟䦷䦯䦯䦳䦳䧢𨸟䪊䪊䪏䪏䪗䪗䪘䪘䪴䪴"
    "䪾䪾䫀䫀䫂䫂䫟䫟䫴䫴䫶䫶䫻䫻䫾䫾䬓䬓䬘䬘䬝䬝䬞䬞䬧䬧䭀䭀䭃䭃䭑䭑䭔䭔䭿䭿䮄𫠊䮝䮝䮞䮞䮠䮠䮫䮫䮰䮰䮳䮳䮾䮾䯀䯅䯤䯤"
    "䰾鲃䱀䱀䱁䱁䱙䱙䱧䱧䱬䱬䱰䱰䱷䲣䱸䱸䱽䲝䲁鳚䲅䲅䲖䲖䲘鳤䲰䲰䳜䳜䳢䳢䳤䳤䳧䳧䳫䳫䴉鹮䴋䴋䴬䴬䴱䴱䴴䴴䴽䴽䵳䵳䵴䵴"
    "䶕䶕䶲䶲丟丢並并么么乾干亂乱亙亘亞亚仝仝佇伫佈布佔占併并來来侖仑侶侣侷局俁俣係系俓俓俔伣俠侠俥伡俬私俱俱倀伥倆俩"
    "倈俫倉仓個个們们倖幸倫伦倲㑈偉伟偑㐽側侧偵侦偽伪傌㐷傑杰傖伧傘伞備备傢家傭佣傯偬傳传傴伛債债傷伤傾倾僂偻僅仅僉佥"
    "像像僑侨僕仆僞伪僤𫢸僥侥僨偾僱雇價价儀仪儁俊儂侬億亿儈侩儉俭儎傤儐傧儔俦儕侪儘尽償偿儣儣優优儭儭儲储儷俪儸㑩儺傩"
    "儻傥儼俨兇凶兌兑兒儿兗兖內内兩两冊册冑胄冪幂凈净凍冻凙凙凜凛凱凯別别刪删剄刭則则剋克剎刹剗刬剛刚剝剥剮剐剴剀創创"
    "剷铲剾剾劃划劄札劇剧劉刘劊刽劌刿劍剑劏㓥劑剂劚㔉勁劲勑勑動动務务勛勋勝胜勞劳勢势勣𪟝勩勚勱劢勳勋勵励勸劝勻匀匭匦"
    "匯汇匱匮區区協协卹恤卻却卽即厙厍厠厕厤历厭厌厲厉厴厣參参叄叁叚叚叢丛吒咤吳吴吶呐呂吕咼呙員员哩哩哯哯唄呗唓唓唸念"
    "問问啓启啞哑啟启啢唡喆喆喎㖞喚唤喪丧喫吃喬乔單单喲哟嗆呛嗇啬嗊唝嗎吗嗚呜嗩唢嗰𠮶嗶哔嗹嗹嘆叹嘍喽嘓啯嘔呕嘖啧嘗尝"
    "嘜唛嘩哗嘪嘪嘮唠嘯啸嘰叽嘳嘳嘵哓嘸呒嘺嘺嘽啴噁恶噅噅噓嘘噚㖊噝咝噞噞噠哒噥哝噦哕噯嗳噲哙噴喷噸吨噹当嚀咛嚇吓嚌哜"
    "嚐尝嚕噜嚙啮嚛嚛嚥咽嚦呖嚧𠰷嚨咙嚮向嚲亸嚳喾嚴严嚶嘤嚽嚽囀啭囁嗫囂嚣囃囃囅冁囈呓囉啰囌苏囑嘱囒囒囪囱圇囵國国圍围"
    "園园圓圆圖图團团圞圞坏坏垻坝埡垭埨𫭢埬埬埰采執执堃堃堅坚堊垩堖垴堚堚堝埚堯尧報报場场塊块塋茔塏垲塒埘塗涂塚冢塢坞"
    "塤埙塵尘塸𫭟塹堑塿𪣻墊垫墜坠墠𫮃墮堕墰坛墲墲墳坟墶垯墻墙墾垦壇坛壈壈壋垱壎埙壓压壗𡋤壘垒壙圹壚垆壜坛壞坏壟垄壠垅"
    "壢坜壣壣壩坝壪塆壯壮壺壶壼壸壽寿夠够夢梦夥伙夾夹奐奂奧奥奩奁奪夺奬奖奮奋奼姹妝妆姍姗姦奸娙𫰛娛娱婁娄婡婡婦妇婭娅"
    "媈媈媧娲媯妫媰㛀媼媪媽妈嫋袅嫗妪嫵妩嫺娴嫻娴嫿婳嬀妫嬃媭嬇嬇嬈娆嬋婵嬌娇嬙嫱嬡嫒嬣嬣嬤嬷嬦嬦嬪嫔嬰婴嬸婶嬻嬻孃娘"
    "孄孄孆孆孇孇孋㛤孌娈孎孎孫孙學学孻𡥧孾孾孿孪宮宫寀采寠寠寢寝實实寧宁審审寫写寬宽寵宠寶宝將将專专尋寻對对導导尷尴"
    "屆届屍尸屓屃屜屉屢屡層层屨屦屩屩屬属岡冈峯峰峴岘島岛峽峡崍崃崑昆崗岗崙仑崢峥崬岽嵐岚嵗岁嵼嵼嵽𫶇嵾㟥嶁嵝嶄崭嶇岖"
    "嶈嶈嶔嵚嶗崂嶘嶘嶠峤嶢峣嶧峄嶨峃嶮崄嶸嵘嶹嶹嶺岭嶼屿嶽岳巊巊巋岿巒峦巔巅巖岩巗巗巘𪩘巰巯巹卺帥帅師师帳帐帶带幀帧"
    "幃帏幓㡎幗帼幘帻幝幝幟帜幣币幩幩幫帮幬帱幷并幹干幾几庫库廁厕廂厢廄厩廈厦廎庼廕荫廚厨廝厮廞𫷷廟庙廠厂廡庑廢废廣广"
    "廧廧廩廪廬庐廳厅弒弑弔吊弳弪張张強强彃彃彄𫸩彆别彈弹彌弥彎弯彔录彙汇彠彟彥彦彫雕彲彨彷彷彿佛後后徑径從从徠徕復复"
    "徵征徹彻徿徿恆恒恥耻悅悦悞悮悵怅悶闷悽凄惡恶惱恼惲恽惻恻愛爱愜惬愨悫愴怆愷恺愻愻愾忾慄栗態态慍愠慘惨慚惭慟恸慣惯"
    "慤悫慪怄慫怂慮虑慳悭慶庆慺㥪慼戚慾欲憂忧憊惫憐怜憑凭憒愦憖慭憚惮憢憢憤愤憫悯憮怃憲宪憶忆憸憸憹憹懀懀懇恳應应懌怿"
    "懍懔懎懎懞蒙懟怼懣懑懤㤽懨恹懲惩懶懒懷怀懸悬懺忏懼惧懾慑戀恋戇戆戔戋戧戗戩戬戰战戱戯戲戏戶户扞捍拋抛拚拼挩捝挱挲"
    "挾挟捨舍捫扪捱挨捲卷掃扫掄抡掆㧏掗挜掙挣掚掚掛挂採采揀拣揚扬換换揮挥揯搄損损搖摇搗捣搧扇搵揾搶抢摋摋摐摐摑掴摜掼"
    "摟搂摯挚摳抠摶抟摺折摻掺撈捞撊撊撏挦撐撑撓挠撝㧑撟挢撣掸撥拨撧撧撫抚撲扑撳揿撻挞撾挝撿捡擁拥擄掳擇择擊击擋挡擓㧟"
    "擔担據据擟擟擠挤擡抬擣捣擫擫擬拟擯摈擰拧擱搁擲掷擴扩擷撷擺摆擻擞擼撸擽㧰擾扰攄摅攆撵攋攋攏拢攔拦攖撄攙搀攛撺攜携"
    "攝摄攢攒攣挛攤摊攪搅攬揽敎教敓敚敗败敘叙敵敌數数斂敛斃毙斅斅斆敩斕斓斬斩斷断斸斸於于旂旗旣既昇升時时晉晋晛𬀪晝昼"
    "暈晕暉晖暐𬀩暘旸暢畅暫暂曄晔曆历曇昙曉晓曊曊曏向曖暧曠旷曥𣆐曨昽曬晒書书會会朥𦛨朧胧朮术東东枴拐柵栅柺拐査查桱𣐕"
    "桿杆梔栀梖梖梘枧梜𬂩條条梟枭梲棁棄弃棊棋棖枨棗枣棟栋棡㭎棧栈棲栖棶梾椀椀椏桠椲㭏楇楇楊杨楓枫楨桢業业極极榘矩榦干"
    "榪杩榮荣榲榅榿桤構构槍枪槓杠槤梿槧椠槨椁槫槫槮椮槳桨槶椢槼椝樁桩樂乐樅枞樑梁樓楼標标樞枢樠樠樢㭤樣样樤樤樧榝樫㭴"
    "樳桪樸朴樹树樺桦樿椫橈桡橋桥機机橢椭橫横橯𣓿檁檩檉柽檔档檜桧檟槚檢检檣樯檭檭檮梼檯台檳槟檵檵檸柠檻槛櫃柜櫅櫅櫍𬃊"
    "櫓橹櫚榈櫛栉櫝椟櫞橼櫟栎櫠櫠櫥橱櫧槠櫨栌櫪枥櫫橥櫬榇櫱蘖櫳栊櫸榉櫻樱欄栏欅榉欇欇權权欍欍欏椤欐欐欑欑欒栾欓𣗋欖榄"
    "欘欘欞棂欽钦歎叹歐欧歟欤歡欢歲岁歷历歸归歿殁殘残殞殒殢殢殤殇殨㱮殫殚殭僵殮殓殯殡殰㱩殲歼殺杀殻壳殼壳毀毁毆殴毊毊"
    "毿毵氂牦氈毡氌氇氣气氫氢氬氩氭氭氳氲氾泛汎泛汙污決决沈沈沒没沖冲況况泝溯洩泄洶汹浹浃浿𬇙涇泾涗涚涼凉淒凄淚泪淥渌"
    "淨净淩凌淪沦淵渊淶涞淺浅淼淼渙涣減减渢沨渦涡測测渾浑湊凑湋𣲗湞浈湧涌湯汤溈沩準准溝沟溡溡溫温溮浉溳涢溼湿滄沧滅灭"
    "滌涤滎荥滙汇滬沪滯滞滲渗滷卤滸浒滻浐滾滚滿满漁渔漊溇漍𬇹漚沤漢汉漣涟漬渍漲涨漵溆漸渐漿浆潁颍潑泼潔洁潕𣲘潙沩潚㴋"
    "潛潜潣潣潤润潯浔潰溃潷滗潿涠澀涩澂澂澅澅澆浇澇涝澐沄澗涧澠渑澤泽澦滪澩泶澫𬇕澬澬澮浍澱淀澾㳠濁浊濃浓濄㳡濆𣸣濕湿"
    "濘泞濚溁濛蒙濜浕濟济濤涛濧㳔濫滥濰潍濱滨濺溅濼泺濾滤濿濿瀂澛瀃瀃瀅滢瀆渎瀇㲿瀉泻瀋沈瀏浏瀕濒瀘泸瀝沥瀟潇瀠潆瀦潴"
    "瀧泷瀨濑瀰弥瀲潋瀾澜灃沣灄滠灍灍灑洒灒𪷽灕漓灘滩灙𣺼灝灏灡㳕灣湾灤滦灧滟灩滟災灾為为烏乌烴烃無无煇煇煉炼煒炜煙烟"
    "煢茕煥焕煩烦煬炀煱㶽熂熂熅煴熉熉熌熌熒荧熓熓熗炝熚熚熡熡熰𬉼熱热熲颎熾炽燀𬊤燁烨燈灯燉炖燒烧燖𬊈燙烫燜焖營营燦灿"
    "燬毁燭烛燴烩燶㶶燻熏燼烬燾焘爃爃爄爄爇爇爍烁爐炉爖爖爛烂爥爥爧爧爭争爲为爺爷爾尔牀床牆墙牘牍牴抵牽牵犇犇犖荦犛牦"
    "犞犞犢犊犧牺狀状狹狭狽狈猌猌猙狰猶犹猻狲獁犸獃呆獄狱獅狮獊獊獎奖獨独獩獩獪狯獫猃獮狝獰狞獱㺍獲获獵猎獷犷獸兽獺獭"
    "獻献獼猕玀猡玁玁珼珼現现琱雕琺珐琿珲瑋玮瑒玚瑣琐瑤瑶瑩莹瑪玛瑲玱瑻瑻瑽瑽璉琏璊𫞩璕𬍤璗𬍡璝璝璡琎璣玑璦瑷璫珰璯㻅"
    "環环璵玙璸瑸璼璼璽玺璾璾璿璇瓄瓄瓅𬍛瓊琼瓏珑瓔璎瓕瓕瓚瓒瓛𤩽甌瓯甕瓮產产産产甦甦甯甯畝亩畢毕畫画異异畵画當当畼畼"
    "疇畴疊叠痙痉痠酸痮痮痾疴瘂痖瘋疯瘍疡瘓痪瘞瘗瘡疮瘧疟瘮瘆瘱瘱瘲疭瘺瘘瘻瘘療疗癆痨癇痫癉瘅癐癐癒愈癘疠癟瘪癡痴癢痒"
    "癤疖癥症癧疬癩癞癬癣癭瘿癮瘾癰痈癱瘫癲癫發发皁皂皚皑皟皟皰疱皸皲皺皱盃杯盜盗盞盏盡尽監监盤盘盧卢盨盨盪荡眝眝眞真"
    "眥眦眾众睍𪾢睏困睜睁睞睐瞘眍瞜䁖瞞瞒瞤瞤瞭瞭瞶瞆瞼睑矇蒙矉矉矑矑矓眬矚瞩矯矫硃朱硜硁硤硖硨砗硯砚碕埼碙碙碩硕碭砀"
    "碸砜確确碼码碽䂵磑硙磚砖磠硵磣碜磧碛磯矶磽硗磾䃅礄硚礆礆礎础礐𬒈礒礒礙碍礦矿礪砺礫砾礬矾礮礮礱砻祇祇祕秘祿禄禍祸"
    "禎祯禕祎禡祃禦御禪禅禮礼禰祢禱祷禿秃秈籼稅税稈秆稏䅉稜棱稟禀種种稱称穀谷穇䅟穌稣積积穎颖穠秾穡穑穢秽穩稳穫获穭穞"
    "窩窝窪洼窮穷窯窑窵窎窶窭窺窥竄窜竅窍竇窦竈灶竊窃竚竚竪竖竱竱競竞筆笔筍笋筦筦筧笕筴䇲箇个箋笺箏筝箚札節节範范築筑"
    "篋箧篔筼篘篘篠筿篢𬕂篤笃篩筛篳筚篸𥮾簀箦簂簂簍篓簑蓑簞箪簡简簢簢簣篑簫箫簹筜簽签簾帘籃篮籅𥫣籋籋籌筹籔䉤籙箓籛篯"
    "籜箨籟籁籠笼籤签籩笾籪簖籬篱籮箩籲吁粵粤糉粽糝糁糞粪糧粮糰团糲粝糴籴糶粜糹纟糺糺糾纠紀纪紂纣紃𬘓約约紅红紆纡紇纥"
    "紈纨紉纫紋纹納纳紐纽紓纾純纯紕纰紖纼紗纱紘纮紙纸級级紛纷紜纭紝纴紞𬘘紟紟紡纺紬䌷紮扎細细紱绂紲绁紳绅紵纻紹绍紺绀"
    "紼绋紿绐絀绌絁絁終终絃弦組组絅䌹絆绊絍絍絎绗結结絕绝絙絙絛绦絜絜絝绔絞绞絡络絢绚絥絥給给絧絧絨绒絪𬘡絰绖統统絲丝"
    "絳绛絶绝絹绢絺𫄨綀綀綁绑綃绡綄𬘫綆绠綇綇綈绨綉绣綋綋綌绤綎𬘩綏绥綐䌼綑捆經经綖𫄧綜综綝𬘭綞缍綟綟綠绿綡𫟅綢绸綣绻"
    "綧𬘯綪𬘬綫线綬绶維维綯绹綰绾綱纲網网綳绷綴缀綵彩綸纶綹绺綺绮綻绽綽绰綾绫綿绵緄绲緇缁緊紧緋绯緍緍緑绿緒绪緓绬緔绱"
    "緗缃緘缄緙缂線线緝缉緞缎緟緟締缔緡缗緣缘緤緤緦缌編编緩缓緬缅緮緮緯纬緰緰緱缑緲缈練练緶缏緷緷緸緸緹缇緻致緼缊縈萦"
    "縉缙縊缢縋缒縍縍縎縎縐绉縑缣縕缊縗缞縛缚縝缜縞缟縟缛縣县縧绦縫缝縬縬縭缡縮缩縯𬙂縰縰縱纵縲缧縳䌸縴纤縵缦縶絷縷缕"
    "縸縸縹缥縺縺總总績绩繂繂繃绷繅缫繆缪繈繈繏繏繐繐繒缯繓繓織织繕缮繚缭繞绕繟繟繡绣繢缋繨繨繩绳繪绘繫系繬繬繭茧繮缰"
    "繯缳繰缲繳缴繶𫄷繷繷繸䍁繹绎繻𦈡繼继繽缤繾缱繿䍀纁𫄸纆𬙊纇颣纈缬纊纩續续纍累纏缠纓缨纔才纕𬙋纖纤纗纗纘缵纚纚纜缆"
    "缽钵罃䓨罈坛罌罂罎坛罰罚罵骂罷罢羅罗羆罴羈羁羋芈羣群羥羟羨羡義义羵羵羶膻習习翫玩翬翚翹翘翽翙耑耑耬耧耮耢聖圣聞闻"
    "聯联聰聪聲声聳耸聵聩聶聂職职聹聍聻聻聽听聾聋肅肃脅胁脈脉脛胫脣唇脥脥脩修脫脱脹胀腎肾腖胨腡脶腦脑腪腪腫肿腳脚腸肠"
    "膃腽膕腘膚肤膞䏝膠胶膢𦝼膩腻膹膹膽胆膾脍膿脓臉脸臍脐臏膑臗臗臘腊臚胪臟脏臠脔臢臜臥卧臨临臺台與与興兴舉举舊旧舖铺"
    "舘馆艙舱艣艣艤舣艦舰艫舻艱艰艷艳芻刍苧苎茲兹荊荆莊庄莖茎莢荚莧苋菉菉菕菕華华菴庵菸烟萇苌萊莱萬万萴荝萵莴葉叶葒荭"
    "葝葝葤荮葦苇葯药葷荤蒍𫇭蒐搜蒓莼蒔莳蒕蒀蒞莅蒭蒭蒼苍蓀荪蓆席蓋盖蓧蓧蓮莲蓯苁蓴莼蓽荜蔄𬜬蔔卜蔘参蔞蒌蔣蒋蔥葱蔦茑"
    "蔭荫蔯𫈟蔿𫇭蕁荨蕆蒇蕎荞蕒荬蕓芸蕕莸蕘荛蕝蕝蕢蒉蕩荡蕪芜蕭萧蕳蕳蕷蓣蕽蕽薀蕰薆薆薈荟薊蓟薌芗薑姜薔蔷薘荙薟莶薦荐"
    "薩萨薳薳薴苧薵䓓薹苔薺荠藉藉藍蓝藎荩藝艺藥药藪薮藭䓖藴蕴藶苈藷藷藹蔼藺蔺蘀萚蘄蕲蘆芦蘇苏蘊蕴蘋苹蘚藓蘞蔹蘟𦻕蘢茏"
    "蘭兰蘺蓠蘿萝虆蔂虉𬟁處处虛虚虜虏號号虧亏虯虬蛺蛱蛻蜕蜆蚬蝀𬟽蝕蚀蝟猬蝦虾蝨虱蝸蜗螄蛳螞蚂螢萤螮䗖螻蝼螿螀蟂蟂蟄蛰"
    "蟈蝈蟎螨蟘蟘蟜蟜蟣虮蟬蝉蟯蛲蟲虫蟳𫊻蟶蛏蟻蚁蠀蠀蠁蚃蠅蝇蠆虿蠍蝎蠐蛴蠑蝾蠔蚝蠙蠙蠟蜡蠣蛎蠦蠦蠨蟏蠱蛊蠶蚕蠻蛮蠾蠾"
    "衆众衊蔑術术衕同衚胡衛卫衝冲衹衹袞衮袷夹裊袅裏里補补裝装裡里製制複复褌裈褘袆褲裤褳裢褸褛褻亵襀𫌀襇裥襉裥襏袯襓襓"
    "襖袄襗襗襘襘襝裣襠裆襤褴襪袜襬摆襯衬襰襰襲袭襴襕襵襵覆覆覈核見见覎觃規规覓觅視视覘觇覛覛覡觋覥觍覦觎親亲覬觊覯觏"
    "覲觐覷觑覹覹覺觉覼覼覽览覿觌觀观觴觞觶觯觸触訁讠訂订訃讣計计訊讯訌讧討讨訏𬣙訐讦訑訑訒讱訓训訕讪訖讫託托記记訛讹"
    "訜訜訝讶訞訞訟讼訢䜣訣诀訥讷訨訨訩讻訪访設设許许訴诉訶诃診诊註注証证詀𧮪詁诂詆诋詊詊詎讵詐诈詑詑詒诒詓詓詔诏評评"
    "詖诐詗诇詘诎詛诅詝𬣞詞词詠咏詡诩詢询詣诣試试詩诗詪𬣳詫诧詬诟詭诡詮诠詰诘話话該该詳详詵诜詷𫍣詼诙詿诖誂誂誄诔誅诛"
    "誆诓誇夸誋誋誌志認认誑诳誒诶誕诞誘诱誚诮語语誠诚誡诫誣诬誤误誥诰誦诵誨诲說说誫誫説说誰谁課课誳誳誴誴誶谇誷誷誹诽"
    "誺誺誼谊誾訚調调諂谄諄谆談谈諉诿請请諍诤諏诹諑诼諒谅諓𬣡論论諗谂諛谀諜谍諝谞諞谝諟𬤊諡谥諢诨諣諣諤谔諥諥諦谛諧谐"
    "諫谏諭谕諮咨諯諯諰諰諱讳諲𬤇諳谙諴𫍯諶谌諷讽諸诸諺谚諼谖諾诺謀谋謁谒謂谓謄誊謅诌謆謆謉謉謊谎謎谜謏𫍲謐谧謔谑謖谡"
    "謗谤謙谦謚谥講讲謝谢謠谣謡谣謨谟謫谪謬谬謭谫謯謯謱謱謳讴謸謸謹谨謾谩譁哗譂譂譅譅譆譆證证譊譊譎谲譏讥譑譑譓𬤝譖谮"
    "識识譙谯譚谭譜谱譞𫍽譟噪譨譨譫谵譭毁譯译議议譴谴護护譸诪譽誉譾谫讀读讅谉變变讋詟讌䜩讎雠讒谗讓让讕谰讖谶讚赞讜谠"
    "讞谳谿溪豈岂豎竖豐丰豔艳豬猪豵豵豶豮貍狸貓猫貗貗貙䝙貝贝貞贞貟贠負负財财貢贡貧贫貨货販贩貪贪貫贯責责貯贮貰贳貲赀"
    "貳贰貴贵貶贬買买貸贷貺贶費费貼贴貽贻貿贸賀贺賁贲賂赂賃赁賄贿賅赅資资賈贾賊贼賑赈賒赊賓宾賕赇賙赒賚赉賜赐賝賝賞赏"
    "賟賟賠赔賡赓賢贤賣卖賤贱賦赋賧赕質质賫赍賬账賭赌賰䞐賴赖賵赗賺赚賻赙購购賽赛賾赜贃贃贄贽贅赘贇赟贈赠贉贉贊赞贋赝"
    "贍赡贏赢贐赆贑贑贓赃贔赑贖赎贗赝贚贚贛赣贜赃赬赪趕赶趙赵趨趋趲趱跡迹踐践踰逾踴踊蹌跄蹔蹔蹕跸蹟迹蹠跖蹣蹒蹤踪蹳蹳"
    "蹺跷蹻蹻躂跶躉趸躊踌躋跻躍跃躎䟢躑踯躒跞躓踬躕蹰躘躘躚跹躝躝躡蹑躥蹿躦躜躪躏軀躯軉軉車车軋轧軌轨軍军軏𫐄軑轪軒轩"
    "軔轫軕軕軗軗軛轭軜軜軝𬨂軟软軤轷軨軨軫轸軬軬軲轱軷軷軸轴軹轵軺轺軻轲軼轶軾轼軿軿較较輄𨐈輅辂輇辁輈辀載载輊轾輋𪨶"
    "輒辄輓挽輔辅輕轻輖輖輗𫐐輛辆輜辎輝辉輞辋輟辍輢輢輥辊輦辇輨輨輩辈輪轮輬辌輮𫐓輯辑輳辏輶𬨎輷輷輸输輻辐輼辒輾辗輿舆"
    "轀辒轂毂轄辖轅辕轆辘轇轇轉转轊轊轍辙轎轿轐轐轔辚轗轗轟轰轠轠轡辔轢轹轣轣轤轳辦办辭辞辮辫辯辩農农迴回迺迺逕径這这"
    "連连週周進进遊游運运過过達达違违遙遥遜逊遞递遠远遡溯適适遱遱遲迟遶绕遷迁選选遺遗遼辽邁迈還还邇迩邊边邏逻邐逦邨邨"
    "郟郏郵邮鄆郓鄉乡鄒邹鄔邬鄖郧鄟鄟鄧邓鄩𬩽鄭郑鄰邻鄲郸鄳𫑡鄴邺鄶郐鄺邝酇酂酈郦醃腌醖酝醜丑醞酝醟蒏醣糖醫医醬酱醱酦"
    "醲𬪩醶醶釀酿釁衅釃酾釅酽釋释釐厘釒钅釓钆釔钇釕钌釗钊釘钉釙钋釚釚針针釟釟釣钓釤钐釦扣釧钏釨釨釩钒釲釲釳釳釴𬬩釵钗"
    "釷钍釹钕釺钎釾䥺釿𬬱鈀钯鈁钫鈃钘鈄钭鈅钥鈆鈆鈇𫓧鈈钚鈉钠鈋鈋鈍钝鈎钩鈐钤鈑钣鈒钑鈔钞鈕钮鈖鈖鈗鈗鈛鈛鈞钧鈠鈠鈡钟"
    "鈣钙鈥钬鈦钛鈧钪鈮铌鈯鈯鈰铈鈲鈲鈳钶鈴铃鈷钴鈸钹鈹铍鈺钰鈽钸鈾铀鈿钿鉀钾鉁鉁鉅巨鉆钻鉈铊鉉铉鉊𬬿鉋铇鉍铋鉑铂鉔鉔"
    "鉕钷鉗钳鉚铆鉛铅鉝𫟷鉞钺鉠鉠鉢钵鉤钩鉥𬬸鉦钲鉧𬭁鉬钼鉭钽鉮𬬹鉳锫鉶铏鉷𫟹鉸铰鉺铒鉻铬鉽鉽鉾鉾鉿铪銀银銁銁銂銂銃铳"
    "銅铜銈𫓯銊銊銍铚銏銏銑铣銓铨銖铢銘铭銚铫銛铦銜衔銠铑銣铷銥铱銦铟銨铵銩铥銪铕銫铯銬铐銱铞銳锐銶𨱇銷销銹锈銻锑銼锉"
    "鋁铝鋂鋂鋃锒鋅锌鋇钡鋉鋉鋌铤鋏铗鋐𬭎鋒锋鋗𫓶鋙铻鋝锊鋟锓鋠鋠鋣铘鋤锄鋥锃鋦锔鋨锇鋩铓鋪铺鋭锐鋮铖鋯锆鋰锂鋱铽鋶锍"
    "鋸锯鋹𬬮鋼钢錀𬬭錁锞錂錂錄录錆锖錇锫錈锩錏铔錐锥錒锕錕锟錘锤錙锱錚铮錛锛錜錜錝錝錞𬭚錟锬錠锭錡锜錢钱錤𫓹錥錥錦锦"
    "錨锚錩锠錫锡錮锢錯错録录錳锰錶表錸铼錼镎錽錽鍀锝鍁锨鍃锪鍄鍄鍅钫鍆钔鍇锴鍈锳鍉鍉鍊炼鍋锅鍍镀鍒鍒鍔锷鍘铡鍚钖鍛锻"
    "鍠锽鍤锸鍥锲鍩锘鍬锹鍭𬭤鍮鍮鍰锾鍵键鍶锶鍺锗鍼针鍾钟鎂镁鎄锿鎇镅鎈鎈鎊镑鎌镰鎍鎍鎓𬭩鎔镕鎖锁鎘镉鎙鎙鎚锤鎛镈鎝𨱏"
    "鎞鎞鎡镃鎢钨鎣蓥鎦镏鎧铠鎩铩鎪锼鎬镐鎭镇鎮镇鎯鎯鎰镒鎲镋鎳镍鎵镓鎶鿔鎷鎷鎸镌鎿镎鏃镞鏆鏆鏇旋鏈链鏉鏉鏌镆鏍镙鏏𬭬"
    "鏐镠鏑镝鏗铿鏘锵鏚鏚鏜镗鏝镘鏞镛鏟铲鏡镜鏢镖鏤镂鏥鏥鏦鏦鏨錾鏰镚鏵铧鏷镤鏹镪鏺䥽鏻𬭸鏽锈鏾鏾鐃铙鐄𨱑鐇𫔍鐈鐈鐋铴"
    "鐍𫔎鐎鐎鐏𨱔鐐镣鐒铹鐓镦鐔镡鐘钟鐙镫鐝镢鐠镨鐥䦅鐦锎鐧锏鐨镄鐩𬭼鐪鐪鐫镌鐮镰鐯䦃鐲镯鐳镭鐵铁鐶镮鐸铎鐺铛鐼鐼鐽𫟼"
    "鐿镱鑀鑀鑄铸鑉鑉鑊镬鑌镔鑑鉴鑒鉴鑔镲鑕锧鑞镴鑠铄鑣镳鑥镥鑪𬬻鑭镧鑰钥鑱镵鑲镶鑴鑴鑷镊鑹镩鑼锣鑽钻鑾銮鑿凿钁镢钂镋"
    "長长門门閂闩閃闪閆闫閈闬閉闭開开閌闶閍閍閎闳閏闰閐閐閑闲閒闲間间閔闵閗閗閘闸閝閝閞閞閡阂閣阁閤合閥阀閨闺閩闽閫阃"
    "閬阆閭闾閱阅閲阅閵閵閶阊閹阉閻阎閼阏閽阍閾阈閿阌闃阒闆板闇暗闈闱闉𬮱闊阔闋阕闌阑闍阇闐阗闑𫔶闒阘闓闿闔阖闕阙闖闯"
    "關关闞阚闠阓闡阐闢辟闤阛闥闼阪阪陘陉陝陕陞升陣阵陰阴陳陈陸陆陽阳隉陧隊队階阶隑𬮿隕陨際际隤𬯎隨随險险隮𬯀隯陦隱隐"
    "隴陇隸隶隻只雋隽雖虽雙双雛雏雜杂雞鸡離离難难雲云電电霑沾霢霡霣霣霧雾霼霼霽霁靂雳靄霭靆叇靈灵靉叆靚靓靜静靝靔靦腼"
    "靧靧靨靥鞏巩鞝绱鞦秋鞽鞒鞾鞾韁缰韃鞑韆千韉鞯韋韦韌韧韍韨韓韩韙韪韚韚韛韛韜韬韝鞲韞韫韠韠韻韵響响頁页頂顶頃顷項项"
    "順顺頇顸須须頊顼頌颂頍𫠆頎颀頏颃預预頑顽頒颁頓顿頔𬱖頗颇領领頜颌頠𬱟頡颉頤颐頦颏頫𫖯頭头頮颒頰颊頲颋頴颕頵𫖳頷颔"
    "頸颈頹颓頻频頽颓顂顂顃顃顅顅顆颗題题額额顎颚顏颜顒颙顓颛顔颜顗𫖮願愿顙颡顛颠類类顢颟顣顣顥颢顧顾顫颤顬颥顯显顰颦"
    "顱颅顳颞顴颧風风颭飐颮飑颯飒颰颰颱台颳刮颶飓颷颷颸飔颺飏颻飖颼飕颾颾飀飗飄飘飆飙飈飚飋飋飛飞飠饣飢饥飣饤飥饦飦飦"
    "飩饨飪饪飫饫飭饬飯饭飱飧飲饮飴饴飵飵飶飶飼饲飽饱飾饰飿饳餃饺餄饸餅饼餈糍餉饷養养餌饵餎饹餏饻餑饽餒馁餓饿餔餔餕馂"
    "餖饾餗𫗧餘余餚肴餛馄餜馃餞饯餡馅餦餦餧餧館馆餪餪餫餫餬糊餭餭餱糇餳饧餵喂餶馉餷馇餸𩠌餺馎餼饩餾馏餿馊饁馌饃馍饅馒"
    "饈馐饉馑饊馓饋馈饌馔饑饥饒饶饗飨饘𫗴饜餍饞馋饟饟饠饠饢馕馬马馭驭馮冯馯馯馱驮馳驰馴驯馹驲馼𫘜駁驳駃𫘝駉𬳶駊駊駎駎"
    "駐驻駑驽駒驹駓𬳵駔驵駕驾駘骀駙驸駚駚駛驶駝驼駞駞駟驷駡骂駢骈駤駤駧駧駩駩駪𬳽駫駫駭骇駰骃駱骆駶駶駸骎駻駻駼𬳿駿骏"
    "騁骋騂骍騃騃騄𫘧騅骓騉騉騊𫘦騌骔騍骒騎骑騏骐騑𬴂騔騔騖骛騙骗騚騚騜騜騝騝騞𬴃騟騟騠𫘨騤骙騧䯄騪騪騫骞騭骘騮骝騰腾"
    "騱𫘬騴騴騵𫘪騶驺騷骚騸骟騻騻騼騼騾骡驀蓦驁骜驂骖驃骠驄骢驅驱驊骅驋驋驌骕驍骁驎𬴊驏骣驓驓驕骄驗验驙驙驚惊驛驿驟骤"
    "驢驴驤骧驥骥驦骦驨驨驪骊驫骉骯肮髏髅髒脏體体髕髌髖髋髮发鬆松鬍胡鬖鬖鬚须鬠鬠鬢鬓鬥斗鬧闹鬨哄鬩阋鬮阄鬱郁鬹鬶魎魉"
    "魘魇魚鱼魛鱽魟𫚉魢鱾魥魥魦魦魨鲀魯鲁魴鲂魵魵魷鱿魺鲄魽魽鮀𬶍鮁鲅鮃鲆鮄鮄鮅鮅鮆𫚖鮈𬶋鮊鲌鮋鲉鮍鲏鮎鲇鮐鲐鮑鲍鮒鲋"
    "鮓鲊鮚鲒鮜鲘鮝鲞鮞鲕鮟𩽾鮠𬶏鮡𬶐鮣䲟鮤鮤鮦鲖鮪鲔鮫鲛鮭鲑鮮鲜鮯鮯鮰鮰鮳鲓鮵鮵鮶鲪鮸𩾃鮺鲝鮿鮿鯀鲧鯁鲠鯄鯄鯆鯆鯇鲩"
    "鯉鲤鯊鲨鯒鲬鯔鲻鯕鲯鯖鲭鯗鲞鯛鲷鯝鲴鯞鯞鯡鲱鯢鲵鯤鲲鯧鲳鯨鲸鯪鲮鯫鲰鯬鯬鯰鲶鯱鯱鯴鲺鯶鯶鯷鳀鯻𬶟鯽鲫鯾鯾鯿鳊鰁鳈"
    "鰂鲗鰃鳂鰆䲠鰈鲽鰉鳇鰊𬶠鰋鰋鰌䲡鰍鳅鰏鲾鰐鳄鰑鰑鰒鳆鰓鳃鰕鰕鰛鳁鰜鳒鰟鳑鰠鳋鰣鲥鰤𫚕鰥鳏鰦鰦鰧䲢鰨鳎鰩鳐鰫鰫鰭鳍"
    "鰮鳁鰱鲢鰲鳌鰳鳓鰵鳘鰶𬶭鰷鲦鰹鲣鰺鲹鰻鳗鰼鳛鰽鰽鰾鳔鱀𬶨鱂鳉鱄鱄鱅鳙鱆鱆鱇𩾌鱈鳕鱉鳖鱊鱊鱒鳟鱔鳝鱖鳜鱗鳞鱘鲟鱚𬶮"
    "鱝鲼鱟鲎鱠鲙鱢鱢鱣鳣鱤鳡鱧鳢鱨鲿鱭鲚鱮鱮鱯鳠鱲𫚭鱷鳄鱸鲈鱺鲡鳥鸟鳧凫鳩鸠鳬凫鳲鸤鳳凤鳴鸣鳶鸢鳷鳷鳼鳼鳽鳽鳾䴓鴀鴀"
    "鴃鴃鴅鴅鴆鸩鴇鸨鴉鸦鴐鴐鴒鸰鴔鴔鴕鸵鴗鴗鴛鸳鴜鴜鴝鸲鴞鸮鴟鸱鴣鸪鴥鴥鴦鸯鴨鸭鴮鴮鴯鸸鴰鸹鴲鴲鴳鴳鴴鸻鴷䴕鴻鸿鴽鴽"
    "鴿鸽鵁䴔鵂鸺鵃鸼鵊鵊鵏𬷕鵐鹀鵑鹃鵒鹆鵓鹁鵚鵚鵜鹈鵝鹅鵟𫛭鵠鹄鵡鹉鵧鵧鵩鵩鵪鹌鵫鵫鵬鹏鵮鹐鵯鹎鵰雕鵲鹊鵷鹓鵾鹍鶄䴖"
    "鶇鸫鶉鹑鶊鹒鶌鶌鶒鶒鶓鹋鶖鹙鶗鶗鶘鹕鶚鹗鶠𬸘鶡鹖鶥鹛鶦鶦鶩鹜鶪䴗鶬鸧鶭鶭鶯莺鶰鶰鶱𬸣鶲鹟鶴鹤鶹鹠鶺鹡鶻鹘鶼鹣鶿鹚"
    "鷀鹚鷁鹢鷂鹞鷄鸡鷅鷅鷉䴘鷊鹝鷐鷐鷓鹧鷔鷔鷖鹥鷗鸥鷙鸷鷚鹨鷟𬸦鷣鷣鷤鷤鷥鸶鷦鹪鷨鷨鷩鷩鷫鹔鷭𬸪鷯鹩鷲鹫鷳鹇鷴鹇鷷鷷"
    "鷸鹬鷹鹰鷺鹭鷽鸴鷿鷿鸂㶉鸇鹯鸊䴙鸋鸋鸌鹱鸏鹲鸑𬸚鸕鸬鸗鸗鸘鹴鸚鹦鸛鹳鸝鹂鸞鸾鹵卤鹹咸鹺鹾鹼碱鹽盐麗丽麥麦麨麨麩麸"
    "麪面麫面麬𤿲麯曲麲麲麳𪎌麴曲麵面麷麷麼么麽么黃黄黌黉點点黨党黲黪黴霉黶黡黷黩黽黾黿鼋鼂鼌鼉鼍鼕冬鼴鼹齊齐齋斋齎赍"
    "齏齑齒齿齔龀齕龁齗龂齘𬹼齙龅齜龇齟龃齠龆齡龄齣出齦龈齧啮齩齩齪龊齬龉齭齭齮𬺈齯𫠜齰齰齲龋齴齴齶腭齷龌齼𬺓齾齾龍龙"
    "龎厐龐庞龑䶮龓龓龔龚龕龛龜龟龢龢龭龭龯龯鿁䜤鿓鿒𠁞𠀾𠌥𠌥𠏢𠏢𠐊𠐊𠗣㓆𠞆𠞆𠠎𠠎𠬙𠬙𠼤𠼤𠽃𠽃𠿕𠿕𡂡𡂡𡃄𡃄𡃕𠴛𡃤𡃤𡄔𡄔"
    "𡄣𡄣𡅏𠲥𡅯𡅯𡑍𫭼𡑭𡋗𡓁𡓁𡓾𡋀𡔖𡍣𡞵㛟𡟫𡟫𡠹㛿𡢃㛠𡮉𡭜𡮣𡭬𡳳𡳃𡸗𡸗𡹬𡹬𡻕岁𡽗𡽗𡾱㟜𡿖𡿖𢍰𢍰𢠼𢠼𢣐𢣐𢣚𢘝𢣭𢣭𢤩𢤩𢤱𢤱"
    "𢤿𢤿𢯷𢯷𢶒𢶒𢶫𢫞𢷮𢷮𢹿𢬦𢺳𢺳𣈶暅𣋋𣋋𣍐𣍐𣙎㭣𣜬𣜬𣝕𣝕𣞻𣘓𣠩𣞎𣠲𣑶𣯩𣯩𣯴𣯴𣯶毶𣽏𣽏𣾷㳢𣿉𣿉𤁣𣺽𤄷𤄷𤅶𣷷𤑳𤑳𤑹𤑹𤒎𤒎"
    "𤒻𤒻𤓌𤓌𤓎𤓎𤓩𤊰𤘀𤘀𤛮𤛮𤛱𤛱𤜆𤜆𤠮𤠮𤢟𤢟𤢻𤢻𤩂𤩂𤪺㻘𤫩㻏𤬅𤬅𤳷𤳷𤳸𤳄𤷃𤷃𤸫𤸫𤺔𤺔𥊝𥅿𥌃𥅘𥏝𥏝𥕥𥐰𥖅𥐯𥖲𥖲𥗇𥗇𥗽𬒗"
    "𥜐𥜐𥜰𥜰𥞵𥞵𥢢䅪𥢶𥢶𥢷𥢷𥨐𥨐𥪂𥪂𥯤𥯤𥴨𥴨𥴼𥴼𥵃𥵃𥵊𥵊𥶽𥶽𥸠𥮋𥻦𥻦𥼽𥹥𥽖𥽖𥾯𥾯𥿊𥿊𦀖𦀖𦂅𦂅𦃄𦃄𦃩𦃩𦅇𦅇𦅈𦅈𦆲𦆲𦒀𦒀"
    "𦔖𦔖𦘧𡳒𦟼𦟼𦠅𦠅𦡝𦡝𦢈𦢈𦣎𦟗𦧺𦧺𦪙䑽𦪽𦪽𦱌𦱌𦾟𦾟𧎈𧎈𧒯𧒯𧔥𧔥𧕟𧕟𧜗䘞𧜵䙊𧝞䘛𧞫𧞫𧟀𧝧𧡴𧡴𧢄𧢄𧦝𧦝𧦧𧦧𧩕𧩕𧩙䜥𧩼𧩼"
    "𧫝𧫝𧬤𧬤𧭈𧭈𧭹𧭹𧳟𧳟𧵳䞌𧶔𧶔𧶧䞎𧷎𧷎𧸘𧸘𧹈𧹈𧽯𧽯𨂐𨂐𨄣𨄣𨅍𨅍𨆪𨆪𨇁𨇁𨇞𨇞𨇤𨇤𨇰𨇰𨇽𨇽𨈊𨈊𨈌𨈌𨊰䢀𨊸䢁𨊻𨊻𨋢䢂𨌈𨌈"
    "𨍰𨍰𨎌𨎌𨎮𨎮𨏠𨏠𨏥𨏥𨞺𨞺𨟊𨟊𨢿𨢿𨣈𨣈𨣞𨣞𨣧𨣧𨤻𨤰𨥛𨥛𨥟𨥟𨦫䦀𨧀𬭊𨧜䦁𨧰𨧰𨧱𨧱𨨏𬭛𨨛𨨛𨨢𨨢𨩰𨩰𨪕𨪕𨫒𨫒𨬖𨬖𨭆𬭶𨭎𬭳"
    "𨭖𨭖𨭸𨭸𨮂𨮂𨮳𨮳𨯅䥿𨯟𨯟𨰃𨰃𨰋𨰋𨰥𨰥𨰲𨰲𨲳𨲳𨳑𨳑𨳕𨳕𨴗𨴗𨴹𨴹𨵩𨵩𨵸𨵸𨶀𨶀𨶏𨶏𨶮𨶮𨶲𨶲𨷲𨷲𨼳𨼳𨽏𨽏𩀨𩀨𩅙𩅙𩎖𩎖𩎢𩎢"
    "𩏂𩏂𩏠𩏠𩏪𩏪𩏷𩏷𩑔𩑔𩒎𩒎𩓣𩓣𩓥𩓥𩔑𩔑𩔳𩔳𩖰𩖰𩗀𩗀𩗓𩗓𩗴𩗴𩘀𩘀𩘝𩘝𩘹𩘹𩘺𩘺𩙈𩙈𩚛𩚛𩚥𩚥𩚩𩚩𩚵𩚵𩛆𩛆𩛌𩛌𩛡𩛡𩛩𩛩𩜇𩜇"
    "𩜦𩜦𩜵𩜵𩝔𩝔𩝽𩝽𩞄𩞄𩞦𩞦𩞯䭪𩟐𩟐𩟗𩟗𩠴𩠠𩡣𩡣𩡺𩡺𩢡𩢡𩢴𩢴𩢸𩢸𩢾𩢾𩣏𩣏𩣑䯃𩣫𩣫𩣵𩣵𩣺𩣺𩤊𩤊𩤙𩤙𩤲𩤲𩤸𩤸𩥄𩥄𩥇𩥇𩥉𩥉"
    "𩥑𩥑𩦠𩦠𩧆𩧆𩭙𩭙𩯁𩯁𩯳𩯳𩰀𩰀𩰹𩰹𩳤𩳤𩴵𩴵𩵦𩵦𩵩𩵩𩵹𩵹𩶁𩶁𩶘䲞𩶰𩶰𩶱𩶱𩷰𩷰𩸃𩸃𩸄𩸄𩸡𩸡𩸦𩸦𩻗𩻗𩻬𩻬𩻮𩻮𩼶𩼶𩽇𩽇𩿅𩿅"
    "𩿤𩿤𩿪𩿪𪀖𪀖𪀦𪀦𪀾𪀾𪁈𪁈𪁖𪁖𪂆𪂆𪃍𪃍𪃏𪃏𪃒𪃒𪃧𪃧𪄆𪄆𪄕𪄕𪅂𪅂𪆷𪆷𪇳𪇳𪈼𪈼𪉸𪉸𪋿𪋿𪌭𪌭𪍠𪍠𪓰𪓰𪔵𪔵𪘀𪘀𪘯𪘯𪙏𪙏𪟖𪟖"
    "𪷓𪷓𫒡𫒡𫜦𫜦𰻞𰻝"
)

# 反方向的简体转繁体单字表，打包时把简体文本写回繁体封包用，取自同仓库 STCharacters.txt。
ST_PAIRS = (
    "㐷傌㐹㑶㐹㐹㐽偑㑇㑳㑈倲㑔㑯㑩儸㓆𠗣㓥劏㓰劃㔉劚㖊噚㖞喎㘎㘚㚯㜄㛀媰㛟𡞵㛠𡢃㛣㜏㛤孋㛿𡠹㟆㠏㟜𡾱㟥嵾㡎幓㤘㥮㤽懤"
    "㥪慺㧏掆㧐㩳㧑撝㧟擓㧰擽㨫㩜㭎棡㭏椲㭣𣙎㭤樢㭴樫㱩殰㱮殨㲿瀇㳔濧㳕灡㳠澾㳡濄㳢𣾷㳽瀰㴋潚㶉鸂㶶燶㶽煱㺍獱㻅璯㻏𤫩"
    "㻘𤪺䀥䁻䁖瞜䂵碽䃅磾䅉稏䅟穇䅪𥢢䇲筴䉤籔䌶䊷䌷紬䌸縳䌹絅䌺䋙䌻䋚䌼綐䌽綵䌾䋻䌿䋹䍀繿䍁繸䍠䍦䎬䎱䏝膞䑽𦪙䓓薵䓕薳"
    "䓖藭䓨罃䗖螮䘛𧝞䘞𧜗䙊𧜵䙌䙡䙓襬䜣訢䜤鿁䜥𧩙䜧䜀䜩讌䝙貙䞌𧵳䞍䝼䞎𧶧䞐賰䟢躎䢀𨊰䢁𨊸䢂𨋢䥺釾䥽鏺䥾䥱䥿𨯅䦀𨦫䦁𨧜"
    "䦂䥇䦃鐯䦅鐥䦆钁䦶䦛䦷䦟䩄靦䭪𩞯䯃𩣑䯄騧䯅䯀䲝䱽䲞𩶘䲟鮣䲠鰆䲡鰌䲢鰧䲣䱷䴓鳾䴔鵁䴕鴷䴖鶄䴗鶪䴘鷉䴙鸊䶮龑万萬万万"
    "与與丑醜丑丑专專业業丛叢东東丝絲丢丟两兩严嚴丧喪个個个箇丰豐丰丰临臨为爲丽麗举舉么麼义義乌烏乐樂乔喬习習乡鄉书書"
    "买買乱亂了了了瞭争爭于於于于亏虧云雲云云亘亙亘亘亚亞产產亩畝亲親亵褻亸嚲亿億仅僅仆僕仆仆仇仇仇讎从從仑侖仑崙仓倉"
    "仪儀们們价價价价仿仿仿彷众衆优優伙夥伙伙会會伛傴伞傘伟偉传傳伡俥伣俔伤傷伥倀伦倫伧傖伪僞伫佇体體余餘余余佛佛佛彿"
    "佣傭佣佣佥僉侠俠侣侶侥僥侦偵侧側侨僑侩儈侪儕侬儂侭儘俊俊俊儁俣俁俦儔俨儼俩倆俪儷俫倈俭儉修修修脩借借借藉债債倾傾"
    "偬傯偻僂偾僨偿償傤儎傥儻傧儐储儲傩儺僵僵僵殭儿兒克克克剋兑兌兖兗党黨党党兰蘭关關兴興具具具俱兹茲养養兽獸冁囅内內"
    "冈岡册冊写寫军軍农農冢冢冢塚冬冬冬鼕冯馮冲衝冲沖决決况況冻凍净淨凄悽凄淒准準准准凉涼凌凌凌淩减減凑湊凛凜几幾几几"
    "凤鳳凫鳧凭憑凯凱凶兇凶凶出出出齣击擊凿鑿刍芻划劃划划刘劉则則刚剛创創删刪别別别彆刬剗刭剄刮刮刮颳制制制製刹剎刽劊"
    "刾㓨刿劌剀剴剂劑剐剮剑劍剥剝剧劇劝勸办辦务務劢勱动動励勵劲勁劳勞势勢勋勳勋勛勚勩匀勻匦匭匮匱区區医醫千千千韆升升"
    "升昇华華协協单單卖賣卜卜卜蔔占佔占占卢盧卤滷卤鹵卧臥卫衛却卻卷卷卷捲卺巹厂廠厂厂厅廳历歷历曆厉厲压壓厌厭厍厙厐龎"
    "厕廁厘釐厘厘厢廂厣厴厦廈厨廚厩廄厮廝县縣叁叄参參参蔘叆靉叇靆双雙发發发髮变變叙敘叠疊只只只隻只祇台臺台檯台颱台台"
    "叶葉叶叶号號叹嘆叹歎叽嘰吁籲吁吁吃喫吃吃合合合閤吊吊吊弔同同同衕后後后后向向向嚮向曏吓嚇吕呂吗嗎吣吣吣唚吨噸听聽"
    "启啓吴吳呆呆呆待呐吶呒嘸呓囈呕嘔呖嚦呗唄员員呙咼呛嗆呜嗚周周周週周賙咏詠咙嚨咛嚀咝噝咤吒咨諮咨咨咸鹹咸咸咽咽咽嚥"
    "哄哄哄鬨响響哑啞哒噠哓嘵哔嗶哕噦哗譁哗嘩哙噲哜嚌哝噥哟喲唇脣唇唇唛嘜唝嗊唠嘮唡啢唢嗩唤喚啧嘖啬嗇啭囀啮齧啮嚙啯嘓"
    "啰囉啴嘽啸嘯喂喂喂餵喷噴喽嘍喾嚳嗫囁嗳噯嘘噓嘤嚶嘱囑噜嚕噪噪噪譟嚣囂回回回迴团團团糰园園困困困睏囱囪围圍囵圇国國"
    "图圖圆圓圣聖圹壙场場坏壞坐坐坐座块塊坚堅坛壇坛罈坜壢坝壩坝垻坞塢坟墳坠墜坯坯坯坏垄壟垅壠垆壚垒壘垦墾垩堊垫墊垭埡"
    "垯墶垱壋垲塏垴堖埘塒埙壎埙塤埚堝堑塹堕墮堤堤堤隄塆壪墙牆壮壯声聲壳殼壶壺壸壼处處备備复復复複复覆够夠夫夫夫伕头頭"
    "夸誇夸夸夹夾夹袷夺奪奁奩奂奐奋奮奖獎奥奧奸奸奸姦妆妝妇婦妈媽妩嫵妪嫗妫嬀姗姍姜姜姜薑姹奼娄婁娅婭娆嬈娇嬌娈孌娘娘"
    "娘孃娱娛娲媧娴嫺娴嫻婳嫿婴嬰婵嬋婶嬸媪媼媭嬃嫒嬡嫔嬪嫱嬙嬷嬤孙孫学學孪孿宁寧宁甯它它它牠宝寶实實宠寵审審宪憲宫宮"
    "家家家傢宽寬宾賓寝寢对對寻尋导導寿壽将將尔爾尘塵尝嘗尝嚐尧堯尴尷尸屍尸尸尽盡尽儘局局局侷层層屃屓屉屜届屆属屬屡屢"
    "屦屨屿嶼岁歲岂豈岖嶇岗崗岘峴岚嵐岛島岩巖岩岩岭嶺岳嶽岳岳岽崬岿巋峃嶨峄嶧峡峽峣嶢峤嶠峥崢峦巒峰峯崂嶗崃崍崄嶮崭嶄"
    "嵘嶸嵚嶔嵝嶁巅巔巨巨巨鉅巩鞏巯巰币幣布布布佈帅帥师師帏幃帐帳帘簾帘帘帜幟带帶帧幀席席席蓆帮幫帱幬帻幘帼幗幂冪干幹"
    "干乾干干干榦并並并併并幷幸幸幸倖广廣广广庄莊庆慶床牀庐廬庑廡库庫应應庙廟庞龐废廢庵庵庵菴庼廎廪廩开開异異弃棄弑弒"
    "张張弥彌弥瀰弦弦弦絃弪弳弯彎弹彈强強归歸当當当噹录錄录彔彟彠彦彥彨彲彩彩彩綵彻徹征徵征征径徑径逕徕徠御御御禦忆憶"
    "忏懺志志志誌忧憂念念念唸忾愾怀懷态態怂慫怃憮怄慪怅悵怆愴怜憐总總怼懟怿懌恋戀恒恆恤恤恤卹恳懇恶惡恶噁恸慟恹懨恺愷"
    "恻惻恼惱恽惲悦悅悫愨悬懸悭慳悮悞悯憫惊驚惧懼惨慘惩懲惫憊惬愜惭慚惮憚惯慣愈愈愈癒愠慍愤憤愦憒愿願愿愿慑懾慭憖懑懣"
    "懒懶懔懍戆戇戋戔戏戲戗戧战戰戚戚戚慼戚鏚戬戩戯戱户戶扇扇扇搧才才才纔扎扎扎紮扑撲托托托託扣扣扣釦执執扩擴扪捫扫掃"
    "扬揚扰擾折折折摺抚撫抛拋抟摶抠摳抡掄抢搶护護报報抵抵抵牴担擔拐拐拐柺拟擬拢攏拣揀拥擁拦攔拧擰拨撥择擇拿拿拿拏挂掛"
    "挂挂挚摯挛攣挜掗挝撾挞撻挟挾挠撓挡擋挢撟挣掙挤擠挥揮挦撏挨挨挨捱挽挽挽輓捆捆捆綑捍捍捍扞捝挩捞撈损損捡撿换換捣搗"
    "据據据据掳擄掴摑掷擲掸撣掺摻掼摜揽攬揾搵揿撳搀攙搁擱搂摟搄揯搅攪搜搜搜蒐携攜摄攝摅攄摆擺摆襬摇搖摈擯摊攤撄攖撑撐"
    "撵攆撷擷撸擼撺攛擜㩵擞擻攒攢敌敵敚敓敛斂敩斆数數斋齋斓斕斗鬥斗斗斤斤斤觔斩斬斫斫斫斲断斷旋旋旋鏇无無旧舊时時旷曠"
    "旸暘昆昆昆崑昙曇昵暱昼晝昽曨显顯晋晉晒曬晓曉晔曄晕暈晖暉暂暫暅𣈶暗暗暗闇暧曖曲曲曲麴札札札劄术術术朮朱朱朱硃朴樸"
    "朴朴机機杀殺杂雜权權杆杆杆桿杠槓杠杠条條来來杨楊杩榪杯杯杯盃杰傑杰杰松松松鬆板板板闆极極极极构構果果果菓枞樅枢樞"
    "枣棗枥櫪枧梘枨棖枪槍枪鎗枫楓枭梟柜櫃柜柜柠檸柽檉栀梔栅柵标標栈棧栉櫛栊櫳栋棟栌櫨栎櫟栏欄树樹栖棲栗栗栗慄样樣核核"
    "核覈栾欒桠椏桡橈桢楨档檔桤榿桥橋桦樺桧檜桨槳桩樁桪樳梁梁梁樑梦夢梼檮梾棶梿槤检檢棁梲棂欞棱棱棱稜椁槨椝槼椟櫝椠槧"
    "椢槶椤欏椫樿椭橢椮槮楼樓榄欖榅榲榇櫬榈櫚榉櫸榝樧槚檟槛檻槟檳槠櫧横橫樯檣樱櫻橥櫫橱櫥橹櫓橼櫞檗檗檗蘗檩檁欢歡欤歟"
    "欧歐欲欲欲慾歼殲殁歿殇殤残殘殒殞殓殮殚殫殡殯殴毆毁毀毁燬毁譭毂轂毕畢毙斃毡氈毵毿毶𣯶氇氌气氣氢氫氩氬氲氳汇匯汇彙"
    "汇滙汉漢汤湯汹洶沄澐沈沈沈瀋沟溝没沒沣灃沤漚沥瀝沦淪沧滄沨渢沩潙沪滬沾沾沾霑泛泛泛氾泛汎泞濘注注注註泪淚泶澩泷瀧"
    "泸瀘泺濼泻瀉泼潑泽澤泾涇洁潔洒灑洼窪浃浹浅淺浆漿浇澆浈湞浉溮浊濁测測浍澮济濟浏瀏浐滻浑渾浒滸浓濃浔潯浕濜浚浚浚濬"
    "涂塗涂涂涌湧涌涌涚涗涛濤涝澇涞淶涟漣涠潿涡渦涢溳涣渙涤滌润潤涧澗涨漲涩澀淀澱淀淀渊淵渌淥渍漬渎瀆渐漸渑澠渔漁渖瀋"
    "渗滲温溫游遊游游湾灣湿溼溁濚溃潰溅濺溆漵溇漊溪溪溪谿滗潷滚滾滞滯滟灩滟灧滠灄满滿滢瀅滤濾滥濫滦灤滨濱滩灘滪澦漓漓"
    "漓灕潆瀠潇瀟潋瀲潍濰潜潛潴瀦澄澄澄澂澛瀂澜瀾濑瀨濒瀕灏灝灭滅灯燈灵靈灶竈灾災灿燦炀煬炉爐炖燉炜煒炝熗点點炼煉炼鍊"
    "炽熾烁爍烂爛烃烴烛燭烟煙烟菸烦煩烧燒烨燁烩燴烫燙烬燼热熱焕煥焖燜焘燾焰焰焰燄煴熅熏燻熏熏熏薰爱愛爷爺牍牘牦犛牵牽"
    "牺犧犊犢状狀犷獷犸獁犹猶狈狽狝獮狞獰独獨狭狹狮獅狯獪狰猙狱獄狲猻狸狸狸貍猃獫猎獵猕獼猡玀猪豬猫貓猬蝟献獻獭獺玑璣"
    "玙璵玚瑒玛瑪玩玩玩翫玮瑋环環现現玱瑲玺璽珐琺珑瓏珰璫珲琿琅琅琅瑯琎璡琏璉琐瑣琼瓊瑶瑤瑷璦瑸璸璇璇璇璿璎瓔瓒瓚瓮甕"
    "瓯甌电電画畫畅暢畴疇疖癤疗療疟瘧疠癘疡瘍疬癧疭瘲疮瘡疯瘋疱皰疴痾症症症癥痈癰痉痙痒癢痖瘂痨癆痪瘓痫癇痴癡瘅癉瘆瘮"
    "瘗瘞瘘瘻瘪癟瘫癱瘾癮瘿癭癞癩癣癬癫癲皂皁皂皂皑皚皱皺皲皸盏盞盐鹽监監盖蓋盗盜盘盤眍瞘眦眥眬矓睁睜睐睞睑瞼瞆瞶瞒瞞"
    "瞩矚矩矩矩榘矫矯矶磯矾礬矿礦砀碭码碼砖磚砗硨砚硯砜碸砺礪砻礱砾礫础礎硁硜硕碩硖硤硗磽硙磑硚礄确確确确硵磠硷硷硷礆"
    "硷鹼碍礙碛磧碜磣碱鹼礼禮祃禡祎禕祢禰祯禎祷禱祸禍禀稟禄祿禅禪离離私私私俬秃禿秆稈秋秋秋鞦种種种种秘祕积積称稱秽穢"
    "秾穠稆穭税稅稣穌稳穩穑穡穗穗穗繐穞穭穷窮窃竊窍竅窎窵窑窯窜竄窝窩窥窺窦竇窭窶竖豎竞競笃篤笋筍笔筆笕筧笺箋笼籠笾籩"
    "筑築筑筑筚篳筛篩筜簹筝箏筱筱筱篠筹籌筼篔签籤签簽筿篠简簡箓籙箦簀箧篋箨籜箩籮箪簞箫簫篑簣篓簍篮籃篯籛篱籬簖籪籁籟"
    "籴糴类類籼秈粜糶粝糲粤粵粪糞粮糧粽糉糁糝糇餱糊糊糊餬糍餈系系系係系繫紧緊累累累纍絷縶緼縕縆緪纟糹纠糾纡紆红紅纣紂"
    "纤纖纤縴纥紇约約级級纨紈纩纊纪紀纫紉纬緯纭紜纮紘纯純纰紕纱紗纲綱纳納纴紝纵縱纶綸纷紛纸紙纹紋纺紡纻紵纼紖纽紐纾紓"
    "线線绀紺绁紲绂紱练練组組绅紳细細织織终終绉縐绊絆绋紼绌絀绍紹绎繹经經绐紿绑綁绒絨结結绔絝绕繞绖絰绗絎绘繪给給绚絢"
    "绛絳络絡绝絕绞絞统統绠綆绡綃绢絹绣繡绤綌绥綏绦絛继繼绨綈绩績绪緒绫綾绬緓续續绮綺绯緋绰綽绱鞝绱緔绲緄绳繩维維绵綿"
    "绶綬绷繃绷綳绸綢绹綯绺綹绻綣综綜绽綻绾綰绿綠缀綴缁緇缂緙缃緗缄緘缅緬缆纜缇緹缈緲缉緝缊縕缋繢缌緦缍綞缎緞缏緶缐線"
    "缑緱缒縋缓緩缔締缕縷编編缗緡缘緣缙縉缚縛缛縟缜縝缝縫缞縗缟縞缠纏缡縭缢縊缣縑缤繽缥縹缦縵缧縲缨纓缩縮缪繆缫繅缬纈"
    "缭繚缮繕缯繒缰繮缱繾缲繰缳繯缴繳缵纘罂罌网網罗羅罚罰罢罷罴羆羁羈羟羥羡羨群羣翘翹翙翽翚翬耇耇耇耈耢耮耧耬耸聳耻恥"
    "聂聶聋聾职職聍聹联聯聩聵聪聰肃肅肠腸肤膚肮骯肴餚肾腎肿腫胀脹胁脅胄胄胄冑胆膽背背背揹胜勝胜胜胡胡胡鬍胡衚胧朧胨腖"
    "胪臚胫脛胶膠脉脈脍膾脏髒脏臟脐臍脑腦脓膿脔臠脚腳脱脫脶腡脸臉腊臘腊腊腌醃腌腌腘膕腭齶腻膩腼靦腽膃腾騰膑臏膻羶膻膻"
    "臜臢致致致緻舆輿舍舍舍捨舣艤舰艦舱艙舻艫艰艱艳豔艳艷艺藝节節芈羋芗薌芜蕪芦蘆芸芸芸蕓苁蓯苇葦苈藶苋莧苌萇苍蒼苎苧"
    "苏蘇苏甦苏囌苔苔苔薹苧薴苹蘋苹苹范範范范茎莖茏蘢茑蔦茔塋茕煢茧繭荆荊荐薦荐荐荙薘荚莢荛蕘荜蓽荝萴荞蕎荟薈荠薺荡蕩"
    "荡盪荣榮荤葷荥滎荦犖荧熒荨蕁荩藎荪蓀荫蔭荫廕荬蕒荭葒荮葤药藥药葯莅蒞莱萊莲蓮莳蒔莴萵莶薟获獲获穫莸蕕莹瑩莺鶯莼蓴"
    "萚蘀萝蘿萤螢营營萦縈萧蕭萨薩葱蔥蒀蒕蒇蕆蒉蕢蒋蔣蒌蔞蒏醟蒙蒙蒙矇蒙濛蒙懞蓝藍蓟薊蓠蘺蓣蕷蓥鎣蓦驀蔂虆蔑蔑蔑衊蔷薔"
    "蔹蘞蔺藺蔼藹蕰薀蕲蘄蕴蘊薮藪藓蘚藤藤藤籐藴蘊蘖櫱虏虜虑慮虚虛虫蟲虫虫虬虯虮蟣虱蝨虽雖虾蝦虿蠆蚀蝕蚁蟻蚂螞蚃蠁蚕蠶"
    "蚝蠔蚝蚝蚬蜆蛊蠱蛎蠣蛏蟶蛮蠻蛰蟄蛱蛺蛲蟯蛳螄蛴蠐蜕蛻蜗蝸蜡蠟蜡蜡蝇蠅蝈蟈蝉蟬蝎蠍蝎蝎蝼螻蝾蠑螀螿螨蟎蟏蠨衅釁衔銜"
    "补補表表表錶衬襯衮袞袄襖袅嫋袅裊袆褘袜襪袭襲袯襏装裝裆襠裈褌裢褳裣襝裤褲裥襉裥襇褛褸褴襤襕襴见見观觀觃覎规規觅覓"
    "视視觇覘览覽觉覺觊覬觋覡觌覿觍覥觎覦觏覯觐覲觑覷觞觴触觸觯觶訚誾詟讋誉譽誊謄讠訁计計订訂讣訃认認讥譏讦訐讧訌讨討"
    "让讓讪訕讫訖讬託训訓议議讯訊记記讱訒讲講讳諱讴謳讵詎讶訝讷訥许許讹訛论論讻訩讼訟讽諷设設访訪诀訣证證证証诂詁诃訶"
    "评評诅詛识識诇詗诈詐诉訴诊診诋詆诌謅词詞诎詘诏詔诐詖译譯诒詒诓誆诔誄试試诖詿诗詩诘詰诙詼诚誠诛誅诜詵话話诞誕诟詬"
    "诠詮诡詭询詢诣詣诤諍该該详詳诧詫诨諢诩詡诪譸诫誡诬誣语語诮誚误誤诰誥诱誘诲誨诳誑说說诵誦诶誒请請诸諸诹諏诺諾读讀"
    "诼諑诽誹课課诿諉谀諛谁誰谂諗调調谄諂谅諒谆諄谇誶谈談谉讅谊誼谋謀谌諶谍諜谎謊谏諫谐諧谑謔谒謁谓謂谔諤谕諭谖諼谗讒"
    "谘諮谙諳谚諺谛諦谜謎谝諞谞諝谟謨谠讜谡謖谢謝谣謠谤謗谥諡谥謚谦謙谧謐谨謹谩謾谪謫谫譾谬謬谭譚谮譖谯譙谰讕谱譜谲譎"
    "谳讞谴譴谵譫谶讖谷谷谷穀豆豆豆荳象象象像豮豶贝貝贞貞负負贠貟贡貢财財责責贤賢败敗账賬货貨质質贩販贪貪贫貧贬貶购購"
    "贮貯贯貫贰貳贱賤贲賁贳貰贴貼贵貴贶貺贷貸贸貿费費贺賀贻貽贼賊贽贄贾賈贿賄赀貲赁賃赂賂赃贓资資赅賅赆贐赇賕赈賑赉賚"
    "赊賒赋賦赌賭赍齎赎贖赏賞赐賜赑贔赒賙赓賡赔賠赕賧赖賴赗賵赘贅赙賻赚賺赛賽赜賾赝贗赝贋赞贊赞讚赟贇赠贈赡贍赢贏赣贛"
    "赪赬赵趙赶趕趋趨趱趲趸躉跃躍跄蹌跖蹠跖跖跞躒践踐跶躂跷蹺跸蹕跹躚跻躋踌躊踪蹤踬躓踯躑蹑躡蹒蹣蹰躕蹿躥躏躪躜躦躯軀"
    "輼轀车車轧軋轨軌轩軒轪軑轫軔转轉轭軛轮輪软軟轰轟轱軲轲軻轳轤轴軸轵軹轶軼轷軤轸軫轹轢轺軺轻輕轼軾载載轾輊轿轎辀輈"
    "辁輇辂輅较較辄輒辅輔辆輛辇輦辈輩辉輝辊輥辋輞辌輬辍輟辎輜辏輳辐輻辑輯辒轀输輸辔轡辕轅辖轄辗輾辘轆辙轍辚轔辞辭辟闢"
    "辟辟辩辯辫辮边邊辽遼达達迁遷过過迈邁运運还還这這进進远遠违違连連迟遲迩邇迳逕迹跡迹蹟适適适适选選逊遜递遞逦邐逻邏"
    "遗遺遥遙邓鄧邝鄺邬鄔邮郵邹鄒邺鄴邻鄰郁鬱郁郁郏郟郐鄶郑鄭郓鄆郦酈郧鄖郸鄲酂酇酝醞酦醱酱醬酸酸酸痠酽釅酾釃酿釀醖醞"
    "采採采采采寀释釋里裏里里里哩鉴鑑鉴鑒銮鑾錾鏨钅釒钆釓钇釔针針针鍼钉釘钊釗钋釙钌釕钍釷钎釺钏釧钐釤钑鈒钒釩钓釣钔鍆"
    "钕釹钖鍚钗釵钘鈃钙鈣钚鈈钛鈦钜鉅钝鈍钞鈔钟鍾钟鐘钟鈡钠鈉钡鋇钢鋼钣鈑钤鈐钥鑰钥鈅钦欽钧鈞钨鎢钩鉤钪鈧钫鈁钫鍅钬鈥"
    "钭鈄钮鈕钯鈀钰鈺钱錢钲鉦钳鉗钴鈷钵鉢钶鈳钷鉕钸鈽钹鈸钺鉞钻鑽钻鉆钼鉬钽鉭钾鉀钿鈿铀鈾铁鐵铂鉑铃鈴铄鑠铅鉛铆鉚铇鉋"
    "铈鈰铉鉉铊鉈铋鉍铌鈮铍鈹铎鐸铏鉶铐銬铑銠铒鉺铓鋩铔錏铕銪铖鋮铗鋏铘鋣铙鐃铚銍铛鐺铜銅铝鋁铞銱铟銦铠鎧铡鍘铢銖铣銑"
    "铤鋌铥銩铦銛铧鏵铨銓铩鎩铪鉿铫銚铬鉻铭銘铮錚铯銫铰鉸铱銥铲鏟铲剷铳銃铴鐋铵銨银銀铷銣铸鑄铹鐒铺鋪铻鋙铼錸铽鋱链鏈"
    "链鍊铿鏗销銷锁鎖锂鋰锃鋥锄鋤锄耡锅鍋锆鋯锇鋨锈鏽锉銼锊鋝锋鋒锌鋅锍鋶锎鐦锏鐧锐銳锑銻锒鋃锓鋟锔鋦锕錒锖錆锗鍺锘鍩"
    "错錯锚錨锛錛锜錡锝鍀锞錁锟錕锠錩锡錫锢錮锣鑼锤錘锥錐锦錦锧鑕锨鍁锩錈锪鍃锫錇锫鉳锬錟锭錠键鍵锯鋸锰錳锱錙锲鍥锳鍈"
    "锴鍇锵鏘锶鍶锷鍔锸鍤锹鍬锺鍾锻鍛锼鎪锽鍠锾鍰锿鎄镀鍍镁鎂镂鏤镃鎡镄鐨镅鎇镆鏌镇鎮镈鎛镉鎘镊鑷镋钂镋鎲镌鐫镍鎳镎鎿"
    "镎錼镏鎦镐鎬镑鎊镒鎰镓鎵镔鑌镕鎔镖鏢镗鏜镘鏝镙鏍镚鏰镛鏞镜鏡镝鏑镞鏃镟鏇镠鏐镡鐔镢钁镢鐝镣鐐镤鏷镥鑥镦鐓镧鑭镨鐠"
    "镩鑹镪鏹镫鐙镬鑊镭鐳镮鐶镯鐲镰鐮镰鎌镱鐿镲鑔镳鑣镴鑞镵鑱镶鑲长長门門闩閂闪閃闫閆闬閈闭閉问問闯闖闰閏闱闈闲閒闲閑"
    "闳閎间間闵閔闶閌闷悶闸閘闹鬧闺閨闻聞闼闥闽閩闾閭闿闓阀閥阁閣阂閡阃閫阄鬮阅閱阆閬阇闍阈閾阉閹阊閶阋鬩阌閿阍閽阎閻"
    "阏閼阐闡阑闌阒闃阓闠阔闊阕闋阖闔阗闐阘闒阙闕阚闞阛闤队隊阳陽阴陰阵陣阶階际際陆陸陇隴陈陳陉陘陕陝陦隯陧隉陨隕险險"
    "随隨隐隱隶隸隽雋难難雇僱雇雇雏雛雕雕雕鵰雠讎雳靂雾霧霁霽霉黴霡霢霭靄靓靚靔靝静靜面面面麪靥靨鞑韃鞒鞽鞯韉鞲韝韦韋"
    "韧韌韨韍韩韓韪韙韫韞韬韜韵韻页頁顶頂顷頃顸頇项項顺順须須须鬚顼頊顽頑顾顧顿頓颀頎颁頒颂頌颃頏预預颅顱领領颇頗颈頸"
    "颉頡颊頰颋頲颌頜颍潁颎熲颏頦颐頤频頻颒頮颓頹颔頷颕頴颖穎颗顆题題颙顒颚顎颛顓颜顏额額颞顳颟顢颠顛颡顙颢顥颣纇颤顫"
    "颥顬颦顰颧顴风風飏颺飐颭飑颮飒颯飓颶飔颸飕颼飖颻飗飀飘飄飙飆飚飈飞飛飨饗餍饜饣飠饤飣饥飢饥饑饦飥饧餳饨飩饩餼饪飪"
    "饫飫饬飭饭飯饮飲饯餞饰飾饱飽饲飼饳飿饴飴饵餌饶饒饷餉饸餄饹餎饺餃饻餏饼餅饽餑饾餖饿餓馀餘馁餒馂餕馃餜馄餛馅餡馆館"
    "馇餷馈饋馉餶馊餿馋饞馌饁馍饃馎餺馏餾馐饈馑饉馒饅馓饊馔饌馕饢马馬驭馭驮馱驯馴驰馳驱驅驲馹驳駁驴驢驵駔驶駛驷駟驸駙"
    "驹駒驺騶驻駐驼駝驽駑驾駕驿驛骀駘骁驍骂罵骃駰骄驕骅驊骆駱骇駭骈駢骉驫骊驪骋騁验驗骍騂骎駸骏駿骐騏骑騎骒騍骓騅骔騌"
    "骕驌骖驂骗騙骘騭骙騤骚騷骛騖骜驁骝騮骞騫骟騸骠驃骡騾骢驄骣驏骤驟骥驥骦驦骧驤髅髏髋髖髌髕鬓鬢鬶鬹魇魘魉魎鱼魚鱽魛"
    "鱾魢鱿魷鲀魨鲁魯鲂魴鲃䰾鲄魺鲅鮁鲆鮃鲇鮎鲈鱸鲉鮋鲊鮓鲋鮒鲌鮊鲍鮑鲎鱟鲏鮍鲐鮐鲑鮭鲒鮚鲓鮳鲔鮪鲕鮞鲖鮦鲗鰂鲘鮜鲙鱠"
    "鲚鱭鲛鮫鲜鮮鲝鮺鲞鯗鲟鱘鲠鯁鲡鱺鲢鰱鲣鰹鲤鯉鲥鰣鲦鰷鲧鯀鲨鯊鲩鯇鲪鮶鲫鯽鲬鯒鲭鯖鲮鯪鲯鯕鲰鯫鲱鯡鲲鯤鲳鯧鲴鯝鲵鯢"
    "鲶鯰鲷鯛鲸鯨鲹鰺鲺鯴鲻鯔鲼鱝鲽鰈鲾鰏鲿鱨鳀鯷鳁鰮鳂鰃鳃鰓鳄鱷鳅鰍鳆鰒鳇鰉鳈鰁鳉鱂鳊鯿鳋鰠鳌鰲鳍鰭鳎鰨鳏鰥鳐鰩鳑鰟"
    "鳒鰜鳓鰳鳔鰾鳕鱈鳖鱉鳗鰻鳘鰵鳙鱅鳚䲁鳛鰼鳜鱖鳝鱔鳞鱗鳟鱒鳠鱯鳡鱤鳢鱧鳣鱣鳤䲘鸟鳥鸠鳩鸡雞鸢鳶鸣鳴鸤鳲鸥鷗鸦鴉鸧鶬"
    "鸨鴇鸩鴆鸪鴣鸫鶇鸬鸕鸭鴨鸮鴞鸯鴦鸰鴒鸱鴟鸲鴝鸳鴛鸴鷽鸵鴕鸶鷥鸷鷙鸸鴯鸹鴰鸺鵂鸻鴴鸼鵃鸽鴿鸾鸞鸿鴻鹀鵐鹁鵓鹂鸝鹃鵑"
    "鹄鵠鹅鵝鹆鵒鹇鷳鹇鷴鹈鵜鹉鵡鹊鵲鹋鶓鹌鵪鹍鵾鹎鵯鹏鵬鹐鵮鹑鶉鹒鶊鹓鵷鹔鷫鹕鶘鹖鶡鹗鶚鹘鶻鹙鶖鹚鷀鹛鶥鹜鶩鹝鷊鹞鷂"
    "鹟鶲鹠鶹鹡鶺鹢鷁鹣鶼鹤鶴鹥鷖鹦鸚鹧鷓鹨鷚鹩鷯鹪鷦鹫鷲鹬鷸鹭鷺鹮䴉鹯鸇鹰鷹鹱鸌鹲鸏鹳鸛鹴鸘鹾鹺麦麥麸麩麹麴麺麪麽麼"
    "黄黃黉黌黡黶黩黷黪黲黾黽鼋黿鼌鼂鼍鼉鼹鼴齐齊齑齏齿齒龀齔龁齕龂齗龃齟龄齡龅齙龆齠龇齜龈齦龉齬龊齪龋齲龌齷龙龍龚龔"
    "龛龕龟龜鿎䃮鿏䥑鿒鿓鿔鎶𠀾𠁞𠆲儣𠆿𠌥𠇹俓𠉂㒓𠉗𠏢𠋆儭𠚳𠠎𠛅剾𠛆𠞆𠛾𪟖𠡠勑𠮶嗰𠯟哯𠯠噅𠰱㘉𠰷嚧𠱞囃𠲥𡅏𠴛𡃕𠴢𡄔𠵸𡄣"
    "𠵾㗲𡋀𡓾𡋗𡑭𡋤壗𡍣𡔖𡒄壈𡝠㜷𡞋㜗𡞱㜢𡠟孎𡥧孻𡭜𡮉𡭬𡮣𡳃𡳳𡳒𦘧𡶴嵼𡸃𡽗𡺃嶈𡺄嶘𢋈㢝𢗓㦛𢘙𢤱𢘝𢣚𢘞𢣭𢙏愻𢙐憹𢙑𢠼𢙒憢"
    "𢙓懀𢛯㦎𢠁懎𢢐𤢻𢧐戰𢫊𢷮𢫞𢶫𢫬摋𢬍擫𢬦𢹿𢭏擣𢽾斅𣃁斸𣆐曥𣈣𣋋𣍨𦢈𣍯腪𣍰脥𣎑臗𣏢槫𣐕桱𣐤欍𣑶𣠲𣒌楇𣓿橯𣔌樤𣗊樠𣗋欓"
    "𣗙㰙𣘐㯤𣘓𣞻𣘴檭𣘷𣝕𣚚欘𣞎𣠩𣨼殢𣭤𣯴𣯣𣯩𣱝氭𣲗湋𣲘潕𣳆㵗𣶩澅𣶫𣿉𣶭𪷓𣷷𤅶𣸣濆𣺼灙𣺽𤁣𣽷瀃𤆡熓𤆢㷍𤇃爄𤇄熌𤇭爖𤇹熚"
    "𤈶熉𤈷㷿𤊀𤒎𤊰𤓩𤋏熡𤎺𤓎𤎻𤑳𤙯𤛮𤝢𤢟𤞃獩𤞤玁𤠋㺏𤦀瓕𤩽瓛𤳄𤳸𤶊癐𤶧𤸫𤻊㿗𤽯㿧𤾀皟𤿲麬𥁢䀉𥅘𥌃𥅴䀹𥅿𥊝𥆧瞤𥇢䁪𥎝䂎"
    "𥐟礒𥐯𥖅𥐰𥕥𥐻碙𥞦𥞵𥧂𥨐𥩟竚𥩺𥪂𥫣籅𥬀䉙𥬞籋𥬠篘𥭉𥵊𥮋𥸠𥮜䉲𥮾篸𥱔𥵃𥹥𥼽𥺅䊭𥺇𥽖𦈈𥿊𦈉緷𦈋綇𦈌綀𦈎繟𦈏緍𦈐縺𦈑緸"
    "𦈒𦂅𦈓䋿𦈔縎𦈕緰𦈖䌈𦈗𦃄𦈘䌋𦈙䌰𦈚縬𦈛繓𦈜䌖𦈝繏𦈞䌟𦈟䌝𦈠䌥𦈡繻𦍠䍽𦛨朥𦝼膢𦟗𦣎𦨩𦪽𦰏蓧𦰴䕳𦶟爇𦶻𦾟𦻕蘟𧉐𧕟𧉞䗿"
    "𧌥𧎈𧏖蠙𧏗蠀𧑏蠾𧒭𧔥𧜭䙱𧝝襰𧝧𧟀𧮪詀𧳕𧳟𧹑䞈𧹒買𧹓𧶔𧹔賬𧹕䝻𧹖賟𧹗贃𧿈𨇁𨀁躘𨀱𨄣𨁴𨅍𨂺𨈊𨄄𨈌𨅛䠱𨅫𨇞𨅬躝𨉗軉𨐅軗"
    "𨐆𨊻𨐇𨏠𨐈輄𨐉𨎮𨐊𨏥𨑹䢨𨟳𨣞𨠨𨣧𨡙𨢿𨡺𨣈𨤰𨤻𨰾鎷𨰿釳𨱀𨥛𨱁鈠𨱂鈋𨱃鈲𨱄鈯𨱅鉁𨱆龯𨱇銶𨱈鋉𨱉鍄𨱊𨧱𨱋錂𨱌鏆𨱍鎯𨱎鍮"
    "𨱏鎝𨱐𨫒𨱑鐄𨱒鏉𨱓鐎𨱔鐏𨱕𨮂𨱖䥩𨷿䦳𨸀𨳕𨸁𨳑𨸂閍𨸃閐𨸄䦘𨸅𨴗𨸆𨵩𨸇𨵸𨸉𨶀𨸊𨶏𨸋𨶲𨸌𨶮𨸎𨷲𨸘𨽏𨸟䧢𩏼䪏𩏽𩏪𩏾𩎢𩏿䪘"
    "𩐀䪗𩓋顂𩖕𩓣𩖖顃𩖗䫴𩙥颰𩙦𩗀𩙧䬞𩙨𩘹𩙩𩘀𩙪颷𩙫颾𩙬𩘺𩙭𩘝𩙮䬘𩙯䬝𩙰𩙈𩟿𩚛𩠀𩚥𩠁𩚵𩠂𩛆𩠃𩛩𩠅𩟐𩠆𩜦𩠇䭀𩠈䭃𩠉𩜇𩠊𩜵"
    "𩠋𩝔𩠌餸𩠎𩞄𩠏𩞦𩠠𩠴𩡖𩡣𩧦𩡺𩧨駎𩧩𩤊𩧪䮾𩧫駚𩧬𩢡𩧭䭿𩧮𩢾𩧯驋𩧰䮝𩧱𩥉𩧲駧𩧳𩢸𩧴駩𩧵𩢴𩧶𩣏𩧸𩣫𩧺駶𩧻𩣵𩧼𩣺𩧿䮠𩨀騔"
    "𩨁䮞𩨂驄𩨃騝𩨄騪𩨅𩤸𩨆𩤙𩨇䮫𩨈騟𩨉𩤲𩨊騚𩨋𩥄𩨌𩥑𩨍𩥇𩨎龭𩨏䮳𩨐𩧆𩩈䯤𩬣𩭙𩬤𩰀𩭹鬖𩯒𩯳𩰰𩰹𩲒𩳤𩴌𩴵𩽹魥𩽺𩵩𩽻𩵹𩽼鯶"
    "𩽽𩶱𩽾鮟𩽿𩶰𩾁鯄𩾂䲖𩾃鮸𩾄𩷰𩾅𩸃𩾆𩸦𩾇鯱𩾈䱙𩾊䱬𩾋䱰𩾌鱇𩾎𩽇𪉂䲰𪉃鳼𪉄𩿪𪉅𪀦𪉆鴲𪉈鴜𪉉𪁈𪉊鷨𪉋𪀾𪉌𪁖𪉍鵚𪉎𪂆𪉏𪃏"
    "𪉐𪃍𪉑鷔𪉒𪄕𪉔𪄆𪉕𪇳𪎈䴬𪎉麲𪎊麨𪎋䴴𪎌麳𪑅䵳𪔭𪔵𪚏𪘀𪚐𪘯𪜎𠿕𪞝凙𪟎㔋𪟝勣𪠀𧷎𪠟㓄𪠡𠬙𪠳唓𪠵㖮𪠸嚛𪠺𠽃𪠽噹𪡀嘺𪡃嘪"
    "𪡋噞𪡏嗹𪡛㗿𪡞嘳𪡺𡃄𪢌㘓𪢐𡃤𪢒𡂡𪢕嚽𪢖𡅯𪢠囒𪢮圞𪢸墲𪣆埬𪣒堚𪣻塿𪤄𡓁𪤚壣𪥠𧹈𪥫孇𪥰嬣𪥿嬻𪧀孾𪧘寠𪨊㞞𪨗屩𪨧崙𪨩𡸗"
    "𪨶輋𪨷巗𪨹𡹬𪩇㟺𪩎巊𪩘巘𪩛𡿖𪩷幝𪩸幩𪪏廬𪪑㢗𪪞廧𪪴𢍰𪪼彃𪫌徿𪫡𢤩𪫷㦞𪫺憸𪬚𢣐𪬯𢤿𪭝𢯷𪭢摐𪭧擟𪭯𢶒𪭵掚𪭾撊𪮃㨻𪮋㩋"
    "𪮖撧𪮳𢺳𪮶攋𪯋㪎𪰶曊𪱥膹𪱷梖𪲎櫅𪲔欐𪲛檵𪲮櫠𪳍欇𪳗𣜬𪴙欑𪵑毊𪵣霼𪵱濿𪶄溡𪶒𤄷𪶮𣽏𪷍㵾𪷽灒𪸕熂𪸩煇𪹀𤑹𪹠𤓌𪹳爥𪹹𤒻"
    "𪺣𤘀𪺪𤜆𪺭犞𪺷獊𪺸𤠮𪺻㺜𪺽猌𪻐瑽𪻨瓄𪻲瑻𪻺璝𪼋㻶𪼴𤬅𪽈畼𪽝𤳷𪽪痮𪽭𤷃𪽮㿖𪽴𤺔𪽷瘱𪾔盨𪾢睍𪾣眝𪾦矑𪾸矉𪿊𥏝𪿞𥖲𪿫礮"
    "𪿵𥗇𫀌𥜰𫀓𥜐𫀨䅐𫀬䅳𫀮𥢷𫁂䆉𫁟竱𫁡鴗𫁱𥶽𫁲䉑𫁳𥯤𫁷䉶𫁺𥴼𫂃簢𫂆簂𫂈䉬𫂖𥴨𫂿𥻦𫃗𩏷𫄙糺𫄚䊺𫄛紟𫄜䋃𫄝𥾯𫄞䋔𫄟絁𫄠絙"
    "𫄡絧𫄢絥𫄣繷𫄤繨𫄥纚𫄦𦀖𫄧綖𫄨絺𫄩䋦𫄪𦅇𫄫綟𫄬緤𫄭緮𫄮䋼𫄯𦃩𫄰縍𫄱繬𫄲縸𫄳縰𫄴繂𫄵𦅈𫄶繈𫄷繶𫄸纁𫄹纗𫅅䍤𫅗羵𫅥𦒀"
    "𫅭䎙𫅼𦔖𫆏聻𫆝𦟼𫆫𦡝𫇘𦧺𫇛艣𫇪𦱌𫇭蔿𫇴蒭𫇽蕽𫈉蕳𫈎葝𫈟蔯𫈵蕝𫉁薆𫉄藷𫊪䗅𫊮蠦𫊸蟜𫊹𧒯𫊻蟳𫋇蟂𫋌蟘𫋲䙔𫋷襗𫋹襓𫋻襘"
    "𫌀襀𫌇襵𫌋𧞫𫌨覼𫌪覛𫌫𧡴𫌬𧢄𫌭覹𫌯䚩𫍐𧭹𫍙訑𫍚訞𫍛訜𫍜詓𫍝諫𫍞𧦝𫍟𧦧𫍠䛄𫍡詑𫍢譊𫍣詷𫍤譑𫍥誂𫍦譨𫍧誺𫍨誫𫍩諣𫍪誋"
    "𫍫䛳𫍬誷𫍭𧩕𫍮誳𫍯諴𫍰諰𫍱諯𫍲謏𫍳諥𫍴謱𫍵謸𫍶𧩼𫍷謉𫍸謆𫍹謯𫍺𧫝𫍻譆𫍼𧬤𫍽譞𫍾𧭈𫍿譾𫎆豵𫎌貗𫎦贚𫎧䝭𫎨𧸘𫎩賝𫎪䞋"
    "𫎫贉𫎬贑𫎭䞓𫎱䟐𫎳䟆𫎸𧽯𫎺䟃𫏃䠆𫏆蹳𫏋蹻𫏌𨂐𫏐蹔𫏑𨇽𫏕𨆪𫏞𨇰𫏨𨇤𫐄軏𫐅軕𫐆轣𫐇軜𫐈軷𫐉軨𫐊軬𫐋𨎌𫐌軿𫐍𨌈𫐎輢𫐏輖"
    "𫐐輗𫐑輨𫐒輷𫐓輮𫐔𨍰𫐕轊𫐖轇𫐗轐𫐘轗𫐙轠𫐷遱𫑘鄟𫑡鄳𫑷醶𫓥釟𫓦釨𫓧鈇𫓨鈛𫓩鏦𫓪鈆𫓫𨥟𫓬鉔𫓭鉠𫓮𨪕𫓯銈𫓰銊𫓱鐈𫓲銁"
    "𫓳𨰋𫓴鉾𫓵鋠𫓶鋗𫓷𫒡𫓸錽𫓹錤𫓺鐪𫓻錜𫓼𨨛𫓽錝𫓾錥𫓿𨨢𫔀鍊𫔁鐼𫔂鍉𫔃𨰲𫔄鍒𫔅鎍𫔆䥯𫔇鎞𫔈鎙𫔉𨰃𫔊鏥𫔋䥗𫔌鏾𫔍鐇𫔎鐍"
    "𫔏𨬖𫔐𨭸𫔑𨭖𫔒𨮳𫔓𨯟𫔔鑴𫔕𨰥𫔖𨲳𫔭開𫔮閒𫔯閗𫔰閞𫔲𨴹𫔴閵𫔵䦯𫔶闑𫔽𨼳𫕚𩀨𫕥霣𫕨𩅙𫖃靧𫖅䪊𫖇鞾𫖑𩎖𫖒韠𫖓𩏂𫖔韛𫖕韝"
    "𫖖𩏠𫖪𩑔𫖫䪴𫖬䪾𫖭𩒎𫖮顗𫖯頫𫖰䫂𫖱䫀𫖲䫟𫖳頵𫖴𩔳𫖵𩓥𫖶顅𫖷𩔑𫖸願𫖹顣𫖺䫶𫗇䫻𫗈𩗓𫗉𩗴𫗊䬓𫗋飋𫗚𩟗𫗞飦𫗟䬧𫗠餦𫗡𩚩"
    "𫗢飵𫗣飶𫗤𩛌𫗥餫𫗦餔𫗧餗𫗨𩛡𫗩饠𫗪餧𫗫餬𫗬餪𫗭餵𫗮餭𫗯餱𫗰䭔𫗱䭑𫗳𩝽𫗴饘𫗵饟𫘛馯𫘜馼𫘝駃𫘞駞𫘟駊𫘠駤𫘡駫𫘣駻𫘤騃"
    "𫘥騉𫘦騊𫘧騄𫘨騠𫘩騜𫘪騵𫘫騴𫘬騱𫘭騻𫘮䮰𫘯驓𫘰驙𫘱驨𫘽鬠𫙂𩯁𫚈鱮𫚉魟𫚊鰑𫚋鱄𫚌魦𫚍魵𫚎𩶁𫚏䱁𫚐䱀𫚑鮅𫚒鮄𫚓鮤𫚔鮰"
    "𫚕鰤𫚖鮆𫚗鮯𫚘𩻮𫚙鯆𫚚鮿𫚛鮵𫚜䲅𫚝𩸄𫚞鯬𫚟𩸡𫚠䱧𫚡鯞𫚢鰋𫚣鯾𫚤鰦𫚥鰕𫚦鰫𫚧鰽𫚨𩻗𫚩𩻬𫚪鱊𫚫鱢𫚬𩼶𫚭鱲𫛚鳽𫛛鳷𫛜鴀"
    "𫛝鴅𫛞鴃𫛟鸗𫛠𩿤𫛡鴔𫛢鸋𫛣鴥𫛤鴐𫛥鵊𫛦鴮𫛧𪀖𫛨鵧𫛩鴳𫛪鴽𫛫鶰𫛬䳜𫛭鵟𫛮䳤𫛯鶭𫛰䳢𫛱鵫𫛲鵰𫛳鵩𫛴鷤𫛵鶌𫛶鶒𫛷鶦𫛸鶗"
    "𫛹𪃧𫛺䳧𫛻𪃒𫛼䳫𫛽鷅𫛾𪆷𫜀鷐𫜁鷩𫜂𪅂𫜃鷣𫜄鷷𫜅䴋𫜊𪉸𫜑麷𫜒䴱𫜓𪌭𫜔䴽𫜕𪍠𫜙䵴𫜟𪓰𫜨䶕𫜩齧𫜪齩𫜫𫜦𫜬齰𫜭齭𫜮齴𫜯𪙏"
    "𫜰齾𫜲龓𫜳䶲𫝈㑮𫝋𠐊𫝦㛝𫝧㜐𫝨媈𫝩嬦𫝪𡟫𫝫婡𫝬嬇𫝭孆𫝮孄𫝵嶹𫞅𦠅𫞗潣𫞚澬𫞛㶆𫞝灍𫞠爧𫞡爃𫞢𤛱𫞣㹽𫞥珼𫞦璾𫞧𤩂𫞨璼"
    "𫞩璊𫞷𥢶𫟃絍𫟄綋𫟅綡𫟆緟𫟇𦆲𫟑䖅𫟕䕤𫟞訨𫟟詊𫟠譂𫟡誴𫟢䜖𫟤䡐𫟥䡩𫟦䡵𫟫𨞺𫟬𨟊𫟲釚𫟳釲𫟴鈖𫟵鈗𫟶銏𫟷鉝𫟸鉽𫟹鉷𫟺䤤"
    "𫟻銂𫟼鐽𫟽𨧰𫟾𨩰𫟿鎈𫠀䥄𫠁鑉𫠂閝𫠅韚𫠆頍𫠇𩖰𫠈䫾𫠊䮄𫠋騼𫠌𩦠𫠏𩵦𫠐魽𫠑䱸𫠒鱆𫠖𩿅𫠜齯𫢸僤𫧃𣍐𫧮𪋿𫫇噁𫬐㘔𫭟塸𫭢埨"
    "𫭼𡑍𫮃墠𫰛娙𫵷㠣𫶇嵽𫷷廞𫸩彄𬀩暐𬀪晛𬂩梜𬃊櫍𬇕澫𬇙浿𬇹漍𬉼熰𬊈燖𬊤燀𬍛瓅𬍡璗𬍤璕𬒈礐𬒗𥗽𬕂篢𬘓紃𬘘紞𬘡絪𬘩綎𬘫綄"
    "𬘬綪𬘭綝𬘯綧𬙂縯𬙊纆𬙋纕𬜬蔄𬜯䓣𬞟蘋𬟁虉𬟽蝀𬣙訏𬣞詝𬣡諓𬣳詪𬤇諲𬤊諟𬤝譓𬨂軝𬨎輶𬩽鄩𬪩醲𬬩釴𬬭錀𬬮鋹𬬱釿𬬸鉥𬬹鉮"
    "𬬻鑪𬬿鉊𬭁鉧𬭊𨧀𬭎鋐𬭚錞𬭛𨨏𬭤鍭𬭩鎓𬭬鏏𬭭鏚𬭯䥕𬭳𨭎𬭶𨭆𬭸鏻𬭼鐩𬮱闉𬮿隑𬯀隮𬯎隤𬱖頔𬱟頠𬳵駓𬳶駉𬳽駪𬳿駼𬴂騑𬴃騞"
    "𬴊驎𬶋鮈𬶍鮀𬶏鮠𬶐鮡𬶟鯻𬶠鰊𬶨鱀𬶭鰶𬶮鱚𬷕鵏𬸘鶠𬸚鸑𬸣鶱𬸦鷟𬸪鷭𬸯鷿𬹼齘𬺈齮𬺓齼𰬸繐𰰨菕𰶎譅𰻝𰻞𰾄鋂𰾭鑀𱊜𪈼"
)

Language = namedtuple("Language", "to_text convert")

TS_MAP = {ord(trad): simp for trad, simp in zip(TS_PAIRS[0::2], TS_PAIRS[1::2])}
TS_REVERSE = {}
for _trad, _simp in zip(TS_PAIRS[0::2], TS_PAIRS[1::2]):
    TS_REVERSE.setdefault(_simp, []).append(_trad)
ST_TARGETS = {}
for _src, _dst in zip(ST_PAIRS[0::2], ST_PAIRS[1::2]):
    ST_TARGETS.setdefault(_src, []).append(_dst)
ST_FIRST = {ord(src): dsts[0] for src, dsts in ST_TARGETS.items()}


def identity(text):
    return text


def to_simplified(text):
    return text.translate(TS_MAP)


def candidates(char):
    """写回繁体时的候选字：首选繁体，其次是能映射到这个简体字的繁体字，最后是原字。"""
    out = list(ST_TARGETS.get(char, ()))
    out += [trad for trad in TS_REVERSE.get(char, ()) if trad not in out]
    if char not in out:
        out.append(char)
    return out


def encode_text(text, lang, codec):
    """把文本编码成 codec 字节。简体模式下逐字换成目标编码收得下的繁体字。"""
    if not lang.convert:
        return text.encode(codec)
    try:
        return text.translate(ST_FIRST).encode(codec)
    except UnicodeEncodeError:
        pass
    out = bytearray()
    for char in text:
        for choice in candidates(char):
            try:
                out += choice.encode(codec)
                break
            except UnicodeEncodeError:
                continue
        else:
            raise ValueError("字符 %r 无法用 %s 编码" % (char, codec))
    return bytes(out)


# 解包时把原文变成本语言，打包时按 convert 决定要不要换回繁体
LANGUAGES = {
    "zh-hans": Language(to_simplified, True),
    "zh-hant": Language(identity, False),
}

if array("I").itemsize != 4:
    raise SystemExit("需要 4 字节无符号整型数组，当前平台 itemsize=%d" % array("I").itemsize)


# ---------------------------------------------------------------- 封包解包

def decrypt(buf, crc32):
    """解密一段按 4 字节对齐的密文，返回等长的 bytes。"""
    if len(buf) % 4:
        raise ValueError("密文长度 %d 不能被 4 整除" % len(buf))
    key = KEY ^ (crc32 & MASK)
    words = array("I")
    words.frombytes(bytes(buf))
    if sys.byteorder != "little":
        words.byteswap()
    plain = array("I")
    append = plain.append
    for w in words:
        x = w ^ key
        append((x >> 6 | x << 26) & MASK)
    if sys.byteorder != "little":
        plain.byteswap()
    return plain.tobytes()


def decrypt_padded(buf, length, crc32):
    """解密按 length 对齐的密文，返回正好 length 字节的明文。"""
    return decrypt(buf[:((length + 3) & ~3)], crc32)[:length]


Header = namedtuple("Header", "uuid version tree_length tree_crc count")


def encrypt(buf, crc32):
    """decrypt 的逆运算：先把 4 字节循环左移 6 位，再异或 key。"""
    if len(buf) % 4:
        raise ValueError("明文长度 %d 不能被 4 整除" % len(buf))
    key = KEY ^ (crc32 & MASK)
    words = array("I")
    words.frombytes(bytes(buf))
    if sys.byteorder != "little":
        words.byteswap()
    out = array("I")
    append = out.append
    for w in words:
        append(((w << 6 | w >> 26) & MASK) ^ key)
    if sys.byteorder != "little":
        out.byteswap()
    return out.tobytes()


def read_index(data):
    """解析头部和目录树，返回 (头部, 文件包起点, 条目列表)。"""
    if len(data) < 8:
        raise ValueError("文件太小，不是 PVF")
    uuid_len = struct.unpack_from("<I", data, 0)[0]
    if not 0 < uuid_len <= 64:
        raise ValueError("UUID 长度异常 %d" % uuid_len)
    uuid = data[4:4 + uuid_len].decode("ascii", "replace")
    version, tree_len, tree_crc, count = HEADER.unpack_from(data, 4 + uuid_len)
    tree_start = 4 + uuid_len + HEADER.size
    tree_end = tree_start + tree_len
    if tree_len <= 0 or tree_end > len(data):
        raise ValueError("目录树越界，%d + %d > %d" % (tree_start, tree_len, len(data)))
    pack_start = tree_end
    pack_len = len(data) - pack_start

    tree = decrypt_padded(data[tree_start:tree_end], tree_len, tree_crc)

    entries = []
    off = 0
    while off + ENTRY_HEAD.size <= tree_len:
        number, path_len = ENTRY_HEAD.unpack_from(tree, off)
        tail = off + ENTRY_HEAD.size + path_len
        if path_len <= 0 or tail + ENTRY_TAIL.size > tree_len:
            raise ValueError("目录树第 %d 条记录损坏，偏移 %d" % (len(entries), off))
        length, crc, offset = ENTRY_TAIL.unpack_from(tree, tail)
        if length < 0 or offset < 0 or offset + length > pack_len:
            raise ValueError("第 %d 条记录越出文件包，偏移 %d 长度 %d" % (len(entries), offset, length))
        raw_path = tree[off + ENTRY_HEAD.size:tail].decode("cp949", "replace")
        entries.append((number, raw_path, length, crc, offset))
        off = tail + ENTRY_TAIL.size

    if len(entries) != count:
        raise ValueError("条目数不符，头部声明 %d，实际解析 %d" % (count, len(entries)))
    return Header(uuid, version, tree_len, tree_crc, count), pack_start, entries


def safe_parts(raw_path):
    """把封包里的路径拆成安全的相对路径片段，不安全时返回 None。"""
    parts = []
    for part in raw_path.replace("\\", "/").split("/"):
        if part in ("", "."):
            continue
        if part == ".." or ":" in part:
            return None
        parts.append(part)
    return parts or None


# ---------------------------------------------------------------- 字符串表

def decode_best(raw, primary):
    """先用主编码解码，不行再试其它，都失败时留下 \\xNN 转义。"""
    for codec in (primary,) + CODECS:
        try:
            return raw.decode(codec)
        except UnicodeDecodeError:
            continue
    return raw.decode(primary, "backslashreplace")


def decode_text(raw, primary, translate):
    """按检测到的编码解码；只有 CP950（繁体中文）的文本才做繁简转换。"""
    text = decode_best(raw, primary)
    return translate(text) if primary == "cp950" else text


def detect_codec(samples):
    """挑解码失败最少的编码，同分时按 CODECS 的顺序。"""
    best = CODECS[0]
    best_fails = None
    for codec in CODECS:
        fails = 0
        for sample in samples:
            try:
                sample.decode(codec)
            except UnicodeDecodeError:
                fails += 1
        if best_fails is None or fails < best_fails:
            best, best_fails = codec, fails
    return best


def load_string_table(raw, translate):
    """解析 stringtable.bin，返回字符串列表（已解码）。"""
    count = INT32.unpack_from(raw, 0)[0]
    if count <= 0 or 4 + 4 * (count + 1) > len(raw):
        raise ValueError("stringtable.bin 头部异常，字符串数 %d" % count)
    offsets = array("i")
    offsets.frombytes(raw[4:4 + 4 * (count + 1)])
    # 索引里的偏移比实际位置小 4，字符串区紧跟在索引后面。
    blob = 4 + 4 * (count + 1)
    if offsets[0] + 4 != blob:
        raise ValueError("stringtable.bin 偏移基准不符，%d + 4 != %d" % (offsets[0], blob))
    end = len(raw)
    strings = []
    for i in range(count):
        start, stop = offsets[i] + 4, offsets[i + 1] + 4
        if not blob <= start <= stop <= end:
            raise ValueError("stringtable.bin 第 %d 个字符串越界" % i)
        strings.append(raw[start:stop])
    primary = detect_codec([s for s in strings if not s.isascii()][:20000])
    return [decode_text(s, primary, translate) for s in strings]


def load_nstring_list(raw, strings):
    """解析 n_string.lst，返回 {序号: .str 文件路径}。"""
    files = {}
    off = 2
    while off + 10 <= len(raw):
        if raw[off] != 2 or raw[off + 5] != 7:
            raise ValueError("n_string.lst 第 %d 字节不是预期结构" % off)
        index = INT32.unpack_from(raw, off + 1)[0]
        name_index = INT32.unpack_from(raw, off + 6)[0]
        if not 0 <= name_index < len(strings):
            raise ValueError("n_string.lst 引用了不存在的字符串 %d" % name_index)
        files[index] = strings[name_index]
        off += 10
    return files


def load_str_values(raw, translate):
    """把 .str 文件解析成 {键: 文本}。"""
    pairs = []
    for line in raw.split(b"\r\n"):
        if not line or line.startswith(b"//") or b">" not in line:
            continue
        key, value = line.split(b">", 1)
        pairs.append((key, value))
    primary = detect_codec([value for _key, value in pairs][:20000])
    return {
        decode_best(key, primary): decode_text(value, primary, translate)
        for key, value in pairs
    }


def str_codecs(raw):
    """挑 .str 里值和注释行各自的编码。注释行往往留着韩文。"""
    lines = raw.split(b"\r\n")
    values = [line.split(b">", 1)[1] for line in lines if b">" in line]
    comments = [line for line in lines if line.startswith(b"//") and not line.isascii()]
    value_codec = detect_codec(values[:20000])
    comment_codec = detect_codec(comments[:20000]) if comments else value_codec
    return value_codec, comment_codec


def str_file_to_text(raw, translate):
    """把 .str 文件逐行按它自己的编码解码并做繁简转换，返回文本。"""
    value_codec, comment_codec = str_codecs(raw)
    out = [
        decode_text(line, comment_codec if line.startswith(b"//") else value_codec, translate)
        for line in raw.split(b"\r\n")
    ]
    return "\r\n".join(out)


def str_text_to_bytes(original, text, lang):
    """把文本写回 .str。行数没变时逐行处理，没改的行沿用原字节。"""
    value_codec, comment_codec = str_codecs(original)
    old_lines = original.split(b"\r\n")
    new_lines = text.split("\r\n")
    if len(old_lines) != len(new_lines):
        return encode_text(text, lang, value_codec)
    out = []
    for old, new in zip(old_lines, new_lines):
        codec = comment_codec if old.startswith(b"//") else value_codec
        if decode_text(old, codec, lang.to_text) == new:
            out.append(old)
        else:
            out.append(encode_text(new, lang, codec))
    return b"\r\n".join(out)


# ---------------------------------------------------------------- 转义

def escape(text):
    out = text.replace("\\", "\\\\").replace("`", "\\`")
    return out.replace("\r", "\\r").replace("\n", "\\n")


def unescape(text):
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        nxt = text[i + 1:i + 2]
        if nxt == "r":
            out.append("\r")
        elif nxt == "n":
            out.append("\n")
        elif nxt == "`":
            out.append("`")
        elif nxt == "\\":
            out.append("\\")
        else:
            raise ValueError("未知转义 \\%s" % nxt)
        i += 2
    return "".join(out)


# ---------------------------------------------------------------- 脚本 <-> 文本

class ScriptText:
    """二进制脚本和文本之间的双向转换，名字表来自封包自身。"""

    def __init__(self, strings, str_values):
        self.strings = strings
        self.string_ids = {}
        for index, name in enumerate(self.strings):
            self.string_ids.setdefault(name, index)
        self.str_values = str_values

    def name(self, index):
        if not 0 <= index < len(self.strings):
            raise ValueError("字符串下标 %d 越界" % index)
        return self.strings[index]

    def link_value(self, nstring, key):
        values = self.str_values.get(nstring)
        if values is None:
            return ""
        return values.get(key, "")

    def string_id(self, name):
        index = self.string_ids.get(name)
        if index is None:
            raise ValueError("字符串表里没有 %r" % name)
        return index

    def decompile(self, buf):
        """把 0xB0D0 脚本转成文本。"""
        items = []
        off = 2
        end = len(buf)
        while off + 5 <= end:
            kind = buf[off]
            value = INT32.unpack_from(buf, off + 1)[0]
            off += 5
            if kind == 2:
                items.append("%d\t" % value)
            elif kind in (1, 3):
                items.append("{%d=`%d`}\t" % (kind, value))
            elif kind == 4:
                items.append("%r\t" % struct.unpack("<f", INT32.pack(value))[0])
            elif kind == 5:
                items.append("\r\n%s\r\n" % escape(self.name(value)))
            elif kind in (6, 8):
                items.append("{%d=`%s`}\r\n" % (kind, escape(self.name(value))))
            elif kind == 7:
                items.append("`%s`\t" % escape(self.name(value)))
            elif kind == 9:
                if off + 5 > end or buf[off] != 10:
                    raise ValueError("类型 9 后面没有跟类型 10")
                key = self.name(INT32.unpack_from(buf, off + 1)[0])
                off += 5
                items.append("<%d::%s`%s`>\r\n" % (value, escape(key), escape(self.link_value(value, key))))
            else:
                raise ValueError("未知的脚本类型 %d，偏移 %d" % (kind, off - 5))
        if off != end:
            raise ValueError("脚本末尾有 %d 个多余字节" % (end - off))
        return SCRIPT_HEADER.decode("ascii") + "".join(items)

    def compile(self, text):
        """把文本还原成 0xB0D0 脚本。text 是 str。"""
        if not text.startswith(SCRIPT_HEADER.decode("ascii")):
            raise ValueError("缺少 #PVF_File 文件头")
        out = bytearray(SCRIPT_MAGIC)
        pos = len(SCRIPT_HEADER)
        end = len(text)
        while pos < end:
            if text.startswith("\r\n", pos):
                pos += 2
                if pos >= end:
                    break
                stop = text.index("\r\n", pos)
                self._emit(out, 5, self.string_id(unescape(text[pos:stop])))
                pos = stop + 2
            elif text[pos] == "`":
                stop = self._find(text, "`", pos + 1)
                self._emit(out, 7, self.string_id(unescape(text[pos + 1:stop])))
                pos = self._skip_tab(text, stop + 1)
            elif text[pos] == "{":
                stop = self._find(text, "}", pos + 1)
                body = text[pos + 1:stop]
                kind_text, _, rest = body.partition("=`")
                kind = int(kind_text)
                if not rest.endswith("`"):
                    raise ValueError("{ 结构不对: %r" % body)
                inner = unescape(rest[:-1])
                if kind in (1, 3):
                    self._emit(out, kind, int(inner))
                    pos = self._skip_tab(text, stop + 1)
                elif kind in (6, 8):
                    self._emit(out, kind, self.string_id(inner))
                    pos = self._skip_crlf(text, stop + 1)
                else:
                    raise ValueError("未知的 { 类型 %d" % kind)
            elif text[pos] == "<":
                head_stop = text.index("::", pos)
                nstring = int(text[pos + 1:head_stop])
                quote = self._find(text, "`", head_stop + 2)
                key = unescape(text[head_stop + 2:quote])
                stop = self._find(text, "`", quote + 1)
                if not text.startswith(">", stop + 1):
                    raise ValueError("< 结构没有以 > 结束")
                self._emit(out, 9, nstring)
                self._emit(out, 10, self.string_id(key))
                pos = self._skip_crlf(text, stop + 2)
            else:
                stop = pos
                while stop < end and text[stop] not in "\t\r":
                    stop += 1
                token = text[pos:stop]
                if "." in token or "e" in token or "E" in token:
                    self._emit(out, 4, struct.unpack("<i", struct.pack("<f", float(token)))[0])
                else:
                    self._emit(out, 2, int(token))
                pos = self._skip_tab(text, stop)
        return bytes(out)

    @staticmethod
    def _emit(out, kind, value):
        out.append(kind)
        out += INT32.pack(value)

    @staticmethod
    def _find(text, char, start):
        """找到未被反斜杆转义的 char。"""
        pos = start
        while pos < len(text):
            if text[pos] == "\\":
                pos += 2
                continue
            if text[pos] == char:
                return pos
            pos += 1
        raise ValueError("找不到 %r" % char)

    @staticmethod
    def _skip_tab(text, pos):
        if text.startswith("\t", pos):
            return pos + 1
        if pos >= len(text) or text.startswith("\r\n", pos):
            return pos
        raise ValueError("期望制表符，位置 %d" % pos)

    @staticmethod
    def _skip_crlf(text, pos):
        if text.startswith("\r\n", pos):
            return pos + 2
        if pos >= len(text):
            return pos
        raise ValueError("期望换行，位置 %d" % pos)


# ---------------------------------------------------------------- 解包写出

def load_script_context(data, pack_start, by_path, lang):
    """从封包里读出字符串表、n_string.lst 和 .str，返回 ScriptText；缺表时返回 None。"""
    table = by_path.get(STRING_TABLE)
    if table is None:
        return None
    strings = load_string_table(entry_bytes(data, pack_start, table), lang.to_text)
    nstring_files = {}
    nstring = by_path.get(NSTRING_LIST)
    if nstring is not None:
        nstring_files = load_nstring_list(entry_bytes(data, pack_start, nstring), strings)
    str_values = {}
    for index, path in nstring_files.items():
        entry = by_path.get(path.lower())
        if entry is None:
            print("警告: n_string.lst 指向的 %s 不在封包里" % path, file=sys.stderr)
            continue
        str_values[index] = load_str_values(entry_bytes(data, pack_start, entry), lang.to_text)
    return ScriptText(strings, str_values)


def entry_bytes(data, pack_start, entry):
    _number, _path, length, crc, offset = entry
    start = pack_start + offset
    return decrypt_padded(data[start:start + ((length + 3) & ~3)], length, crc)


def unique_target(out_dir, parts, used):
    """同一条路径出现多次时，后出现的写成 name~1.ext，避免覆盖。"""
    target = os.path.join(out_dir, *parts)
    if target not in used:
        return target
    stem, ext = os.path.splitext(target)
    n = 1
    while "%s~%d%s" % (stem, n, ext) in used:
        n += 1
    return "%s~%d%s" % (stem, n, ext)


def extract(data, pack_start, entries, out_dir, scripts, keep_raw, lang):
    """把条目写到 out_dir，返回 (写入数, 跳过数, 重复数, 写入字节数, 转文本数)。"""
    written = 0
    skipped = 0
    dupes = 0
    converted = 0
    total = 0
    used = set()
    made_dirs = set()
    for entry in entries:
        raw_path = entry[1]
        parts = safe_parts(raw_path)
        if parts is None:
            skipped += 1
            print("跳过可疑路径 %r" % raw_path, file=sys.stderr)
            continue
        target = unique_target(out_dir, parts, used)
        if target != os.path.join(out_dir, *parts):
            dupes += 1
        used.add(target)
        parent = os.path.dirname(target)
        if parent not in made_dirs:
            os.makedirs(parent, exist_ok=True)
            made_dirs.add(parent)
        raw = entry_bytes(data, pack_start, entry)
        body = raw
        if not keep_raw and scripts is not None and raw[:2] == SCRIPT_MAGIC:
            body = scripts.decompile(raw).encode(TEXT_CODEC, "backslashreplace")
            converted += 1
        elif not keep_raw and raw_path.lower().endswith(".str"):
            body = str_file_to_text(raw, lang.to_text).encode(TEXT_CODEC, "backslashreplace")
            converted += 1
        with open(target, "wb") as f:
            f.write(body)
        written += 1
        total += len(raw)
    return written, skipped, dupes, total, converted


def verify(data, pack_start, entries, scripts):
    """逐个脚本做 文本->二进制 的往返。

    返回 (检查数, 字节完全一致数, 仅字符串下标不同数, 失败列表)。
    字符串表里有 3632 个重复文本，下标不唯一，往返时可能换成另一个同文本的下标，
    这种差异只比字节会误判，所以再比一次解析后的项目流。
    """
    if scripts is None:
        raise ValueError("封包里找不到 %s，无法校验" % STRING_TABLE)
    checked = 0
    exact = 0
    index_only = 0
    failures = []
    for entry in entries:
        raw = entry_bytes(data, pack_start, entry)
        if raw[:2] != SCRIPT_MAGIC:
            continue
        checked += 1
        try:
            again = scripts.compile(scripts.decompile(raw))
        except ValueError as exc:
            failures.append((entry[1], str(exc)))
            continue
        if again == raw:
            exact += 1
        elif item_stream(again, scripts) == item_stream(raw, scripts):
            index_only += 1
        else:
            failures.append((entry[1], "重新编码后项目流不一致"))
    return checked, exact, index_only, failures


def item_stream(buf, scripts):
    """把脚本拆成 (类型, 值) 列表，字符串类项目用解出的文本比较。"""
    items = []
    off = 2
    end = len(buf)
    while off + 5 <= end:
        kind = buf[off]
        value = INT32.unpack_from(buf, off + 1)[0]
        off += 5
        items.append((kind, scripts.name(value) if kind in (5, 6, 7, 10) else value))
    return items


# ---------------------------------------------------------------- 重新打包

def read_file(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None


def unpacked_bytes(original, path, scripts, lang, keep_raw):
    """解包时这个条目会写成什么，用来判断 output 里的文件动过没有。"""
    if keep_raw:
        return original
    if scripts is not None and original[:2] == SCRIPT_MAGIC:
        return scripts.decompile(original).encode(TEXT_CODEC, "backslashreplace")
    if path.lower().endswith(".str"):
        return str_file_to_text(original, lang.to_text).encode(TEXT_CODEC, "backslashreplace")
    return original


def packed_bytes(original, path, on_disk, scripts, lang):
    """把 output 里改过的文本还原成封包里的字节。"""
    if original[:2] == SCRIPT_MAGIC:
        if scripts is None:
            raise ValueError("%s 是脚本，但封包里没有 %s，无法还原" % (path, STRING_TABLE))
        return scripts.compile(on_disk.decode(TEXT_CODEC))
    if path.lower().endswith(".str"):
        try:
            return str_text_to_bytes(original, on_disk.decode(TEXT_CODEC), lang)
        except ValueError as exc:
            raise ValueError("%s: %s" % (path, exc))
    return on_disk


def build_archive(data, header, pack_start, entries, root, scripts, lang, keep_raw):
    """按 entries 的顺序读 root 下的文件，返回 (新封包字节, 统计, 用到的磁盘路径)。

    没动过的条目直接沿用原封包里的字节、密钥和偏移，所以原样打包会和来源完全一致。
    改过的条目追加到文件包末尾。output 里删掉的文件不再写进目录树。
    """
    pack = bytearray(data[pack_start:])
    tree = bytearray()
    used = set()
    kept = edited = missing = 0
    for entry in entries:
        number, path, _length, crc, offset = entry
        parts = safe_parts(path)
        if parts is None:
            continue
        target = unique_target(root, parts, used)
        used.add(target)
        on_disk = read_file(target)
        if on_disk is None:
            missing += 1
            continue
        original = entry_bytes(data, pack_start, entry)
        if on_disk == unpacked_bytes(original, path, scripts, lang, keep_raw):
            payload, key, offset = original, crc, offset
            kept += 1
        else:
            payload = packed_bytes(original, path, on_disk, scripts, lang)
            key = zlib.crc32(payload) & MASK
            offset = len(pack)
            pack += encrypt(payload + b"\x00" * (-len(payload) % 4), key)
            edited += 1
        path_bytes = path.encode("cp949")
        tree += INT32.pack(number)
        tree += INT32.pack(len(path_bytes))
        tree += path_bytes
        tree += INT32.pack(len(payload))
        tree += struct.pack("<I", key)
        tree += INT32.pack(offset)
    tree += b"\x00" * (-len(tree) % 4)
    body = (
        struct.pack("<I", len(header.uuid))
        + header.uuid.encode("ascii")
        + struct.pack("<iiIi", header.version, len(tree), header.tree_crc, kept + edited)
        + encrypt(tree, header.tree_crc)
        + pack
    )
    return bytes(body), kept, edited, missing, used


def unused_files(root, used):
    """output 里不属于原封包的文件。"""
    extra = []
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            path = os.path.join(dirpath, name)
            if path not in used:
                extra.append(path)
    return extra


# ---------------------------------------------------------------- 命令行

def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="解包和重新打包 DNF 的 PVF 封包（Script.pvf）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("pvf", nargs="?", default="Script.pvf", help="PVF 文件路径")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="解包输出目录（默认 output），打包输出目录（默认 rebuild）",
    )
    parser.add_argument("-i", "--input", default="output", help="打包时读取的目录")
    parser.add_argument("--pack", action="store_true", help="按 -i 目录重新打包，不写解包文件")
    parser.add_argument("--list", action="store_true", help="只列出条目路径和长度，不写文件")
    parser.add_argument(
        "--lang",
        choices=sorted(LANGUAGES),
        default="zh-hans",
        help="文本语言，zh-hans 转简体，zh-hant 保留原文",
    )
    parser.add_argument("--raw", action="store_true", help="原样解包，脚本和 .str 都不转")
    parser.add_argument("--verify", action="store_true", help="只校验脚本能无损还原成二进制")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    with open(args.pvf, "rb") as f:
        data = f.read()

    header, pack_start, entries = read_index(data)
    print(
        "%s: uuid=%s version=%d 条目=%d 文件包=%d 字节"
        % (args.pvf, header.uuid, header.version, len(entries), len(data) - pack_start),
        file=sys.stderr,
    )

    if args.list:
        for _number, raw_path, length, _crc, _offset in entries:
            print("%s\t%d" % (raw_path, length))
        return 0

    by_path = {}
    for entry in entries:
        by_path.setdefault(entry[1], entry)
        by_path.setdefault(entry[1].lower(), entry)
    lang = LANGUAGES[args.lang]
    scripts = None if args.raw else load_script_context(data, pack_start, by_path, lang)
    if scripts is None and not args.raw:
        print("警告: 封包里没有 %s，脚本保持二进制" % STRING_TABLE, file=sys.stderr)

    if args.pack:
        body, kept, edited, missing, used = build_archive(
            data, header, pack_start, entries, args.input, scripts, lang, args.raw
        )
        out_dir = args.output or "rebuild"
        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, os.path.basename(args.pvf))
        with open(target, "wb") as f:
            f.write(body)
        print(
            "打包完成: %s, 条目 %d, 未改动 %d, 改动 %d, 缺失 %d, %d 字节"
            % (target, kept + edited, kept, edited, missing, len(body)),
            file=sys.stderr,
        )
        if missing:
            print("output 里缺 %d 个文件，对应条目已从目录树移除" % missing, file=sys.stderr)
        extra = unused_files(args.input, used)
        if extra:
            print("output 里有 %d 个文件不属于原封包，已跳过" % len(extra), file=sys.stderr)
            for path in extra[:5]:
                print("  %s" % path, file=sys.stderr)
        return 0 if kept + edited else 1

    if args.verify:
        checked, exact, index_only, failures = verify(data, pack_start, entries, scripts)
        print(
            "校验 %d 个脚本: 字节一致 %d, 仅字符串下标不同 %d, 失败 %d"
            % (checked, exact, index_only, len(failures)),
            file=sys.stderr,
        )
        for path, reason in failures[:20]:
            print("  %s: %s" % (path, reason), file=sys.stderr)
        return 0 if not failures else 1

    out_dir = args.output or "output"
    os.makedirs(out_dir, exist_ok=True)
    written, skipped, dupes, total, converted = extract(
        data, pack_start, entries, out_dir, scripts, args.raw, lang
    )
    print(
        "解包完成: %d 个文件, %d 字节 -> %s" % (written, total, out_dir),
        file=sys.stderr,
    )
    if converted:
        print("其中 %d 个文件已转成文本" % converted, file=sys.stderr)
    if dupes:
        print("重复路径 %d 条，后出现的写成 <文件名>~<序号><扩展名>" % dupes, file=sys.stderr)
    if skipped:
        print("跳过 %d 条不安全路径" % skipped, file=sys.stderr)
    return 0 if written + skipped == len(entries) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, struct.error) as exc:
        sys.exit("错误: %s" % exc)

/*
 * CTI 戰情室｜語音導覽台詞
 *   每個群組對應多句台詞，格式：[說話者, 表情, 台詞]
 *   說話者：allan = Allan 顧問（zh-TW-YunJheNeural）、arale = AI 助理阿拉蕾（zh-TW-HsiaoYuNeural）
 *   表情：allan → smile laugh think scratch wow point wink shock
 *         arale → laugh think wow confused explain sad wink fight
 *   群組：welcome 開場、s_* 各區塊導覽、end 結束、d1～d4 情境演練
 * 修改台詞後依序執行：
 *   python3 tools/gen_audio.py --target dash
 *   python3 tools/build.py --target dash
 */
window.CTI_SCRIPT = {
  welcome: [
    ['arale', 'laugh', '歡迎進入 CTI 戰情室！這裡用一個畫面，掌握內部情資、外部情資和脆弱性的最新狀態。'],
    ['allan', 'smile', '我是 Allan 顧問。接下來帶你逐一看懂每個區塊：它在呈現什麼、有什麼管理意涵，以及該採取哪些行動。']
  ],
  s_overview: [['allan', 'point', '最上面是整體態勢。威脅指數綜合了相關情資、未修補的高風險弱點、逾期處置和告警異常。到了「高」，就要召開當日處置會議。']],
  s_brief: [['arale', 'explain', '這是我每天整理的 AI 晨報，把過去二十四小時最重要的三件事濃縮出來。不過內容要由資安人員覆核後才能發布喔！']],
  s_trend: [
    ['arale', 'fight', '內部告警依來源分成五類。像這個尖峰，就是一次針對 AD 帳號的密碼暴力破解。'],
    ['allan', 'think', '看到尖峰要追查原因；反過來，某個來源長期都是零，也可能是日誌沒有接上。']
  ],
  s_alerts: [['allan', 'point', '告警排行告訴我們最常發生的異常。登入失敗持續上升，就要檢查帳號鎖定和多因素驗證。']],
  s_funnel: [
    ['arale', 'explain', '外部情資蒐集了很多則，但跟我們資產相關的只有一小部分。這個漏斗，就是用資產清冊在過濾。'],
    ['allan', 'smile', '不相關的也要記錄判斷理由，每季再檢討哪些來源真的有用。']
  ],
  s_feed: [['allan', 'point', '最新情資會標出相關性、威脅程度和處置狀態。列入 KEV 又影響對外系統的，一定最優先處理。']],
  s_sla: [['allan', 'think', '弱點依 P1 到 P4 排序，紅色代表已經超過修補期限。逾期的要升級處理，或由風險擁有者正式簽核接受風險。']],
  s_cal: [['arale', 'wow', '檢測行事曆提醒弱掃、滲透測試、資安健診和原碼檢測的週期。快到期的要先排時程，滲透測試還要先取得授權！']],
  s_assets: [['allan', 'point', '高風險資產排行，讓我們看清楚風險集中在哪些系統。對外又核心的系統，要優先修補和隔離。']],
  s_matrix: [['arale', 'explain', '風險矩陣顯示未結案情資的分布，越靠右上角越危險。處置單要追到複測通過，才能結案。']],
  s_kpi: [['allan', 'smile', '最後是成效指標：偵測時間、修補時間、釣魚點擊率和日誌納管率。這些趨勢要定期提報管理審查。']],
  end: [
    ['arale', 'laugh', '導覽結束！點每個區塊右上角的「解讀」，可以隨時再聽一次說明。'],
    ['allan', 'smile', '也可以按上方的「情境演練」，體驗重大漏洞來襲時，戰情室怎麼應變。']
  ],
  d1: [['arale', 'wow', '警報！外部情資進來一筆重大漏洞：A 廠牌 SSL VPN 零時差漏洞，已經遭到利用！']],
  d2: [['allan', 'point', '第一步，比對資產清冊。我們有兩台對外的 A 廠牌 VPN，確認受到影響，威脅等級升到重大。']],
  d3: [['allan', 'think', '接著依應變程序：先緩解、再修補、最後複測結案，同時評估是否需要依規定通報。']],
  d4: [['arale', 'laugh', '處置完成，威脅指數降下來了！記得把整個過程留下紀錄，這就是稽核證據喔。']]
};

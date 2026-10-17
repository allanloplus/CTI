/*
 * CTI 情資作業全景｜串場台詞
 *   每段場景 id 對應多句台詞，格式：[說話者, 表情, 台詞]
 *   說話者：allan = Allan 顧問（zh-TW-YunJheNeural）、arale = AI 助理阿拉蕾（zh-TW-HsiaoYuNeural）
 *   表情：allan → smile 微笑、laugh 大笑、think 思考、scratch 抓頭、wow 驚訝、point 豎指強調、wink 眨眼、shock 驚呼
 *         arale → laugh 大笑、think 思考、wow 驚訝、confused 疑惑、explain 說明、sad 哭哭、wink 讚、fight 加油
 * 修改台詞後依序執行：
 *   python3 tools/gen_audio.py   只重新產生有變動的句子
 *   python3 tools/build.py       重新組成 index.html
 */
window.CTI_SCRIPT = {
  title: [
    ['arale', 'laugh', '大家好！我是 AI 小助手阿拉蕾。今天跟 Allan 顧問一起，帶大家走完整套情資作業！'],
    ['allan', 'smile', '資安不能靠感覺。要知道外面發生什麼、裡面發生什麼，還有自己哪裡有洞。']
  ],
  why: [
    ['allan', 'point', 'ISO 27001:2022 新增了 A.5.7 威脅情資。稽核時我一定會問：情資從哪來？誰在看？看完做了什麼？'],
    ['arale', 'wow', '原來情資還分策略、戰術、作業三層，給老闆看的跟給 SOC 看的不一樣！'],
    ['allan', 'smile', '沒錯。好的情資要相關、有洞察、有脈絡、可行動，少一樣都很難用。']
  ],
  overview: [
    ['arale', 'explain', '三條資料流：內部情資、外部情資、脆弱性識別，全部匯進情資融合中心！'],
    ['allan', 'point', '重點在後半段：分析完要變成風險處理、防護調整，最後回到管理審查，才算閉環。']
  ],
  cycle: [
    ['arale', 'think', '所以情資作業是一個循環？每轉一圈就更準一點？'],
    ['allan', 'laugh', '對！第六步「回饋」最常被忽略，卻是稽核員檢視持續改善的地方。']
  ],
  internal: [
    ['arale', 'fight', '內部情資我最拿手！日誌一進來，我就幫忙找出異常模式。'],
    ['allan', 'think', '先顧好基本功：日誌有沒有集中保存、時間有沒有同步、保存多久。不然出事時連證據都拿不出來。'],
    ['arale', 'wink', '還有同仁回報的可疑郵件，也是第一手情資喔！']
  ],
  external: [
    ['allan', 'point', '外部情資不是越多越好，關鍵是：跟我們有沒有關係？'],
    ['arale', 'wink', '交給我！我先用資產清冊過濾，只把相關的情資推給你～'],
    ['allan', 'smile', '也別忘了 ISAC 和同業交流，很多攻擊會先在同產業出現。']
  ],
  vuln: [
    ['arale', 'wow', '哇，脆弱性識別有這麼多種方法！'],
    ['allan', 'smile', '它們是互補的：弱掃看廣度、滲透測試看深度、原碼檢測從源頭擋、資安健診看有沒有已經被入侵。'],
    ['allan', 'point', '滲透測試前一定要先取得授權、界定範圍，避免影響營運。']
  ],
  priority: [
    ['arale', 'think', '只看 CVSS 的話，第一名應該是測試環境那個 9.1 吧？'],
    ['allan', 'point', '再加上脈絡：有沒有被利用、資產多重要、是不是對外。排序就完全不一樣了。'],
    ['arale', 'laugh', '對外的 VPN 直接跳到 P1！這就是以風險為基礎的處理！']
  ],
  ai: [
    ['arale', 'fight', '這段交給我！上百則情資，我很快就能讀完、分類、比對資產。'],
    ['allan', 'point', '很好，但最後按下核准的是人。AI 提供建議，責任還是在組織。'],
    ['arale', 'wink', '了解！我的每個建議都會留下紀錄，等你覆核～']
  ],
  action: [
    ['allan', 'smile', '每一筆情資都要有結論。就算是「現行不影響」，也要寫下判斷理由。'],
    ['arale', 'laugh', '這樣稽核員來的時候，就有完整的證據鏈啦！']
  ],
  evidence: [
    ['allan', 'point', '站在稽核員的角度，我會從這六點抽樣查核。'],
    ['arale', 'explain', '紀錄格式也幫大家準備好了：情資彙整、重大漏洞處理、資安月報，一次到位！']
  ],
  cadence: [
    ['arale', 'confused', '要做的事好多，時間要怎麼排呢？'],
    ['allan', 'smile', '固定節奏加上事件觸發。頻率依資安責任等級、法規與風險調整，再用 KPI 檢視成效。']
  ],
  finale: [
    ['arale', 'laugh', '謝謝大家！情資作業有任何問題，歡迎找 Allan 顧問～'],
    ['allan', 'laugh', '情資的價值在於轉化為行動。看得見、排得準、證得出，稽核自然不用怕！']
  ]
};

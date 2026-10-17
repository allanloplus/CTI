/*
 * 情資官特訓營｜角色配音台詞
 *   每個群組對應多句台詞，格式：[說話者, 表情, 台詞]
 *   說話者：allan = Allan 顧問（zh-TW-YunJheNeural）、arale = AI 助理阿拉蕾（zh-TW-HsiaoYuNeural）
 *   表情：allan → smile laugh think scratch wow point wink shock
 *         arale → laugh think wow confused explain sad wink fight
 *   群組：intro 開場、map 地圖說明、l1～l7 各關開場、boss 稽核提問、ok／ng 答對答錯、
 *         clear 過關、hit／miss 稽核關證據對錯、win／lose 稽核關結果、final 結訓
 * 修改台詞後依序執行：
 *   python3 tools/gen_audio.py --target game
 *   python3 tools/build.py --target game
 */
window.CTI_SCRIPT = {
  intro: [
    ['arale', 'laugh', '歡迎來到情資官特訓營！我是 AI 助理阿拉蕾，會陪你闖過七個關卡，成為合格的情資官！'],
    ['allan', 'smile', '我是 Allan 顧問。最後一關，我會用稽核員的身分來考你。準備好就出發吧！']
  ],
  map: [
    ['arale', 'explain', '點選地圖上發亮的關卡開始挑戰。每關拿到一顆星以上，就能解鎖下一關喔！']
  ],
  l1: [['arale', 'explain', '第一關，情資雷達！每張卡片是一個情資來源，請判斷它屬於內部情資、外部情資，還是脆弱性識別。']],
  l2: [['arale', 'think', '第二關，生命週期拼圖。先把六個步驟依照順序排好，再判斷每項工作屬於哪一步。']],
  l3: [['allan', 'point', '第三關，情資洪流。左邊是公司的資產清冊，請判斷每則情資跟我們有沒有關係。不相關的，也要記錄理由喔。']],
  l4: [['arale', 'fight', '第四關，檢測工具箱！看看每個情境，選出最適合的脆弱性識別方法。']],
  l5: [['allan', 'think', '第五關，風險排序戰。別只看 CVSS 分數，還要看有沒有遭到利用、資產重要性，以及是不是對外。']],
  l6: [['arale', 'explain', '第六關，情資判官。先判斷威脅程度，再選出最適當的第一步行動。']],
  l7: [['allan', 'point', '最終關卡！現在我是稽核員。我會問六個問題，請拿出正確的證據。答錯三次就不及格喔！']],
  boss: [
    ['allan', 'think', '第一題：你們的情資從哪些來源蒐集？由誰負責？多久蒐集一次？'],
    ['allan', 'point', '第二題：上個月公布的重大漏洞，你們怎麼評估對公司的影響？'],
    ['allan', 'think', '第三題：這個高風險弱點已經修補了嗎？要怎麼證明？'],
    ['allan', 'point', '第四題：你說這筆情資現行不影響，判斷的依據是什麼？'],
    ['allan', 'think', '第五題：滲透測試開始前，有沒有取得授權並界定範圍？'],
    ['allan', 'point', '最後一題：情資與弱點的結果，有沒有進到管理審查？']
  ],
  ok: [
    ['arale', 'laugh', '答對了！'],
    ['arale', 'wink', '漂亮，完全正確！'],
    ['arale', 'fight', '太厲害了，繼續保持！']
  ],
  ng: [
    ['arale', 'confused', '哎呀，再想想看～'],
    ['arale', 'think', '差一點點！看看下面的說明吧。'],
    ['allan', 'think', '這題要特別注意喔。']
  ],
  clear: [
    ['arale', 'laugh', '過關啦！'],
    ['allan', 'smile', '表現得很好，繼續挑戰下一關吧！']
  ],
  hit: [
    ['allan', 'wow', '嗯，這份證據可以接受。'],
    ['allan', 'smile', '很好，紀錄很完整。']
  ],
  miss: [
    ['allan', 'scratch', '這個證據不夠喔。'],
    ['allan', 'think', '這樣沒辦法證明有做到喔。']
  ],
  win: [['allan', 'laugh', '恭喜你！六個問題都拿出了適當的證據，稽核通過！']],
  lose: [['allan', 'think', '這次的證據還不夠充分，回去準備好再來挑戰吧！']],
  final: [
    ['arale', 'laugh', '恭喜結訓！你已經是合格的情資官了！'],
    ['allan', 'smile', '記得，情資的價值在於轉化為行動。我們下次見！']
  ]
};

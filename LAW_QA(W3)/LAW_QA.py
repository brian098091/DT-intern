#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 4.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No matching Intent."
                }
            ]
        }
"""

from requests import post
from requests import codes
import json
import math
import os
import re
try:
    from intent import Loki_Q2
    from intent import Loki_Q3
    from intent import Loki_Q4
    from intent import Loki_Q5
    from intent import Loki_Q6
    from intent import Loki_Q7
    from intent import Loki_Q8
    from intent import Loki_Q1
except:
    from .intent import Loki_Q2
    from .intent import Loki_Q3
    from .intent import Loki_Q4
    from .intent import Loki_Q5
    from .intent import Loki_Q6
    from .intent import Loki_Q7
    from .intent import Loki_Q8
    from .intent import Loki_Q1


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
try:
    accountInfo = json.load(open(os.path.join(os.path.dirname(__file__), "account.info"), encoding="utf-8"))
    USERNAME = accountInfo["username"]
    LOKI_KEY = accountInfo["loki_key"]
except Exception as e:
    print("[ERROR] AccountInfo => {}".format(str(e)))
    USERNAME = ""
    LOKI_KEY = ""

# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []
INPUT_LIMIT = 20

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    if "word_count_balance" in result:
                        self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "{} Connection failed.".format(result.status_code)
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    # 將 intent 會使用到的 key 預先設爲空列表
    resultDICT = {
       #"key": []
    }
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # Q2
                if lokiRst.getIntent(index, resultIndex) == "Q2":
                    resultDICT = Loki_Q2.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Q3
                if lokiRst.getIntent(index, resultIndex) == "Q3":
                    resultDICT = Loki_Q3.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Q4
                if lokiRst.getIntent(index, resultIndex) == "Q4":
                    resultDICT = Loki_Q4.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Q5
                if lokiRst.getIntent(index, resultIndex) == "Q5":
                    resultDICT = Loki_Q5.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Q6
                if lokiRst.getIntent(index, resultIndex) == "Q6":
                    resultDICT = Loki_Q6.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Q7
                if lokiRst.getIntent(index, resultIndex) == "Q7":
                    resultDICT = Loki_Q7.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Q8
                if lokiRst.getIntent(index, resultIndex) == "Q8":
                    resultDICT = Loki_Q8.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # Q1
                if lokiRst.getIntent(index, resultIndex) == "Q1":
                    resultDICT = Loki_Q1.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def execLoki(content, filterLIST=[], splitLIST=[]):
    """
    input
        content       STR / STR[]    要執行 loki 分析的內容 (可以是字串或字串列表)
        filterLIST    STR[]          指定要比對的意圖 (空列表代表不指定)
        splitLIST     STR[]          指定要斷句的符號 (空列表代表不指定)
                                     * 如果一句 content 內包含同一意圖的多個 utterance，請使用 splitLIST 切割 content

    output
        resultDICT    DICT           合併 runLoki() 的結果，請先設定 runLoki() 的 resultDICT 初始值

    e.g.
        splitLIST = ["！", "，", "。", "？", "!", ",", "
", "；", "　", ";"]
        resultDICT = execLoki("今天天氣如何？後天氣象如何？")                      # output => ["今天天氣"]
        resultDICT = execLoki("今天天氣如何？後天氣象如何？", splitLIST=splitLIST) # output => ["今天天氣", "後天氣象"]
        resultDICT = execLoki(["今天天氣如何？", "後天氣象如何？"])                # output => ["今天天氣", "後天氣象"]
    """
    contentLIST = []
    if type(content) == str:
        contentLIST = [content]
    if type(content) == list:
        contentLIST = content

    resultDICT = {}
    if contentLIST:
        if splitLIST:
            # 依 splitLIST 做分句切割
            splitPAT = re.compile("[{}]".format("".join(splitLIST)))
            inputLIST = []
            for c in contentLIST:
                tmpLIST = splitPAT.split(c)
                inputLIST.extend(tmpLIST)
            # 去除空字串
            while "" in inputLIST:
                inputLIST.remove("")
        else:
            # 不做分句切割處理
            inputLIST = contentLIST

        # 依 INPUT_LIMIT 限制批次處理
        for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
            lokiResultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)
            if "msg" in lokiResultDICT:
                return lokiResultDICT

            # 將 lokiResultDICT 結果儲存至 resultDICT
            for k in lokiResultDICT:
                if k not in resultDICT:
                    resultDICT[k] = []
                if type(lokiResultDICT[k]) == list:
                    resultDICT[k].extend(lokiResultDICT[k])
                else:
                    resultDICT[k].append(lokiResultDICT[k])

    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)

    if "msg" in resultDICT:
        print(resultDICT["msg"])

def testIntent():
    # Q2
    print("[TEST] Q2")
    inputLIST = ['在這裡可以找到律師嗎？','在這裡可以請教律師嗎？','我該找哪裡可以請教律師呢？','請問這裡有律師可以請教嗎？','這個地方是否有律師可諮詢？','這裡提供尋找律師的服務嗎？','可否請問在此處尋找律師的方式？','請問，我可以在這裡找到律師嗎？','這個地方有法律專家可以指導嗎？','請問，在這裡可以尋求法律協助嗎？','這個地點是否提供找尋律師的資訊？']
    testLoki(inputLIST, ['Q2'])
    print("")

    # Q3
    print("[TEST] Q3")
    inputLIST = ['法律人在法律百科回答問題，有沒有可能違反相關法令及倫理規範關於「利益衝突」的規定？']
    testLoki(inputLIST, ['Q3'])
    print("")

    # Q4
    print("[TEST] Q4")
    inputLIST = ['誰是認證法律人？','誰有確實的法律專業認證？','誰擁有獲得法律認證的資格？','誰被認可為合格的法律專家？','誰被證明具備法律專業能力？','有哪些人是經過法律專業認證的？','誰具有經過認證的法律專業資格？','誰被承認為合格的法律從業人員？','誰擁有經過正式認證的法律專業背景？']
    testLoki(inputLIST, ['Q4'])
    print("")

    # Q5
    print("[TEST] Q5")
    inputLIST = ['如何保證進階會員所寫文章的品質？','進階會員寫文章時，該如何確保品質？','為確保文章品質，進階會員能做些什麼？','只要是進階會員都能寫文章，如何確保文章的品質？','如何確保文章品質，這對於進階會員的限制是什麼？','若是進階會員則可以寫文章，但怎樣能確保其品質？','品質保證是所有進階會員寫文章的前提，該如何實現？','進階會員擁有寫文章的權利，應如何確保文章品質高？','進階會員能夠寫文章，不過如何確保其品質不受影響？']
    testLoki(inputLIST, ['Q5'])
    print("")

    # Q6
    print("[TEST] Q6")
    inputLIST = ['如何轉載法律百科的文章？','如何正確地轉載法律百科文章？','如何遵守法律百科的轉載指南？','如何引用或分享法律百科的文章？','如何在其他平臺上轉載法律百科的文章？','想要分享法律百科的文章，該如何操作？','在法律百科上轉載文章需要注意哪些事項？','如何在其他網站上轉載法律百科提供的文章？','想請問一下，我們可以如何轉載法律百科的內容？','若我想轉載法律百科上的文章，有什麼相關規定嗎？','針對法律百科內容的轉載，我們有哪些可以遵循的準則？']
    testLoki(inputLIST, ['Q6'])
    print("")

    # Q7
    print("[TEST] Q7")
    inputLIST = ['希望與法律百科提出合作邀約，怎麼進行？','如何與法律百科進行合作邀約是我們關心的問題。','我們希望與法律百科提出合作邀約，該如何進行？','想要與法律百科合作，我們希望瞭解如何進行邀約。','麻煩告訴我們與法律百科進行合作邀約的相關流程。','對於希望與法律百科合作提案，我們想知道進行方式。','我們希望能夠與法律百科合作，請問該如何進行邀約？','有沒有關於與法律百科合作邀約的具體步驟可以提供？','對於與法律百科開展合作邀約，我們需要知道如何進行。','對於向法律百科提出的合作邀約，我們希望瞭解具體操作步驟。']
    testLoki(inputLIST, ['Q7'])
    print("")

    # Q8
    print("[TEST] Q8")
    inputLIST = ['人工智慧AI出現，律師都可能被取代，法律百科呢？','人工智慧AI的出現可能導致律師被取代，法律百科又將如何應對？','若人工智慧AI進步取代律師，那麼法律百科是否也會有同樣的命運？','人工智慧AI的出現導致律師行業的變革，那麼法律百科又該如何因應？','如果人工智慧AI能夠取代律師，那麼對於法律百科而言會有什麼影響？','若人工智慧AI能夠取代律師的工作，那麼法律百科又有可能被取代嗎？','假若律師會因人工智慧AI而失業，那麼法律百科是否也會面臨相同的危機？']
    testLoki(inputLIST, ['Q8'])
    print("")

    # Q1
    print("[TEST] Q1")
    inputLIST = ['法律百科是非營利組織嗎？','法律百科是否為非營利組織？','法律百科是否屬於非營利性質？','法律百科是否屬於非營利組織？','法律百科是否是一個非營利機構？','法律百科是否為非營利性質的組織？','是否可以說法律百科屬於非營利型別？','是否可以認為法律百科是非營利性質的？','是否可以說法律百科是一個非營利組織？','法律百科是否是一個非營利型別的組織？','是否可以說法律百科是一個非營利性質的組織？']
    testLoki(inputLIST, ['Q1'])
    print("")


if __name__ == "__main__":
    # 測試所有意圖
    # testIntent()

    # 測試其它句子
    filterLIST = []
    # splitLIST = ["！", "，", "。", "？", "!", ",", "\n", "；", "\u3000", ";"]
    # resultDICT = execLoki("今天天氣如何？後天氣象如何？", filterLIST)            # output => ["今天天氣"]
    # resultDICT = execLoki("今天天氣如何？後天氣象如何？", filterLIST, splitLIST) # output => ["今天天氣", "後天氣象"]
    # resultDICT = execLoki(["今天天氣如何？", "後天氣象如何？"], filterLIST)      # output => ["今天天氣", "後天氣象"]
    resultDICT = execLoki("有沒有關於與法律百科合作邀約的具體步驟可以提供？")
    print(resultDICT["response"][0])
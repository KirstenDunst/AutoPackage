class CommonTool:
    # 转换成一级map
    @staticmethod
    def tranformDict(dict: dict, subKey=""):
        newDict = {}
        for k, v in dict.items():
            nowKey = k
            if subKey != "":
                nowKey = subKey + "." + k
                # nowKey = subKey + (k[0].upper() + k[1:len(k)])
            if str(v.__class__).__contains__("dict"):
                dealDict = CommonTool.tranformDict(v, subKey=nowKey)
                newDict.update(dealDict)
            else:
                newDict[nowKey] = v
        return newDict

    @staticmethod
    def getLocalDict() -> dict:
        return {
            "de": "de_DE",
            "en": "en_US",
            "es": "es_ES",
            "fr": "fr_FR",
            "it": "it_IT",
            "pl": "pl_PL",
            "pt": "pt_PT",
            "zh": "zh_CN",
            "nl": "nl_NL",
            "ja": "ja_JP",
            "ro": "ro_RO",
            "tr": "tr_TR",
            "ar": "ar_SA",
            "vi": "vi_VN",
            "id": "id_ID",
        }

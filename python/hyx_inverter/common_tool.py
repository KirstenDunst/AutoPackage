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

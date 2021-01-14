from Shapes import  changeShape, createNewCSV, statistics, changeValue
import csv, copy, random

def unitStatistics(section): #用来返回单个事件的频率
    dic = {}
    for sec in section:
        dic[sec] = 0
    path = "/Users/yjl/Downloads/北大/软件工程课程/项目/data/学生行为记录UTF8-value.csv"
    csvFile = open(path,'r')
    reader = csv.reader(csvFile)
    time = 0
    for line in reader:
        time += 1
        for i in range(1, len(line)):
            if line[i] == "1":
                dic[section[i-1]] += 1
    csvFile.close()
    for sec in section:
        dic[sec] /= time
    return dic

def doubleStatistics(section, unitDic): #用来返回两个事件在同一个记录中发生的概率
    dic = {}
    length = len(section)
    #考虑建立一个二维数组，行代表某个section，列代表与它关联的section的提升度lift, 坐标对应的section name由section来决定
    secMatrix = [[0 for i in range(length)] for j in range(length)]
    path = "/Users/yjl/Downloads/北大/软件工程课程/项目/data/学生行为记录UTF8-output.csv"
    time = 0
    csvFile = open(path, 'r')
    reader = csv.reader(csvFile)
    for line in reader:
        time += 1
        l = len(line)
        for i in range(l - 1):
            for j in range(i + 1, l):
                sec1, sec2 = line[i],line[j]
                if sec1 not in section or sec2 not in section:
                    continue
                x, y = section.index(sec1), section.index(sec2)
                secMatrix[x][y] += 1
    for i in range(length):
        for j in range(length):
            p1 = unitDic[section[i]]
            p2 = unitDic[section[j]]
            if p1 * p2 == 0:
                secMatrix[i][j] = 0
            else:
                secMatrix[i][j] /= (p1 * p2 * time)

    return secMatrix

def LiftStatistics(doubleDic):
    path = "/Users/yjl/Downloads/北大/软件工程课程/项目/data/学生行为记录UTF8-lift.csv"
    writeFile = open(path, 'w')
    writer = csv.writer(writeFile)
    writer.writerow(section)
    for line in doubleDic:
        writer.writerow(line)
    writeFile.close()

def findMaximum(secName, section, doubleDic, number):
    if secName not in section: #如果这个sec 不在section中，那么就随机返回几个
        return random.sample(section, number)
    length = len(section)
    pos = section.index(secName)
    res = []
    temp = copy.deepcopy(doubleDic[pos])
    for i in range(number):
        maximum = max(temp)
        if maximum == 0:
            res.append(random.randint(0, length - 1))
        else:
            index = temp.index(maximum)
            res.append(index)
            temp[index] = 0
    ans = []
    for num in res:
        Name = section[num]
        ans.append(Name)
    return ans



if __name__ == '__main__':
    section = statistics() #这里仍然需要用到section表单
    print(section)
    UnitDic = unitStatistics(section) #dic用来存储单个事件发生的频率
    #print(UnitDic)
    doubleDic = doubleStatistics(section, UnitDic)
    #print(doubleDic)
    #LiftStatistics(doubleDic)
    secName = "beidawlf_01_01_02"
    recommend_res = findMaximum(secName, section, doubleDic, 5)
    print(recommend_res)





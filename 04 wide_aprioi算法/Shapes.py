import csv
def changeShape():
    path = "/Users/yjl/Downloads/北大/软件工程课程/项目/data/学生行为记录UTF8.csv"
    i = 0
    res = {}
    with open(path,'r') as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            if i == 0:
                i += 1
                continue
            if line[1] in res:
                res[line[1]].append(line[2])
            else:
                res[line[1]] = [line[2]]
    return res

def createNewCSV(res):
    path = "/Users/yjl/Downloads/北大/软件工程课程/项目/data/学生行为记录UTF8-output.csv"
    csvFile = open(path,'w')
    writer = csv.writer(csvFile)
    for key, value in res.items():
        temp = []
        for v in value:
            temp.append(v)
        temp = list(set(temp))
        writer.writerow([key] + temp)
    csvFile.close()

def statistics():
    path = "/Users/yjl/Downloads/北大/软件工程课程/项目/data/section.csv"
    section = []
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            section.append(line[0])
    return section

def changeValue(section):
    readPath = "/Users/yjl/Downloads/北大/软件工程课程/项目/data/学生行为记录UTF8-output.csv"
    writePath = "/Users/yjl/Downloads/北大/软件工程课程/项目/data/学生行为记录UTF8-value.csv"
    readFile = open(readPath, 'r')
    writeFile = open(writePath, 'w')
    reader = csv.reader(readFile)
    writer = csv.writer(writeFile)
    writer.writerow(['id'] + section)
    for line in reader:
        temp = [0 for name in section]
        for sec in line:
            if sec in section:
                temp[section.index(sec)] = 1
        writer.writerow([line[0]] + temp)
    readFile.close()
    writeFile.close()

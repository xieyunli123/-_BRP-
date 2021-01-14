from Shapes import  changeShape, createNewCSV, statistics, changeValue

if __name__ == '__main__':
    #store = (changeShape()) 第一步，把学生活动文件转换成hash的形式
    #createNewCSV(store) 第二步，建立新表，表的列是学生编号以及他看过的section
    section = statistics() #第三步，section用来存储所有的课程小节
    #changeValue(section) #第四步，将第二步创立的文件转换成0或1的表格，1表示选了某课，0表示未选
   
    #至此，建立了学生编号与对应选课的矩阵
    #然后，考虑建立不同section的关联，看哪两种section容易被同一学生查看


分析一下，




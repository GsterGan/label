import os

f = open('index.html','r',encoding='gbk')
for i in range(0,5):
    print(f.readline().strip())

'''
输入一个小数序列，用逗号隔开，输出排序后的小数
'''

lis = input().split(',')
lis = [float(item) for item in lis]
lis.sort(reverse = True)
for item in lis:
    print(item)
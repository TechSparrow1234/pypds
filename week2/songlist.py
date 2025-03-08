n = int(input())
lis=[]
for i in range(n):
    m = int(input())
    for j in range(m):
        lis.append(input().split())

lis.sort(key=lambda x:int(x[1]), reverse=True)
for item in lis:
    print(item[0]+' '+item[1])
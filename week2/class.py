n,m = map(int,input().split())
name_lis=input().split()
dic = {item : 0 for item in name_lis}

for _ in range(m):
    temp = input().split()
    while temp:
        dic[temp.pop()]+=1
cnt=0
for key,value in dic.items():
    if value==0:
        cnt+=1
print(cnt)
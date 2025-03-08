'''
use eval function to get a list
sort the list by their score
'''
students = eval(input())
students.sort(key=lambda x:x[2], reverse = True)
n = len(students)
for _ in range(n):
    print(students[_][0], students[_][1], students[_][2])
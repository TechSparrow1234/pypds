def my_sum(*args, value=1):
    '''
    Add Value To Numbers
    '''
    cnt=0
    args=list(args)
    for arg in args:
        arg+=value
        args[cnt]=arg
        cnt+=1
    return args
    

print(my_sum(9, 9, 8, 2, 4, 4, 3, 5, 3, value=10))
print(my_sum(9, 9, 8, 2, 4, 4, 3, 5, 3))
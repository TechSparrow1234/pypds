def get_my_counter():
    '''
    编写一个闭包函数
    '''
    x=-1
    def inner():
        '''
        编写内函数
        '''
        nonlocal x
        x+=1
        return x
    return inner



mycounter = get_my_counter()
print(mycounter())
print(mycounter())
print(mycounter())

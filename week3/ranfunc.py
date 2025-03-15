import random

def my_random(keys, weights):
    '''
    从keys列表中加权随机抽取
    检验随机数是否则特定范围内
    '''
    tol = sum(weights)
    ran_num = random.uniform(0, tol)
    acum_w = 0
    for i, w in enumerate(weights):
        acum_w += w
        if ran_num <= acum_w:
            return keys[i]
    return None
    
    


# 后续为评测使用代码，请做题时忽视。
# 如提示结果WA，请根据题面中的查错指南进行排查。

if __name__ == "__main__":
    import base64
    exec(base64.b64decode(input().encode('utf-8')).decode('utf-8'))

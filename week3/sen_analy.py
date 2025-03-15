import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% 
def emo_analysis():
    '''
    混合情绪分析,统计文本中所有情绪出现次数
    '''
    # 闭包变量
    emo_lexi = {}
    emo_types = ["anger", "disgust", "fear", "sadness", "joy"]
    
    def load_lexi():
        '''
        内部函数,加载情绪词表
        '''
        # 在lexicon为空时才加载
        if not emo_lexi:
            for emo_type in emo_types:
                file_path = emo_type + '.txt'
                with open(file_path, 'r', encoding='utf-8') as f:
                    words = f.read().splitlines()
                    emo_lexi[emo_type] = set(words)
        return emo_lexi
    
    def mixed_emo_analysis(text):
        '''
        混合情绪分析
        '''
        # 先加载情绪词典
        # lexicon是一个字典，键是情绪，值是该情绪的单词集合
        lexicon = load_lexi()
        # 初始化词典
        emo_cnts = {emo_type: 0 for emo_type in emo_types}
        words = str(text).split()
        tol_emo_words = 0
        for word in words:
            for emo_type in emo_types:
                if word in lexicon[emo_type]:
                    emo_cnts[emo_type] += 1
                    tol_emo_words += 1
                    
        emo_prop = {emo_type: cnt/tol_emo_words if tol_emo_words else 0 
                    for emo_type, cnt in emo_cnts.items()}
        return emo_prop
     
    def unique_emo_analysis(text):
        '''
        唯一情绪分析
        '''
        lexicon = load_lexi()
        emo_cnts = {emo_type: 0 for emo_type in emo_types}
        words = str(text).split()
         
        # 遍历每一个单词，检查这个单词是不是某种情绪词
        for word in words:
            for emo_type in emo_types:
                if word in lexicon[emo_type]:
                    emo_cnts[emo_type] += 1
        max_cnt = max(emo_cnts.values())
        
        max_emo = [emo_type for emo_type, cnt in emo_cnts.items() if cnt == max_cnt]
        # 处理特殊情况
        if len(max_emo) > 1:
            return max_emo[0]
        elif max_cnt == 0:
            return 'neutral'
        else:
            return max_emo[0]
    # 返回内部函数
    return mixed_emo_analysis, unique_emo_analysis
def time_pattern_analysis(df, shop_id, emo_type, time_unit = 'hour'):
    '''
    分析指定店铺，指定情绪的时间模式，并可视化呈现
    
    :param df: 包含评论数据的dataframe
    :param shop_id: 店铺id
    :param emo_type: 指定的情绪类型
    :param time_unit: 时间单位，可以选hour, weekday等
    :return: none
    '''
    
    # 筛选指定店铺id的数据,创建一个新的dataframe
    shop_data = df[df['shopID'] == shop_id].copy()
    
    # 提取时间信息
    shop_data['time_period'] = pd.to_datetime(shop_data['comment_time'])
    try:
        shop_data['time_period'] = getattr(shop_data['time_period'].dt, time_unit)
    except AttributeError:
        print('time_unit not supported')
        return
    
    # 筛选指定情绪的数据（积极或者消极）
    if emo_type == 'positive':
        positive_emo = ['joy']
        shop_data['is_positive'] = shop_data['unique_emo'].isin(positive_emo)
        emo_ratio = shop_data.groupby('time_period')['is_positive'].mean()
    elif emo_type == 'negative':
        negative_emo = ['anger', 'disgust', 'fear', 'sadness']
        shop_data['is_negative'] = shop_data['unique_emo'].isin(negative_emo)
        emo_ratio = shop_data.groupby('time_period')['is_negative'].mean()
    else:
        print('emo_type not supported')

    # 可视化结果
    plt.figure(figsize=(10,6))
    sns.lineplot(x=emo_ratio.index, y=emo_ratio.values)
    plt.title(f"time pattern of {emo_type} emotion in shop {shop_id} {time_unit} mode")
    plt.xlabel(time_unit.capitalize())
    plt.ylabel(f"{emo_type.capitalize()} Emotion Ratio")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()    
        


file_path = 'week3.csv'
df = pd.read_csv(file_path)
comment = 'cus_comment'


mix_analysis, unique_analysis = emo_analysis()

df['mixed_emo'] = df[comment].apply(mix_analysis)
df['unique_emo'] = df[comment].apply(unique_analysis)

df.to_csv('week3_emo.csv', index=False)

#%%
# 画图
shop_id , emotype, time_unit = input("请输入店铺id 情绪类型 时间单位：").split()
shop_id = int(shop_id)
time_pattern_analysis(df, shop_id, emotype, time_unit)
# %%

rating_col = 'stars'
emo_col = 'unique_emo'

positive_emo = ['joy']
negative_emo = ['anger', 'disgust', 'fear', 'sadness']

df['emo_cat'] = 'neutral'
df.loc[df[emo_col].isin(positive_emo), 'emo_cat'] = 'positive'
df.loc[df[emo_col].isin(negative_emo), 'emo_cat'] = 'negative'

# 可视化展示
# 箱线图
plt.figure(figsize=(10,6))
sns.boxplot(x='emo_cat', y=rating_col, data=df)
plt.title('ating Distribution by Emotion Category')
plt.xlabel('Emotion Category')
plt.ylabel('Rating')
plt.show()

# 散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x=rating_col, y=emo_col, data=df)
plt.title('Relationship between Rating and Emotion')
plt.xlabel('Rating')
plt.ylabel('Emotion')
plt.show()

no_emotion_ratio = (df['emo_cat'] == 'neutral').mean()
print(f"情绪词典未覆盖的评论比例: {no_emotion_ratio * 100:.2f}%")

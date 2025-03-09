#%%
import jieba
import jieba.posseg as pseg
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'SimFang'

def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        stopwords = {line.strip() for line in file.readlines()}
    stopwords.add(' ')
    stopwords.add('\n')
    return stopwords    
    
# 任务1和任务2
try:
    with open('week2.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("以下是前十行内容：")
    for _, line in enumerate(lines[:10], start=1):
        print(f"第{_}行：{line.strip()}")
        
    doc = ''.join(lines)
except FileNotFoundError:
    print('未在相对路径下找到文件')
    exit()
#%%
# 任务3：对词频排序，并输出词频最高的10个词
terms = jieba.cut(doc)
terms = list(terms)
tfreq = Counter(terms)

top_10=tfreq.most_common(10)
print("词频最高的10个单词")
for term, freq in top_10:
    print(f'{term}\t{freq}')

#%%
# 任务4：加载停用词表，重新排序
# 加载停用词表
stopwords = load_stopwords('cn_stopwords.txt')
# 过滤词表
filtered_terms = [t for t in terms if t and t not in stopwords]
filtered_tfreq = Counter(filtered_terms)
# 重新输出词频最高的10个词
filtered_top_10 = filtered_tfreq.most_common(10)
print("过滤后词频最高的10个单词")
for term, freq in filtered_top_10:
    print(f'{term}\t{freq}')

#%%
# 任务5：删除部分低频词后对剩余结果进行可视化

# 设定词频阈值
freq_threshold = 100
# 取出低频词
tfreq = {term.strip(): freq for term, freq in filtered_tfreq.items() if freq >= freq_threshold}
fpath = r'C:\Windows\Fonts\simfang.ttf'
wd = WordCloud(font_path=fpath)
wd.fit_words(tfreq)
#wd.to_file('./wd.png')
plt.imshow(wd)
plt.axis('off')
plt.show()
#%%
# 任务6：对词性进行分析，再进行可视化
words_with_pos = pseg.cut(doc)
filtered_words_with_pos = [(word, pos) for word, pos in words_with_pos if word and word not in stopwords]

# 统计不同词性的出现频率
pos_freq = Counter()
for _, pos in filtered_words_with_pos:
    pos_freq[pos] += 1

# 打印不同词性的出现频率
print("不同词性的出现频率：")
for pos, freq in pos_freq.most_common():
    print(f"{pos}: {freq}")

specific_pos = 'n'
specific_words = [word for word, pos in filtered_words_with_pos if pos == specific_pos]
# 统计特定词性的词频
specific_tfreq = Counter(specific_words)
specific_tfreq = {term: freq for term, freq in specific_tfreq.items() if freq >= freq_threshold}

wd = WordCloud(font_path=r'C:\Windows\Fonts\simfang.ttf')
wd.fit_words(specific_tfreq)

# 显示特定词性的词云
plt.imshow(wd)
plt.axis('off')
plt.show()
#%%
# 任务7：统计高频的bigram，然后对其进行可视化
# 生成 bigram
bigrams = [(filtered_terms[i], filtered_terms[i + 1]) for i in range(len(filtered_terms) - 1)]

# 统计 bigram 频率
bigram_freq = Counter(bigrams)

# 过滤低频 bigram
bigram_freq_threshold = 2
filtered_bigram_freq = {bigram: freq for bigram, freq in bigram_freq.items() if freq >= bigram_freq_threshold}

# 将 bigram 转换为字符串形式，方便词云展示
bigram_str_freq = {' '.join(bigram): freq for bigram, freq in filtered_bigram_freq.items()}

# 打印高频 bigram
print("高频 bigram:")
for bigram, freq in Counter(bigram_str_freq).most_common(10):
    print(f'{bigram}\t{freq}')

# 生成 bigram 词云
bigram_wd = WordCloud(font_path=r'C:\Windows\Fonts\simfang.ttf')
bigram_wd.fit_words(bigram_str_freq)

# 显示 bigram 词云
plt.figure()
plt.imshow(bigram_wd)
plt.axis('off')
plt.show()
#%%
# 任务8
'''
可以利用词频加上停用词来筛选特征词
比如前文的top_10列表,就可以被作为特征词
有了特征词之后,可以对每一行进行向量表示
比如,设置一个10维向量,每个特征词出现一次
就在这个向量的特定位数上+1,这样可以表示出这个句子的向量
有了向量,可以利用余弦相似度或欧氏距离或曼哈顿距离来量化两个句子的相似性
'''
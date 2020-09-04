import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

file = pd.read_csv('./data/#seaweedchips.csv', encoding='unicode_escape')

#print(type(list(file['pp_text'])))
text_data = list(file['pp_text'])

word_string = ' '.join(text_data)
wc = WordCloud(stopwords=STOPWORDS, background_color='black', max_words=300).generate(word_string)

plt.figure(figsize=(15, 10))
plt.clf()
plt.imshow(wc)
plt.axis('off')
plt.show()

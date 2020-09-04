import pandas as pd

file = input("file name: ")
df = pd.read_csv(file)
df = df.drop('Unnamed: 0', axis=1)
print(df)

df = df.drop('text', axis=1)
df = df.drop('like', axis=1)

df = df.dropna(subset=['pp_text'])
new_df = pd.DataFrame([df['date'], df['user_id'], df['pp_text'], df['tag'], df['like_point']]).transpose()
print(new_df)
new_df.to_csv(file + '_complete.csv', header=True, encoding='utf-8-sig')


# %% [markdown]
# # Import Moduel

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# # Load Data

# %%
df_clean = pd.read_csv('input\cleaned_data.csv')

# %% [markdown]
# # 資料清理 & EDA
# 
# ---
# 
# * 100,000 筆評分 (1-5)
# * 943 位用戶(每位至少評估20部電影)
# * 1682 部電影(18部重複)

# %% [markdown]
# ## Rating 分佈

# %%
ax = sns.countplot(x='rating', data=df_clean)
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=10, xytext=(0, 5),
                textcoords='offset points')
plt.title(f'Distribution of rating')
plt.xlabel('rating')
plt.ylabel('Count')
plt.show()

# %% [markdown]
# ## Genres 分佈

# %%
# 電影類別數量 分佈
genres = df_clean.columns[10:]
genres_count = {}
for g in genres:
    genres_count[g] = df_clean.groupby('movie_title')[g].max().sum()
genre_df = pd.DataFrame(genres_count.items(), columns=['Genre', 'Count'])

# 繪圖
plt.figure(figsize=(12, 6))
ax = sns.barplot(x='Genre', y = 'Count', data=genre_df)
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=10, xytext=(0, 5),
                textcoords='offset points')
plt.title(f'Distribution of Genre')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# %% [markdown]
# ## 資料去重
# ---
# 相同user_id、movie_title; 不同movie_id、timestamp >> 同人同電影重複評論 >> 取平均rating

# %%
df_clean_copy = df_clean.copy()
# average_ratings = df_clean.groupby(['user_id', 'movie_title'])['rating'].mean().reset_index()
average_ratings = df_clean.groupby(['user_id', 'movie_title'], as_index=False).agg({"rating":"mean"})
data = df_clean_copy.merge(average_ratings, on=['user_id', 'movie_title'], suffixes=('', '_avg'))
data.drop(columns=['rating'], inplace=True)
data.rename(columns={'rating_avg': 'rating'}, inplace=True)

# %%
# check user_id、movie_title 相同的重複評分
data[(data.duplicated(subset=data.columns.difference(['movie_id','timestamp']), keep=False))][['user_id', 'movie_id','movie_title','rating']].sort_values(by='user_id')

# %%
# 檢查評論人數、電影總數前後落差
data_no_duplicates = data.drop_duplicates(subset=data.columns.difference(['movie_id','timestamp']), keep='last')
print('原資料評論人數 :', df_clean['user_id'].nunique())
print('原資料電影總數 :', df_clean['movie_title'].nunique())
print('不重複的評論者數 :', data_no_duplicates['user_id'].nunique())
print('不重複的電影總數 :', data_no_duplicates['movie_title'].nunique())

# %%
data_no_duplicates['rating'].value_counts().sort_index()



# %% [markdown]
# # Import Moduel

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# # Load Data

# %%
# genre_df = pd.read_csv('input/ml-100k/u.genre',sep='|')
# occupation_df = pd.read_csv('input/ml-100k/u.occupation')

# %%
# users
user_col = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
user_df = pd.read_csv('input/ml-100k/u.user', sep='|', names = user_col)

# %%
# ratings
ratings_col = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings_df = pd.read_csv('input/ml-100k/u.data', sep="\t", names = ratings_col)

# %%
# movies
item_col = ['movie_id', 'movie_title' ,'release_date','video_release_date', 'IMDb_URL', 'unknown', 'Action', 'Adventure',
 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
item_df = pd.read_csv('input/ml-100k/u.item', sep="|", encoding='latin-1', names=item_col)

# %%
print(ratings_df.shape) # (100000, 4)
print(item_df.shape) # (1682, 24)
print(user_df.shape) # (943, 5)

# %% [markdown]
# ## Ratings

# %%
ratings_df.head(3)

# %% [markdown]
# ## Items

# %%
item_df.head(3)

# %% [markdown]
# ## Users

# %%
user_df.head(3)

# %% [markdown]
# # Merge

# %%
df = pd.merge(ratings_df, user_df, on = "user_id")
df = pd.merge(df, item_df, on = 'movie_id')

# %%
df.shape

# %% [markdown]
# ## 欄位定義
# 1. user_id : 使用者id
# 2. movie_id : 電影id
# 3. rating : 評分(1~5)
# 4. timestamp : UTC of 1/1/1970 後幾秒
# 5. age : 年紀
# 6. sex : 性別
# 7. occupation : 職業
# 8. zip_code : 郵政編碼
# 9. movie_title : 電影名稱
# 10. release_date : 發佈日期
# 11. video_release_date : 家用媒體市場發佈日期(DVD、非電影院)
# 12. IMDb_URL : 該電影IMDb網址
# 13. 13 ~ 31 為電影分類(unknown, Action, Adventure, Animation, Children's, Comedy, Crime, Documentary,
#                       Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western)

# %% [markdown]
# # 資料清理 & EDA
# 
# ---
# 
# * 100,000 筆評分 (1-5)
# * 943 位用戶(每位至少評估20部電影)
# * 1682 部電影(18部重複)

# %%
# 常用函數
def count_plot(df, x):
    ax = sns.countplot(x=x, data=df)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=10, xytext=(0, 5),
                    textcoords='offset points')
    plt.title(f'Distribution of {x}')
    plt.xlabel(x)
    plt.ylabel('Count')
    plt.show()

# %%
df.info()

# %%
# 刪除IMDb_URL、video_release_date(全部缺失)
df_clean = df.drop(['IMDb_URL', 'video_release_date'], axis=1)

# %% [markdown]
# ## Rating 分佈

# %%
# Rating 數量分佈
count_plot(df_clean, 'rating')

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

# %% [markdown]
# # Content-Based filtering
# ---
# 內容相似度 : 輸入電影尋找相似的電影並推薦(餘弦相似度)
# 
# 概念 : 喜歡某電影，可能也喜歡類似該部的電影

# %%
from sklearn.metrics.pairwise import cosine_similarity

# %%
# 刪除內容相似度不需要的欄位
contentBased_df = item_df.drop(['release_date', 'video_release_date', 'IMDb_URL'], axis=1)
print('原始電影數 :', len(contentBased_df))
# 刪除相同movie_title不同movie_id但類型相同的重複電影
# contentBased_df.duplicated(subset=contentBased_df.columns.difference(['movie_id'])).sum() # 18
contentBased_df.drop_duplicates(subset=contentBased_df.columns.difference(['movie_id']), keep='last', inplace=True)
contentBased_df.reset_index(drop=True, inplace=True)
print('去重後電影數 :', len(contentBased_df))

# %%
features_matrix = contentBased_df.iloc[:, 2:]
cosine_sim_features = cosine_similarity(features_matrix, features_matrix)

# %%
def get_similar_movies_bycontent(df, movie_id, seen = [], num_recom = 10):
    idx = movie_id - 1
    sim_scores = list(enumerate(cosine_sim_features[idx])) # 該dix電影對其他電影的相似度 (index, score)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:] # 排序分數並排除自己

    # 使用者已看過的就不推, 如果全部電影都已看過則返回空結果
    temp = []
    id = 0
    while len(temp) != num_recom and id < len(sim_scores):
        real_idx = df.loc[sim_scores[id][0], 'movie_id']
        if real_idx not in seen:
            temp.append((real_idx, sim_scores[id][1]))
        id += 1
    
    # 返回電影movie_id, movie_title, 餘弦相似度
    result = []
    for movie_idx, score in temp:
        movie_info = {
            'movie_id':movie_idx,
            'movie_title':df[df['movie_id'] == movie_idx]['movie_title'].values[0],
            'cosine_similarity': round(score, 4)
        }
        result.append(movie_info)

    return pd.DataFrame(result)

# %%
contentBased_df[contentBased_df['movie_id'] == 1]['movie_title'].values[0]

# %%
# Test
# get_similar_movies_bycontent(data_set, 來源電影編號, 已看過電影編號(內建無), 推薦幾部相似的(內建10))
# 電影編號1為 Toy Story (1995)
# seen = contentBased_df['movie_id'].values << 全電影都看過

wantedTofind = contentBased_df[contentBased_df['movie_id'] == 1]['movie_title'].values[0]
seen = [700, 240, 18]
print(f'Recommendation for moives silmlar with "{wantedTofind}"')
print("You've already watched movies those we don't recommend again!")
for i, m in enumerate(seen, 1):
    print(i, contentBased_df[contentBased_df['movie_id'] == m]['movie_title'].values[0])
get_similar_movies_bycontent(contentBased_df, 1, seen, 5)



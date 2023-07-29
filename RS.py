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
user_df

# %% [markdown]
# # Merge

# %%
df = pd.merge(ratings_df, user_df, on = "user_id")
df = pd.merge(df, item_df, on = 'movie_id')

# %%
df.shape

# %%
# 12 ~ 30 是電影分類 
for i, v in enumerate(df.columns):
    print(i, v)

# %%
df.head()



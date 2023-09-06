import pandas as pd

# users
user_col = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
user_df = pd.read_csv('input/ml-100k/u.user', sep='|', names = user_col)

# ratings
ratings_col = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings_df = pd.read_csv('input/ml-100k/u.data', sep="\t", names = ratings_col)

# movies
item_col = ['movie_id', 'movie_title' ,'release_date','video_release_date', 'IMDb_URL', 'unknown', 'Action', 'Adventure',
 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
item_df = pd.read_csv('input/ml-100k/u.item', sep="|", encoding='latin-1', names=item_col)

if __name__ == "__main__":
    print(ratings_df.shape) # (100000, 4)
    print(item_df.shape) # (1682, 24)
    print(user_df.shape) # (943, 5)


# Merge
df = pd.merge(ratings_df, user_df, on = "user_id")
df = pd.merge(df, item_df, on = 'movie_id')

# 刪除IMDb_URL、video_release_date
df_clean = df.drop(['IMDb_URL', 'video_release_date'], axis=1)

# Save
df_clean.to_csv('./input/cleaned_data.csv', index=False)
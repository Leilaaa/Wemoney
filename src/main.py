import pandas as pd
from interest import Interest
from posts import Posts

interest_df = pd.read_csv("data/interest.csv")
posts_df = pd.read_csv("data/posts.csv")
users_df = pd.read_csv("data/users.csv")


user_interest = Interest(interest_df)
similarity_dict = user_interest.find_similarity()

users_posts = Posts(posts_df, similarity_dict)
sorted_post = users_posts.sort_posts_for_user(target_user="e31e7cf3-9c4b-4da7-be33-db0e0cf4edd7",
                                              by_reply_numbers=False,
                                              by_recency=True)
print(sorted_post)